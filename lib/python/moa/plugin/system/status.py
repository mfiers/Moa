# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**status** - Job Status
-----------------------

Possible job states:

* waiting - not yet executed
* running - is currently being executed
* success - finished succesfully
* error   - finished with an error
* interrupted - manual interruption

"""

import os
import signal

import moa.ui
import moa.utils
import moa.args
import moa.logger as l
from moa.sysConf import sysConf

LLOG = False
STATUS = 'unknown'

@moa.args.addFlag('-a', dest='showAll', help='show all parameters')
@moa.args.addFlag('-p', dest='showPrivate', help='show private parameters')
@moa.args.addFlag('-R', dest='showRecursive', help='show recursively defined '
                  + 'parameters not specified by the local template')
@moa.args.addFlag('-u', dest='showUnrendered', help='show unrendered values '+
                  '(when using inline parameters)')
@moa.args.needsJob
@moa.args.doNotLog
@moa.args.command
def status(job, args):
    """
    Show job status

    Print a short status of the job, including configuration
    """
    if job.template.name == 'nojob':
        moa.ui.fprint("not a Moa job")
        return
    message = ""

    message +="{{bold}}Moa{{reset}} %s " % sysConf.getVersion()
    message += "- template: {{bold}}%s{{reset}}\n" % job.template.name

    message +='"{{bold}}%s{{reset}}"\n' % job.conf.title
    status = _getStatus(job)
    color = {
        'running' : '{{bold}}',
        'success' : '{{green}}',
        'locked' : '{{red}}{{bold}}',
        'error' : '{{red}}{{bold}}',
        'interrupted' : '{{blue}}'}.get(status, '{{bold}}')
    message += "Status: %s%s{{reset}}" % (color, status)        
    moa.ui.fprint(message, f='jinja')

    moa.ui.fprint("\n{{bold}}Configuration{{reset}}:", f='jinja')
    if 'show' in sysConf.commands:
        commandFunction = sysConf.commands['show']['call']
        commandFunction(job, args)
        
def _getStatus(job, silent=False):
    """
    Figure out what the status of this job is

    If it is running -check if the pid corresponds with a moa process
    """
    
    statusFile = os.path.join(job.wd, '.moa', 'status')
    lockFile = os.path.join(job.wd, '.moa', 'lock')
    pidFile = os.path.join(job.wd, '.moa', 'pid')

    l.debug("checking status")
    if os.path.exists(lockFile):
        l.debug("found lockfile")
        return 'locked'

    if not os.path.exists(statusFile):
        l.debug("no statusfile - not doing anything")
        return 'waiting'

    with open(statusFile) as F:
        status = F.read()
        l.debug("reading status file: " + status.strip())
        
    if status != 'running':
        return status

    #if running - check if it is really running 
    otherPid = _getPid(job)
    l.debug("Check if we're really running - should be process id %s" % otherPid)
    if otherPid == None:
        return 'error'
    
    processInfo = moa.utils.getProcessInfo(otherPid)
    if processInfo.get('moa', False):
        return 'running'
    
    #So, this jobs; status says running - but the processInfo
    #disagrees - must be a stale lock
    try:
        if not silent:
            moa.ui.warn("Removing a stale lockfile")
        os.unlink(pidFile)
        _setStatus(job, 'error')
        
    except OSError, e:
        if e.errno == 2:
            #weird - the pid file dissapeared -
            moa.ui.warn("weird - pidfile dissapeared")
            #try again
            return _getStatus(job)
        else:
            raise
        
    return "error"

def _setStatus(job, status):
    l.debug("set job status to %s" % status)
    sysConf.job.status = status
    statusFile = os.path.join(job.wd, '.moa', 'status')
    if LLOG: print 'writing status %s' % status
    with open(statusFile, 'w') as F:
        F.write("%s" % status)

def _setPid(job, pid):
    l.debug("write PID file (%s)" % pid)
    pidFile = os.path.join(job.wd, '.moa', 'pid')
    with open(pidFile, 'w') as F:
        F.write("%s" % pid)

def _removePid(job):
    pidFile = os.path.join(job.wd, '.moa', 'pid')
    try:
        os.unlink(pidFile)
    except OSError, e:
        if e.errno != 2:
            raise
        
def _getPid(job):
    pidFile = os.path.join(job.wd, '.moa', 'pid')
    if not os.path.exists(pidFile):
        return None
    with open(pidFile) as F:
        return int(F.read())

@moa.args.needsJob
@moa.args.command
def kill(job, args):
    """
    Kill a running job.

    This command checks if a job is running. If so - it tries to kill
    it by sending SIGKILL (-9) to the job.
    """
    status = _getStatus(job)
    print status
    if not status == 'running':
        moa.ui.exitError("Job is not running")

    pid = _getPid(job)
    moa.ui.warn("sending a kill signal to process %d" % pid)
    os.kill(pid, signal.SIGKILL)
    status = _getStatus(job, silent=True)
    if status == 'running':
        moa.exitError("Failed to kill this Moa job")
    _removePid(job)
    _setStatus(job, 'interrupted')
    
    
def hook_preRun(): 
    status = _getStatus(sysConf.job)
    if status in ['running', 'paused']:
        moa.ui.exitError("Already running")

    if sysConf.job.isMoa():
        _setPid(sysConf.job, os.getpid())
        _setStatus(sysConf.job, 'running')

def hook_postRun():
    status = 'success'
    if sysConf.rc != 0:
        status = 'error'
    if sysConf.job.isMoa():
        _setStatus(sysConf.job, status)
        _removePid(sysConf.job)

def hook_postInterrupt():
    if sysConf.job.isMoa():
        _setStatus(sysConf.job, 'interrupted')
        _removePid(sysConf.job)

def hook_postError():
    if sysConf.job.isMoa():
        _setStatus(sysConf.job, 'error')
        _removePid(sysConf.job)

@moa.args.needsJob
@moa.args.command
def pause(job, args):
    """
    Pause a running job
    """
    status = _getStatus(job)
    if LLOG: print 'pausing job with status', status
    if status != 'running':
        moa.ui.exitError("Not running")

    pid = _getPid(job)
    print pid
    moa.ui.warn("Pausing job %d" % pid)
    os.kill(pid, 19)
    _setStatus(job, 'paused')

@moa.args.needsJob
@moa.args.command
def resume(job, args):
    """
    Resume a running job
    """
    status = _getStatus(job)
    if LLOG: print 'resuming job with status', status
    if status != 'paused':
        moa.ui.exitError("Not paused")

    pid = _getPid(job)
    moa.ui.warn("Resuming job %d" % pid)
    os.kill(pid, 18)
    _setStatus(job, 'running')

KILLTEST = '''

'''
STATUSTEST = '''
moa status | grep -qi "not a Moa job"
moa simple --np -t test
moa status | grep -qi "template: simple"
moa status | grep -qi "Status: waiting"
moa run 2>/dev/null || true
echo a
moa show
moa status | grep -qi "Status: error"
echo b
moa set process="sleep 0.1"
echo c
moa run
moa status | grep -qi "Status: success"
moa set process="sleep 10"
echo d
moa run --bg
echo c
moa kill
moa status | grep -qi "Status: interrupted"
'''
