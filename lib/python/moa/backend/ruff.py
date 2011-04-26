"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
import sys
import stat
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
    def load(self, from_file):
        """
        Load a ruff/jinja file
        """
        with open(from_file) as F:
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
        
        templateFile = os.path.join(
            self.job.confDir, 'template.d',
            '%s.jinja2' % (self.job.template.moa_id))

        self.commands = RuffCommands()

        if not os.path.exists(templateFile):
            l.error("cannot find template file %s" % templateFile)
        else:
            self.commands.load(templateFile)

        #TODO: Remove snippets
        snippetsFile = os.path.join(
            MOABASE, 'lib', 'ruff', 'snippets.jinja2')
        self.snippets = RuffCommands()
        self.snippets.load(snippetsFile)

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
                verbose=False, silent=False,
                renderTemplate = True):
        """
        Execute a command

        :param renderTemplate: Jinja-render the template
        """

        if not self.commands.has_key(command):
            moa.ui.exitError("Unknown command %s" % command)

        if len(self.job.data.inputs) + len(self.job.data.outputs) == 0:
            moa.ui.exitError("no in or output files")
            sys.exit()
            
        #determine which files are prerequisites
        prereqs = []
        for fsid in self.job.data.prerequisites:
            prereqs.extend(self.job.data.filesets[fsid]['files'])
                
        #determine which files are 'others'
        others = []
        for fsid in self.job.data.others:
            others.extend(self.job.data.filesets[fsid]['files'])
                    
        def generate_data_map():
            """
            Process & generate the data for a map operation
            """
            rv = []
  
         
                
            #determine number the number of files
            noFiles = 0
            in_out_files = self.job.data.outputs + self.job.data.inputs
            for i, k in enumerate(in_out_files):
                if i == 0:
                    noFiles = len(self.job.data.filesets[k].files)
                else:
                    assert(len(self.job.data.filesets[k].files) == noFiles)

            #rearrange files
            for i in range(noFiles):
                outputs = [self.job.data.filesets[x].files[i] 
                           for x in self.job.data.outputs]
                inputs =  [self.job.data.filesets[x].files[i] 
                           for x in self.job.data.inputs]
                
                l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))
                
                
                fsDict = dict([(x, self.job.data.filesets[x]['files'][i]) 
                               for x in self.job.data.inputs + self.job.data.outputs])
                
                jobData = {}
                jobData.update(self.job.conf)
                jobData['snippets'] = self.snippets.get_data()
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
        if cmode == 'map':
            
            #late decoration - see if that works :/
            executor2 = ruffus.files(generate_data_map)(executor)
            
            l.info("Start run (with %d thread(s))" %
                   sysConf.options.threads)

            try:
                ruffus.pipeline_run(
                    [executor2],
                    verbose = sysConf.options.verbose,
                    one_second_per_job=False,
                    multiprocess= sysConf.options.threads,
                    )
                rc = 0
                l.debug("Finished running (with %d thread(s))" %
                   sysConf.options.threads)

            except ruffus.ruffus_exceptions.RethrownJobError, e:
                try:
                    einfo = e[0][1].split('->')[0].split('=')[1].strip()
                    einfo = einfo.replace('[', '').replace(']', '')
                    moa.ui.warn("Caught an error processing: %s" % einfo)
                except:
                    moa.ui.warn("Caught an error: %s" % str(e))
                rc = 1                
        elif cmode == 'reduce':
            pass
        elif cmode == 'simple':
            tf = tempfile.NamedTemporaryFile( 
                delete = False, prefix='moa', mode='w')
            script = self.commands.render(command, self.job.conf)
            tf.write(script + "\n")
            tf.close()
            os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            rc = moa.actor.simpleRunner(
                self.job.wd, [tf.name],
                silent=silent)
        return rc

def executor(input, output, script, jobData):    
    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')
    
    tf.write(script)
    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

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
    
