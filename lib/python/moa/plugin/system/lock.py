# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**lock** - Lock/Unlock moa jobs
-------------------------------



"""

import os
import sys

import moa.ui
import moa.job
import moa.logger as l
import moa.args
import moa.plugin
from moa.sysConf import sysConf
    
def hook_check_run():
    command = sysConf.originalCommand

    #see if this command is 'lockable'
    if command in sysConf.plugins.lock.runnable: 
        return True

    if os.path.exists(os.path.join(sysConf.job.confDir, 'lock')):
        moa.ui.fprint(("This {{bold}}{{green}}Moa{{reset}} job is " +
                       "{{bold}}{{red}}locked{{reset}}"), f='jinja')
        
        return False

    else:
        return True

@moa.args.needsJob
@moa.args.command
def unlock(job, args):
    """
    Unlock a job - allow execution
    """
    lockfile = os.path.join(job.confDir, 'lock')
    if os.path.exists(lockfile):
        l.debug("unlocking job in %s" % job.wd)
        os.remove(lockfile)

@moa.args.needsJob
@moa.args.command
def lock(job, args):
    """
    Lock a job - prevent execution
    """
    lockfile = os.path.join(job.confDir, 'lock')
    if not os.path.exists(lockfile):
        l.debug("locking job in %s" % job.wd)
        with open(lockfile, 'w') as F:
            F.write(" ")        


LOCKTEST = '''
moa simple --np -t test -- echo "poiuy"
out=`moa run` 2>/dev/null
[[ ! -f ".moa/lock" ]]
[[ ! "$out" =~ "querty" ]]
[[ "$out" =~ "poiuy" ]]
moa lock
[[ -f ".moa/lock" ]]
out=`moa run 2>&1 || true`
[[ "$out" =~ "This Moa job is locked" ]]
'''


UNLOCKTEST = '''
moa simple --np -t test -- echo "poiuy"
moa lock
[[ -f ".moa/lock" ]]
out=`moa run 2>&1 || true`
[[ "$out" =~ "This Moa job is locked" ]]
moa unlock
[[ ! -f ".moa/lock" ]]
out=`moa run` 2>/dev/null
[[ ! "$out" =~ "querty" ]]
[[ "$out" =~ "poiuy" ]]
'''
