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

from moa.backend.ruff.commands import RuffCommands
from moa.backend.ruff.simple import RuffSimpleJob
from moa.backend.ruff.map import RuffMapJob

import Yaco

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template2')

def load(job):
    """
    Load the backend
    """    
    return Ruff(job)

class Ruff(moa.backend.BaseBackend):
    """
    Ruffus backend class

    
    """
    def __init__(self, job):
        super(Ruff, self).__init__(job)

        self.commands = RuffCommands(
            self.job.confDir, self.job.template.moa_id)

    def prepare(self):
        """
        Run template prepare step - that is if there is a 
        prepare command defined.
        """
        pass

    def finish(self):
        """
        Run template finish step - that is if there is a 
        prepare command defined.
        """
        pass
        
    def hasCommand(self, command):
        return command in self.commands.keys()
    
    def defineOptions(self, parser):
        g = parser.add_option_group('Ruffus backend')
        parser.set_defaults(threads=1)
        g.add_option("-j", dest="threads", type='int',
                     help="threads to use when running Ruffus")

        #TODO:
        #g.add_option("-B", dest="remake", action='store_true',
        #             help="Reexecute all targets (corresponds to make -B) ")


    def simpleExecute(self, command):
        """
        Run a 'simple' template command
        """
        if not self.commands.has_key(command):
            return -1
        j = RuffSimpleJob(command)
        return j.go()

    def execute(self, 
                command,
                verbose=False,
                silent=False,
                renderTemplate = True):
        """
        Execute the 'run' template command

        :param renderTemplate: Jinja-render the template
        """

        if command != 'run':
            moa.ui.exitError("Not 'run'ning???")

        #should have 'run'...
        if not self.commands.has_key(command):
            return -1


        if self.job.template.commands.has_key(command):
            cmode = self.job.template.commands[command].mode
        else:
            cmode = 'simple'
            
        rc = 0
            
        if cmode == 'map':
            j = RuffMapJob('run')
            j.go()
            
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

            jobData = self.job.data.simple()
            jobData.update(self.job.conf.render())
            jobData['wd'] = self.job.wd
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
            j = RuffSimpleJob('run')
            j.go()

        #empty the ruffus node name cache needs to be empty -
        #otherwise ruffus might think that we're rerunning jobs
        if hasattr(executor, 'pipeline_task'):
            for k in executor.pipeline_task._name_to_node.keys():
                del executor.pipeline_task._name_to_node[k]
        return rc

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

    runner = moa.actor.getRunner()
    rc = runner(jobData['wd'],  [tf.name], jobData)
    if rc != 0:
        raise ruffus.JobSignalledBreak
    l.debug("Executing %s" % tf.name)
    
