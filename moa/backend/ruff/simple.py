"""
Ruff
----

Ruffus/Jinja Backend
"""

import moa.actor
import moa.logger as l
from moa.sysConf import sysConf

from moa.backend.ruff.base import RuffBaseJob

class RuffSimpleJob(RuffBaseJob):    
    
    def execute(self):
        l.debug("Executing simple with runid %s" % self.jobData['runid'])
        runner = moa.actor.getRunner()
        rc = runner(
            sysConf.job.wd, 
            [self.scriptFile], 
            self.jobData, 
            command=self.command
            )
        return rc

