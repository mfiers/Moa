# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.actor
---------

'Simple' wrapper around subprocess to execute code
"""

import os
import sys
import fcntl
import datetime
import subprocess

import moa.ui
import moa.logger as l
from moa.sysConf import sysConf


def getRunner():    
    actorId = getattr(sysConf.options, 'actorId', 'default')
    if not actorId: actorId = 'default'
    if not sysConf.actor.actors.has_key(actorId):
        moa.ui.exitError("Invalid actor id: %s" % actorId)
    l.debug("Actor: %s" % actorId)
    return sysConf.actor.actors[actorId]

def simpleRunner(wd, cl, conf={}, **kwargs):
    """
    Don't think - just run - here & now

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """
    

    #stst = datetime.datetime.today().strftime("%Y%m%dT%H%M%S")
    #outDir = os.path.join(wd, '.moa', 'out', stst)
    outDir = os.path.join(wd, '.moa', 'log.latest')
    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    #dump the configuration in the environment
    for k in conf:
        # to prevent collusion, prepend all env variables
        # with 'moa_'
        outk = 'moa_' + k
        v = conf[k]
        if isinstance(v, list):
            os.putenv(outk, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(outk, str(v))

    SOUT = open(os.path.join(outDir, 'stdout'), 'a')
    SERR = open(os.path.join(outDir, 'stderr'), 'a')    
    l.debug("executing %s" % " ".join(cl))
    
    if sysConf.options.silent or sysConf.force_silent:
        p = subprocess.Popen(cl, cwd = wd, stdout=SOUT, stderr=SERR)
        p.communicate()
        return p.returncode

    #non silent - split output to the output files &
    #stdout/stderr
    p = subprocess.Popen(
        cl, cwd = wd, shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    #make the file handles non-blocking
    fdout = p.stdout.fileno()
    flout = fcntl.fcntl(fdout, fcntl.F_GETFL)
    fcntl.fcntl(fdout, fcntl.F_SETFL, flout | os.O_NONBLOCK)

    fderr = p.stderr.fileno()
    flerr = fcntl.fcntl(fderr, fcntl.F_GETFL)
    fcntl.fcntl(fderr, fcntl.F_SETFL, flerr | os.O_NONBLOCK)

    #now start polling & output the data
    while True:
        if p.poll() != None: break
        try:
            o = p.stdout.read(1024)
            sys.stdout.write(o)
            SOUT.write(o)
        except IOError:
            pass
        try:
            e = p.stderr.read(1024)
            sys.stderr.write(e)
            SERR.write(e)
        except IOError:
            pass

        sys.stdout.flush(); sys.stderr.flush()
        
    #make sure that nothing is left
    try:
        o = p.stdout.read(); 
        sys.stdout.write(o)
        SOUT.write(o);
    except IOError:
        pass

    try:
        e = p.stderr.read()
        sys.stderr.write(e)
        SERR.write(e)
    except IOError:
        pass

    sys.stdout.flush()    
    sys.stderr.flush()

    #return returncode
    return p.returncode


def getRecentOutDir(job):
    """
    Return the most recent output directory
    """
    baseDir = os.path.join(job.confDir, 'log.latest')
    if not os.path.exists(baseDir):
        return None
    #subDirs = [os.path.join(baseDir, x) for x in os.listdir(baseDir)]
    #subDirs = filter(os.path.isdir, subDirs)
    #subDirs.sort(key=lambda x: os.path.getmtime(x))
    return baseDir


def getLastStdout(job):
    """
    Get the last stdout
    """
    outDir = getRecentOutDir(job)
    if not outDir:
        return None
    outFile = os.path.join(outDir, 'stdout')
    if not os.path.exists(outFile):
        return None
    with open(outFile) as F:
        return F.read().strip()

def getLastStderr(job):
    """
    Get the last stderr
    """
    outDir = getRecentOutDir(job)
    if not outDir:
        return None
    errFile = os.path.join(outDir, 'stderr')
    if not os.path.exists(errFile):
        return None
    with open(errFile) as F:
        return F.read().strip()

#set up some actor data in the sysConf
sysConf.actor = {}
sysConf.actor.actors = {
    'default' : simpleRunner
    }
