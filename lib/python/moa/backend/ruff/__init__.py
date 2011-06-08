"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
import sys
import stat
import glob
import random
import tempfile
import subprocess

import ruffus
import ruffus.ruffus_exceptions

from jinja2 import Template as jTemplate

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.logger as l
from moa.sysConf import sysConf

import Yaco

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template2')


class RuffCommands(Yaco.Yaco):
    """
    Read commands for use with Ruff    
    """

    def __init__(self, confDir, moaid):

        super(RuffCommands, self).__init__()
        
        self._confDir = confDir
        self._moaid = moaid
        self.load()
        
    def load(self):
        """
        Load a ruff/jinja file
        """
        templateFile = os.path.join(
            self._confDir, 'template.d',
            '%s.jinja2' % (self._moaid))

        if os.path.exists(templateFile):
            #first, attempt to load 'old style' template files
            with open(templateFile) as F:
                raw = F.read()

            rawc = re.split('###', raw)

            for r in rawc:
                r = r.strip()
                if not r: continue
                splitr = r.split("\n", 1)
                if len(splitr) != 2:                
                    continue

                firstline, rest = splitr

                spl = firstline.strip().split()
                if rest[:2] != '#!':
                    rest = "#!%s\n" % sysConf.default_shell \
                           + rest
                self[spl[0]] = {
                    'script' : rest,
                    'args' : spl[1:] }
            
        # then load new style -looking for files called
        # {{moa_id}}.command.jinja2

        #to be implemented
        glb = "%s/template.d/%s.*.jinja2" % (
            self._confDir, self._moaid)
        for f in glob.glob(glb):
            cname = f.rsplit('/',1)[-1]\
                    .replace('%s.' % self._moaid, '')\
                    .replace('.jinja2', '')
            with open(f) as F:
                raw = F.read()
            self[cname] = {
                'script' : raw,
                'args' : []}
        
            
    def  render(self, command, data):

        if not self.has_key(command):
            return ""

        this = self[command]

        script = this.get('script', '')
        args = this.get('args', [])

        if 'noexpand' in args:
            return script
                
        jt = jTemplate(script)
        rscript = jt.render(data)
        
        if '{{' or '{%' in rscript:
            #try a second level jinja interpretation
            jt2 = jTemplate(rscript)
            rscript = jt2.render(data)

        return rscript

