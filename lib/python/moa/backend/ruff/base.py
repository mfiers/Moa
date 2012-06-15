"""
Ruff
----

Ruffus/Jinja base job
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
import moa.backend
import moa.logger as l
from moa.sysConf import sysConf

from moa.backend.ruff.commands import RuffCommands

import Yaco

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template2')

class RuffBaseJob(object):

    def __init__(self, job, command, args):

        self.job = job
        self.command = command
        self.args = args

        self.commands = RuffCommands(job.confDir, job.template.moa_id)

        #dict, not Yaco! - ruffus does not like any complex objects
        self.jobData = {}
        self.getRunId()
        
    def go(self):
        """
        Run!
        """
        self.prepareJobData()
        self.writeScript()
        return self.execute()

    def getRunId(self):
        """
        Get a run id for this job
        """        
        runid = 'moa'
        job = sysConf.job
        if job.conf.project:
            runid = job.conf.project + '.' + runid
        if job.conf.get('jobid'):
            runid =  job.conf['jobid'] + '.' + runid
        self.jobData['runid'] = runid

    def prepareJobData(self):
        """
        Load job data, configuration into the jobConf
        """
        self.jobData.update(sysConf.job.data.simple())
        self.jobData.update(sysConf.job.conf.render())
        self.jobData['wd'] = sysConf.job.wd
        self.jobData['silent'] = False #sysConf.options.silent
        
    def writeScript(self):
        """
        Render & write the script to a tempfile
        """

        #save the file
        tmpdir = os.path.join(self.job.wd, '.moa', 'tmp')    
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)

        tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='moa.', 
                                         delete=False, suffix='.sh')
        #tmpfile.write("\n".join(sc))
        self.scriptFile = os.path.abspath(tmpfile.name)

        script = self.commands.render(self.command, self.jobData)
        tmpfile.write(script + "\n\n")
        tmpfile.close()
        os.chmod(tmpfile.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        
