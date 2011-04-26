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

import moa.logger as l

def simpleRunner(wd, cl, silent=False):
    """
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """
    
    stst = datetime.datetime.today().strftime("%Y%m%dT%H%M%S")
    outDir = os.path.join(wd, '.moa', 'out', stst)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    SOUT = open(os.path.join(outDir, 'stdout'), 'w')
    SERR = open(os.path.join(outDir, 'stderr'), 'w')    
    l.debug("executing %s" % " ".join(cl))


    if silent:
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
    o = p.stdout.read(); e = p.stderr.read()
    sys.stdout.write(o); sys.stderr.write(e)
    SOUT.write(o); SERR.write(e)
    sys.stdout.flush();     sys.stderr.flush()

    #return returncode
    return p.returncode

def getRecentOutDir(job):
    """
    Return the most recent output directory
    """
    baseDir = os.path.join(job.confDir, 'out')
    if not os.path.exists(baseDir):
        return []
    subDirs = [os.path.join(baseDir, x) for x in os.listdir(baseDir)]
    subDirs = filter(os.path.isdir, subDirs)
    subDirs.sort(key=lambda x: os.path.getmtime(x))
    return subDirs[-1]

def getLastStdout(job):
    """
    Get the last stdout
    """
    outDir = getRecentOutDir(job)
    if not outDir:
        return None
    with open(os.path.join(outDir, 'stdout')) as F:
        return F.read().strip()

def getLastStderr(job):
    """
    Get the last stderr
    """
    outDir = getRecentOutDir(job)
    if not outDir:
        return None
    with open(os.path.join(outDir, 'stderr')) as F:
        return F.read().strip()