class Ruff(moa.backend.BaseBackend):
    """
    Ruffus backend class

    
    """
    def __init__(self, job):
        super(Ruff, self).__init__(job)

        self.commands = RuffCommands(
            self.job.confDir, self.job.template.moa_id)

    def hasCommand(self, command):
        return command in self.commands.keys()
    
    def defineOptions(self, parser):
        g = parser.add_option_group('Ruffus backend')
        parser.set_defaults(threads=1)
        g.add_option("-j", dest="threads", type='int',
                     help="threads to use when running Ruffus")

        g.add_option("-B", dest="remake", action='store_true',
                     help="Reexecute all targets (corresponds to make -B) ")

    def execute(self, command,
                verbose=False,
                silent=False,
                renderTemplate = True):
        """
        Execute a command

        :param renderTemplate: Jinja-render the template
        """

        if not self.commands.has_key(command):
            rc = -1
            return rc

        #determine which files are prerequisites
        prereqs = []
        for fsid in self.job.data.prerequisites:
            prereqs.extend(self.job.data.filesets[fsid]['files'])
                
        #determine which files are 'others' - i.e. those files that
        #are necessary, but do not force a rebuild if updated
        others = []
        for fsid in self.job.data.others:
            others.extend(self.job.data.filesets[fsid]['files'])
                    
        def generate_data_map():
            """
            Generator for a map operation -

            this function generates each pair of in & output files
            that constitute a single job.
            """
                  
            #determine number the number of files - make sure that each
            #job has the same number of in & output files
            noFiles = 0
            in_out_files = self.job.data.outputs + self.job.data.inputs
            for i, k in enumerate(in_out_files):
                if i == 0:
                    noFiles = len(self.job.data.filesets[k].files)
                else:
                    assert(len(self.job.data.filesets[k].files) == noFiles)

            #rearrange the files for yielding
            for i in range(noFiles):
                outputs = [self.job.data.filesets[x].files[i] 
                           for x in self.job.data.outputs]
                inputs =  [self.job.data.filesets[x].files[i] 
                           for x in self.job.data.inputs]
                
                l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))
                                
                fsDict = dict([(x, self.job.data.filesets[x]['files'][i])
                               for x in self.job.data.inputs + self.job.data.outputs])

                jobData = {}
                jobData.update(self.job.conf.render())
                jobData['wd'] = self.job.wd
                jobData['silent'] = silent
                jobData.update(fsDict)
                script = self.commands.render(command, jobData)
                l.debug("Executing %s" %  script)

                yield([inputs + prereqs], outputs, script, jobData)

        if self.job.template.commands.has_key(command):
            cmode = self.job.template.commands[command].mode
        else:
            cmode = 'simple'
            
        rc = 0

        #this is because we're possibly reusing the executor
        #function in multiple ruffus calls. In all cases it's to
        #be interpreted as a new, fresh call - so, remove all
        #metadata that might have stuck from the last time
        if hasattr(executor, 'pipeline_task'):
            del executor.pipeline_task

        if cmode == 'map':
            #if there are no & output files complain:
            if len(self.job.data.inputs) + len(self.job.data.outputs) == 0:
                moa.ui.exitError("no in or output files")

            #here we're telling ruffus to proceed using the in & output files
            #we're generating
            l.debug("decorating executor")
            executor2 = ruffus.files(generate_data_map)(executor)
            l.debug("Start run (with %d thread(s))" %
                   sysConf.options.threads)
            
            try:
                #Run!
                ruffus.pipeline_run(
                    [executor2],
                    verbose = sysConf.options.verbose,
                    one_second_per_job=False,
                    multiprocess= sysConf.options.threads,
                    logger = ruffus.black_hole_logger,                    
                    )
                rc = 0
                l.debug("Finished running (with %d thread(s))" %
                   sysConf.options.threads)

            except ruffus.ruffus_exceptions.RethrownJobError, e:
                #any error thrown somewhere in the pipeline will be
                #caught here.
                try:
                    #try to get some structured info & output that.
                    einfo = e[0][1].split('->')[0].split('=')[1].strip()
                    einfo = einfo.replace('[', '').replace(']', '')
                    moa.ui.warn("Caught an error processing: %s" % einfo)
                    raise
                except:
                    moa.ui.warn("Caught an error: \n%s" % str(e))
                    raise
                rc = 1
                 
        elif cmode == 'reduce':
            inputs = []
            for x in self.job.data.inputs:
                inputs.extend(self.job.data.filesets[x].files)
            outputs = []
            for x in self.job.data.outputs:
                outputs.extend(self.job.data.filesets[x].files)
            if len(outputs) != 1:
                moa.ui.exitError("invalid number of outputfiles for a reduce job")
                
            fsInDict = dict(
                [(x, self.job.data.filesets[x]['files'])
                 for x in self.job.data.inputs])
            fsOutDict = dict(
                [(x, self.job.data.filesets[x]['files'][0])
                 for x in self.job.data.outputs])

            jobData = {}
            jobData.update(self.job.conf.render())
            jobData['wd'] = self.job.wd
            jobData['input']
            jobData['silent'] = silent
            jobData.update(fsInDict)
            jobData.update(fsOutDict)
            script = self.commands.render(command, jobData)
            l.debug("Executing %s" %  script)
            executor2 = ruffus.files(
                [inputs + prereqs], outputs, script, jobData
                )(executor)
            l.debug("Start reduce run")
            try:
                #Run!
                ruffus.pipeline_run(
                    [executor2],
                    one_second_per_job=False,
                    verbose = sysConf.options.verbose,
                    logger = ruffus.black_hole_logger,                    
                    )
                rc = 0
                l.debug("Finished running (with %d thread(s))" %
                        sysConf.options.threads)
            except ruffus.ruffus_exceptions.RethrownJobError, e:
               #any error thrown somewhere in the pipeline will be
               #caught here.
               try:
                   #try to get some structured info & output that.
                   einfo = e[0][1].split('->')[0].split('=')[1].strip()
                   einfo = einfo.replace('[', '').replace(']', '')
                   moa.ui.warn("Caught an error processing: %s" % einfo)
                   raise
               except:
                   moa.ui.warn("Caught an error: %s" % str(e))
                   raise
               rc = 1
 
        elif cmode == 'simple':
            data = self.job.conf.render()
            data['job'] = self.job
            tf = tempfile.NamedTemporaryFile( 
                delete = False, prefix='moa', mode='w')
            script = self.commands.render(command, self.job.conf)
            tf.write(script + "\n")
            tf.close()
            os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            rc = moa.actor.simpleRunner(
                self.job.wd, [tf.name],
                silent=silent)

        #empty the ruffus node name cache needs to be empty -
        #otherwise ruffus might think that we're rerunning jobs
        if hasattr(executor, 'pipeline_task'):
            for k in executor.pipeline_task._name_to_node.keys():
                del executor.pipeline_task._name_to_node[k]
        return rc

#A hack - @improve_name randomizes the function name upon calling so
#it does not appear in the ruffus database of nodes
@moa.utils.simple_decorator
def improve_name(func):
    def f(*args, **kwargs):
        nn = 'executor_%s' % random.randint(0,100000)
        f.__name__ = nn
        f.func_name = nn
        func.__name__ = nn
        func.func_name = nn
        return func(*args, **kwargs)

    import random
    nn = 'executor_%s' % random.randint(0,100000)
    f.__name__ = nn
    f.func_name = nn
    func.__name__ = nn
    func.func_name = nn
    return f

#@improve_name
def executor(input, output, script, jobData):    
    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')
    
    tf.write(script)
    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    import logging
    for k in jobData:
        v = jobData[k]
        if isinstance(v, list):
            os.putenv(k, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(k, str(v))

    rc = moa.actor.simpleRunner(jobData['wd'],  [tf.name], silent=jobData['silent'])
    if rc != 0:
        raise ruffus.JobSignalledBreak
    l.debug("Executing %s" % tf.name)
    
