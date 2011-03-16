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
import datetime
import subprocess

import moa.logger as l

def simpleRunner(job, cl):
    """
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """
    
    stst = datetime.datetime.today().strftime("%Y%m%dT%H%M%S")
    outDir = os.path.join(job.confDir, 'out', stst)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    STDOUT = open(os.path.join(outDir, 'stdout'), 'w')
    STDERR = open(os.path.join(outDir, 'stderr'), 'w')
    l.debug("executing %s" % " ".join(cl))
    sp = subprocess.Popen(cl, cwd = job.wd,
                          stdout=STDOUT, stderr=STDERR)
    sp.communicate()
    return sp.returncode

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
