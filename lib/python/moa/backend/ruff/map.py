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
    

class RuffMapJob(RuffBaseJob):    

    def execute(self):

        def generate_data_map():
            """
            Generator for a map operation -

            this function generates each pair of in & output files
            that constitute a single job.
            """

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
                    

            # determine number the number of files - make sure that each
            # job has the same number of in & output files

            noFiles = 0
            in_out_files = sysConf.job.data.outputs + sysConf.job.data.inputs
            for i, k in enumerate(in_out_files):
                if i == 0:
                    noFiles = len(sysConf.job.data.filesets[k].files)
                else:
                    assert(len(sysConf.job.data.filesets[k].files) == noFiles)

            # rearrange the files for yielding
                    
            for i in range(noFiles):
                outputs = [sysConf.job.data.filesets[x].files[i] 
                           for x in sysConf.job.data.outputs]
                inputs =  [sysConf.job.data.filesets[x].files[i] 
                           for x in sysConf.job.data.inputs]
                
                l.debug('pushing job with inputs %s' % ", ".join(inputs[:10]))
                                
                fsDict = dict([(x, sysConf.job.data.filesets[x]['files'][i])
                               for x in sysConf.job.data.inputs + sysConf.job.data.outputs])

                thisJobData = copy.copy(self.jobData)
                thisJobData.update(fsDict)                
                thisJobData['command'] = 'run'
                runid = thisJobData.get('runid', "moa")
                if sysConf.job.data.inputs:
                    fips =  sysConf.job.data.inputs[0]
                    ffn =  os.path.basename(fsDict[fips])
                    runid = ffn + '.' + runid
                runid = 'r' + runid
                thisJobData['runid'] = runid
                thisJobData['command'] = 'run'

                script = self.commands.render('run', thisJobData)
                l.debug("Executing %s" %  script)

                yield([inputs + prereqs], outputs, script, thisJobData)



        #this is because we're possibly reusing the this module (are we??)
        #function in multiple ruffus calls. In all cases it's to
        #be interpreted as a new, fresh call - so, remove all
        #metadata that might have stuck from the last time
        if hasattr(localMapExecutor, 'pipeline_task'):
            del localMapExecutor.pipeline_task
        
        #if there are no & output files complain:
        if len(sysConf.job.data.inputs) + len(sysConf.job.data.outputs) == 0:
            moa.ui.exitError("no in or output files")


        #here we're telling ruffus to proceed using the in & output files
        #we're generating
        l.debug("decorating executor")
        executor2 = ruffus.files(generate_data_map)(localMapExecutor)
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

        except ruffus.ruffus_exceptions.RethrownJobError as e:
            #any error thrown somewhere in the pipeline will be
            #caught here.
            l.debug("Caught a Ruffus error!")
            l.debug(str(e))
            startOfError = "{{gray}}" + re.sub(r'\s+', " ", str(e))[:72].strip() + "...{{reset}}"
            endOfError = "{{gray}}..." + re.sub(r'\s+', " ", str(e)).strip()[-72:] + \
                         "{{reset}}"
            moa.ui.error("Caught a Ruffus error")
            moa.ui.error(startOfError)
            moa.ui.error(endOfError)
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
                 

