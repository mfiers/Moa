"""
**lock** - Lock/Unlock moa jobs
-------------------------------



"""

import os
import sys

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
        l.debug("unlocking job in %s" % data.job.wd)
        os.remove(lockfile)

def lock(data):
    lockfile = os.path.join(data.job.confDir, 'lock')
    if not os.path.exists(lockfile):
        l.debug("locking job in %s" % data.job.wd)
        with open(lockfile, 'w') as F:
            F.write(" ")
        
