"""
Ruff
----

Ruffus (and Jinja) Backend
"""

import os

import ruffus
#import ruffus.ruffus_exceptions

import moa.utils
import moa.template
import moa.actor
import moa.exceptions
import moa.backend
import moa.logger
from moa.sysConf import sysConf

from moa.backend.ruff.commands import RuffCommands
from moa.backend.ruff.simple import RuffSimpleJob
from moa.backend.ruff.reduce import RuffReduceJob
from moa.backend.ruff.map import RuffMapJob

import Yaco

l = moa.logger.getLogger(__name__)
#l.setLevel(moa.logger.DEBUG)

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
        pass

    def execute(self, job, command, args):
        """
        Run a 'simple' template command
        """

        if not self.commands.has_key(command):
            l.debug("command '%s' does not exists" % command)
            l.debug("was able to find: %s" % str(self.commands.keys()))
            raise moa.exceptions.MoaCommandDoesNotExist
        
        #see how it should execute
        cmode = job.template.commands[command].get('mode', 'simple')

        l.debug('executing %s' % command)
            
        rc = 0                
        if cmode == 'map':
            j = RuffMapJob(job, command, args)
            rc = j.go()
            
        elif cmode == 'reduce':
            j = RuffReduceJob(job, command, args)
            rc = j.go()
 
        elif cmode == 'simple':
            j = RuffSimpleJob(job, command, args)
            rc = j.go()

        #empty the ruffus node name cache needs to be empty -
        #otherwise ruffus might think that we're rerunning jobs
        if hasattr(executor, 'pipeline_task'):
            for k in executor.pipeline_task._name_to_node.keys():
                del executor.pipeline_task._name_to_node[k]
                
        return rc

def executor(input, output, script, jobData):
    """
    Execute the script
    """
    import tempfile
    import stat

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

    runner = moa.actor.getRunner()
    rc = runner(jobData['wd'],  [tf.name], jobData)
    if rc != 0:
        raise ruffus.JobSignalledBreak
    l.debug("Executing %s" % tf.name)
    
