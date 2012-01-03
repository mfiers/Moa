"""
Ruff
----

Ruffus/Jinja Backend
"""

import os
import re
import sys
import stat
import copy
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
from moa.backend.ruff.base import RuffBaseJob

def localMapExecutor(input, output, script, jobData):    
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
    rc = runner(jobData['wd'],  [tf.name], jobData, command=jobData['command'])
    if rc != 0:
        raise ruffus.JobSignalledBreak
    l.debug("Executing %s" % tf.name)
    

class RuffReduceJob(RuffBaseJob):    

    def execute(self):


        ## What files are prerequisites?
        prereqs = []
        for fsid in sysConf.job.data.prerequisites:
            prereqs.extend(sysConf.job.data.filesets[fsid]['files'])


        # What files are 'others' - 
        # i.e. those that are necessary, but do not force a rebuild
        # if updated - currently ignoring these - should probably 
        # look at this.
        others = []
        for fsid in sysConf.job.data.others:
            others.extend(sysConf.job.data.filesets[fsid]['files'])


        outputs = []
        for x in sysConf.job.data.outputs:
            outputs.extend(sysConf.job.data.filesets[x].files)
        inputs = []
        for x in sysConf.job.data.inputs:
            inputs.extend(sysConf.job.data.filesets[x].files)

        if len(outputs) != 1:
            moa.ui.exitError("invalid number of outputfiles for a reduce job")

        l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))


        fsInDict = dict(
            [(x, sysConf.job.data.filesets[x]['files'])
             for x in sysConf.job.data.inputs])
        fsOutDict = dict(
            [(x, sysConf.job.data.filesets[x]['files'][0])
             for x in sysConf.job.data.outputs])

        thisJobData = copy.copy(self.jobData)
        thisJobData.update(fsInDict)                
        thisJobData.update(fsOutDict)                

        thisJobData['command'] = 'run'
        runid = thisJobData.get('runid', "moa")

        runid = 'r' + runid
        thisJobData['runid'] = runid
        thisJobData['command'] = 'run'

        script = self.commands.render('run', thisJobData)
        l.debug("Executing %s" %  script)


        if hasattr(localMapExecutor, 'pipeline_task'):
            del localMapExecutor.pipeline_task

        #here we're telling ruffus to proceed using the in & output files
        #we're generating
        l.debug("decorating executor")
        executor2 = ruffus.files(
            [inputs + prereqs], outputs, script, thisJobData
            )(localMapExecutor)
        l.debug("Start reduce run")
            
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

        except ruffus.ruffus_exceptions.RethrownJobError as e:
            #any error thrown somewhere in the pipeline will be
            #caught here.
            l.debug("CAUGHT A RUFFUS ERROR!")
            l.debug(str(e))
            startOfError = "{{gray}}" + re.sub(r'\s+', " ", str(e))[:72].strip() + "...{{reset}}"
            moa.ui.error("Caught a Ruffus error")
            moa.ui.error(startOfError)

            try:
                #try to get some structured info & output that.
                einfo = e[0][1].split('->')[0].split('=')[1].strip()
                einfo = einfo.replace('[', '').replace(']', '')
                moa.ui.error("While  processing: %s" % einfo)
            except:
                pass
            moa.ui.exitError("Quitting")
                 

        #empty the ruffus node name cache needs to be empty -
        #otherwise ruffus might think that we're rerunning jobs
        if hasattr(localMapExecutor, 'pipeline_task'):
            for k in localMapExecutor.pipeline_task._name_to_node.keys():
                del localMapExecutor.pipeline_task._name_to_node[k]
                
        return rc
    
