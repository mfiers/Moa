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
from moa.sysConf import sysConf

LLOG = False
STATUS = 'unknown'

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['status'] = {
        'desc' : 'Show the state of the current job',
        'log' : False,
        'needsJob' : True,
        'call' : status,
        'unittest' : STATUSTEST
        }

    data['commands']['kill'] = {
        'desc' : 'Kill a job',
        'log' : True,
        'needsJob' : True,
        'call' : kill,
        'unittest' : KILLTEST,
        }
    
    data['commands']['pause'] = {
        'desc' : 'Pause a job',
        'log' : True,
        'needsJob' : True,
        'call' : pause,
        }
    data['commands']['resume'] = {
        'desc' : 'Resume a job',
        'log' : True,
        'needsJob' : True,
        'call' : resume,
        }

    
def status(job):
    """
    **moa status** - print out a short status status message

    Usage::

       moa status       
    """
    if job.template.name == 'nojob':
        moa.ui.fprint("not a Moa job")
        return
    message = ""

    message +="{{bold}}Moa{{reset}} %s. " % sysConf.getVersion()
    message += "template: {{bold}}%s{{reset}}. " % job.template.name
    
    status = _getStatus(job)
    color = {
        'running' : '{{bold}}',
        'success' : '{{green}}',
        'error' : '{{red}}{{bold}}',
        'interrupted' : '{{blue}}'}.get(status, '')
    message += "Status: %s%s{{reset}}" % (color, status)        
    moa.ui.fprint(message, f='jinja')
    
        
def _getStatus(job, silent=False):
    """
    Figure out what the status of this job is

    If it is running -check if the pid corresponds with a moa process
    """
    
    statusFile = os.path.join(job.wd, '.moa', 'status')
    pidFile = os.path.join(job.wd, '.moa', 'pid')
    if not os.path.exists(statusFile):
        return 'waiting'

    with open(statusFile) as F:
        status = F.read()
        
    if status != 'running':
        return status

    #if running - check if it is really running    
    otherPid = _getPid(job)
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
    statusFile = os.path.join(job.wd, '.moa', 'status')
    if LLOG: print 'writing status %s' % status
    with open(statusFile, 'w') as F:
        F.write("%s" % status)

def _setPid(job, pid):
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

#def background_exit(data):
#    """
#3    Rewrite the pid file to contain the child pid id
#3    """
#    _setPid(data.job, data.childPid)
#    if LLOG: print 'local parent exit'

def kill(job):
    """
    See if a job is running, if so - kill it
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
    
    
def preRun(data): 
    status = _getStatus(data.job)
    if status in ['running', 'paused']:
        moa.ui.exitError("Already running")

    if data.job.isMoa():
        _setPid(data.job, os.getpid())
        _setStatus(data.job, 'running')

def postRun(data):
    status = 'success'
    if data.rc != 0:
        status = 'error'
    if data.job.isMoa():
        _setStatus(data.job, status)
        _removePid(data.job)

def postInterrupt(data):
    if data.job.isMoa():
        _setStatus(data.job, 'interrupted')
        _removePid(data.job)

def postError(data):
    if data.job.isMoa():
        _setStatus(data.job, 'error')
        _removePid(data.job)



def pause(job):
    """
    pause a running job
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

def resume(job):
    """
    pause a running job
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
moa run >/dev/null 2>/dev/null || true
echo a
moa status | grep -qi "Status: error"
echo b
moa set process="sleep 0.5"
echo c
moa run
moa status | grep -qi "Status: success"
moa run --bg >/dev/null
echo c
moa kill >/dev/null
moa status | grep -qi "Status: interrupted"
'''
