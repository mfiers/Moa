# Copyright 2009, 2010 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
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
