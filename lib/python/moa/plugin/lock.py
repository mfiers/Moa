"""
**logger** - Log Moa activity



"""

import os
import re
import sys
from datetime import datetime

import moa.ui
import moa.job
import moa.logger as l
import moa.plugin

def defineCommands(data):
    data['commands']['unlock'] = { 
        'desc' : 'Unlock this job',
        'call' : unlock
        }
    data['commands']['lock'] = { 
        'desc' : 'Lock this job - prevent execution',
        'call' : lock
        }
    
def preRun(data):
    if os.path.exists(os.path.join(data.job.confDir, 'lock')):
        moa.ui.fprint(("This {{bold}}{{green}}Moa{{reset}} job is "
                       "{{bold}}{{red}}locked{{reset}} "
                       "(try 'moa unlock')"), f='jinja')
        sys.exit(-1)

def unlock(data):
    lockfile = os.path.join(data.job.confDir, 'lock')
    if os.path.exists(lockfile):
        os.remove(lockfile)

def lock(data):
    lockfile = os.path.join(data.job.confDir, 'lock')
    if not os.path.exists(lockfile):
        with open(lockfile, 'w') as F:
            F.write(" ")
        
def finish(data):

    data.logger.end_time = datetime.today()
    data.logger.run_time = data.logger.end_time - data.logger.start_time
    runtime = data.logger.end_time - data.logger.start_time
    logFile = os.path.join(data.job.confDir, 'log')
    
    with open(logFile, 'a') as F:
        F.write("%s\n" % "\t".join([
            str(data.rc),
            ",".join(data.executeCommand),
            data.logger.start_time.strftime("%Y-%m-%dT%H:%M:%S:%f"),
            data.logger.end_time.strftime("%Y-%m-%dT%H:%M:%S:%f"),
            str(runtime),
            " ".join(sys.argv)
            ]))
        
def showLog(data):
    logFile = os.path.join(data.job.confDir, 'log')
    with open(logFile) as F:
        for line in F:
            print line
