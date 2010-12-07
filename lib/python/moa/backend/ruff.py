"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
import sys
import tempfile

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
        
        snippetsFile = os.path.join(
            MOABASE, 'lib', 'ruff', 'snippets.jinja2')

        self.commands = RuffCommands()
        self.commands.load(templateFile)
        self.snippets = RuffCommands()
        self.snippets.load(snippetsFile)
        
    def getCommandTemplate(self, command):
        return jTemplate(self.commands[command])
                
    def hasCommand(self, command):
        return True

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
        #self.job.plugins.run("readFilesets")

        l.debug("executing %s" % command)
        jt = self.getCommandTemplate(command)
        actor = moa.actor.Actor(self.job.wd)
        
        #rawConf = {}
        #for k in self.job.conf.keys():
        #        rawConf[k] = self.job.conf[k]

  
        #determine which files are prerequisites
        prereqs = []
        for fsid in self.job.data.prerequisites:
            prereqs.extend(self.job.data.fileSets[fsid]['files'])
                
            
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
            for i, k in enumerate(self.job.data.fileSets.keys()):
                if i == 0:
                    noFiles = len(self.job.data.fileSets[k]['files'])
                else:
                    assert(len(self.job.data.fileSets[k]['files']) == noFiles)
          
            #rearrange files
            for i in range(noFiles):
                outputs = [self.job.data.fileSets[x]['files'][i] 
                           for x in self.job.data.outputs]
                inputs =  [self.job.data.fileSets[x]['files'][i] 
                           for x in self.job.data.inputs]

                l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))
                
                fsDict = dict([(x, self.job.data.fileSets[x]['files'][i]) 
                               for x in self.job.data.inputs + self.job.data.outputs])
                
                jobData = fsDict
                jobData.update(self.job.conf)
                jobData['snippets'] = self.snippets
                script = jt.render(jobData)
                                 
                yield([inputs + prereqs], outputs, actor, script)
                       
        cmode = self.job.template.commands[command].mode

        if cmode == 'map':
            #late decoration - see if that works :/
            executor2 = ruffus.files(generate_data_map)(executor)
            ruffus.pipeline_run([executor2],
                                verbose = self.job.options.verbose,
                                one_second_per_job=False,
                                multiprocess= self.job.options.threads,
                                )
        elif cmode == 'reduce':
            pass
        elif cmode == 'simple':
            tf = tempfile.NamedTemporaryFile( 
                delete = False, prefix='moa', mode='w')
            tf.write(jt.render(self.job.conf))
            tf.close()
            l.debug("exxxxxecuting script %s" % tf.name)
            actor.run(['bash', '-e', tf.name])


def executor(input, output, actor, script):

    tf = tempfile.NamedTemporaryFile( delete = False,
                                      prefix='moa',
                                      mode='w')
    tf.write(script)
    tf.close()
    cl = ['bash', '-e', tf.name]
    actor.run(cl)
