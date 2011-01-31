"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
import sys
import tempfile
import subprocess

import ruffus

from jinja2 import Template as jTemplate

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.sysConf
import moa.logger as l

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

        rawc = re.split('### *(\w+) *\n', raw)
        commands = dict([(rawc[i], rawc[i+1].strip())
                         for i in range(1, len(rawc), 2)])
        self.update(commands)
    
class Ruff(moa.backend.BaseBackend):
    """
    Ruffus backend class

    
    """
    def __init__(self, job):
        super(Ruff, self).__init__(job)
        
        templateFile = os.path.join(
            TEMPLATEDIR, '%s.jinja2' % (self.job.template.moa_id))

        self.commands = RuffCommands()

        if not os.path.exists(templateFile):
            l.critical("cannot find template file %s" % templateFile)
            moa.ui.exitError("Template %s does not seem to be properly installed" % 
                             self.job.template.moa_id)
        self.commands.load(templateFile)

        snippetsFile = os.path.join(
            MOABASE, 'lib', 'ruff', 'snippets.jinja2')
        self.snippets = RuffCommands()
        self.snippets.load(snippetsFile)

    def getCommandTemplate(self, command):
        if self.commands.has_key(command):
            return jTemplate(self.commands[command])
        else:
            return False
                
    def hasCommand(self, command):
        return command in self.commands.keys()

    def defineOptions(self, parser):
        g = parser.add_option_group('Ruffus backend')
        parser.set_defaults(threads=1)
        g.add_option("-j", dest="threads", type='int',
                     help="threads to use when running Ruffus")

        g.add_option("-B", dest="remake", action='store_true',
                     help="Reexecute all targets (corresponds to make -B) ")
        
    def execute(self, command, verbose=False, background=False):
        """
        Execute a command
        """
        #self.job.plugins.run("readfilesets")

        jt = self.getCommandTemplate(command)
        actor = self.job.getActor()

        #determine which files are prerequisites
        prereqs = []
        for fsid in self.job.data.prerequisites:
            prereqs.extend(self.job.data.filesets[fsid]['files'])
                
            
        def generate_data_map():
            """
            Process & generate the data for a map operation
            """
            rv = []
  
            if len(self.job.data.inputs) + len(self.job.data.outputs) == 0:
                l.critical("no in or output files")
                sys.exit()
                
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
                jobData.update(fsDict)
                script = jt.render(jobData)
                yield([inputs + prereqs], outputs, script, jobData)


        if self.job.template.commands.has_key(command):
            cmode = self.job.template.commands[command].mode
        else:
            cmode = 'simple'
            
        rc = 0
        if cmode == 'map':
            #late decoration - see if that works :/
            executor2 = ruffus.files(generate_data_map)(executor)
            l.critical("start run map with %d threads" % self.job.options.threads)
            ruffus.pipeline_run([executor2],
                                verbose = self.job.options.verbose,
                                one_second_per_job=False,
                                multiprocess= self.job.options.threads,
                                )
            l.critical("Done run map with %d threads" % self.job.options.threads)
            rc = 0
        elif cmode == 'reduce':
            pass
        elif cmode == 'simple':
            tf = tempfile.NamedTemporaryFile( 
                delete = False, prefix='moa', mode='w')
            tf.write("\n" + jt.render(self.job.conf)+ "\n")
            tf.close()
            rc = actor.run(['bash', '-e', tf.name])            
        return rc



def executor(input, output, script, jobData):    
    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')
    tf.write(script)
    tf.close()
    cl = ['bash', '-e', tf.name]
    l.debug("Executing %s" % " ".join(cl))
    #dump the configuration in the env
    for k in jobData:
        v = jobData[k]
        if isinstance(v, list):
            os.putenv(k, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(k, str(v))
    rc = subprocess.call(cl)
    print cl
