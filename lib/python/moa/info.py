# Copyright 2009 Mark Fiers, Plant & Food Research
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
Functions to retrieve information from Moa directories
"""

import os
import re
import sys
import commands

from moa.logger import l
from moa import runMake
from moa.exceptions import *
import moa.utils
import moa.lock

MOABASE = os.environ["MOABASE"]

def getMoaBase():
    """
    Return the MOABASE
    
        >>> mb = getMoaBase()
        >>> type(mb) == type('string')
        True
        >>> os.path.exists(mb)
        True
        >>> os.path.exists(os.path.join(mb, 'bin', 'moa'))
        True
        
    """
    return MOABASE


def isMoaDir(d):
    """
    Is directory d a 'moa' directory?

        >>> isMoaDir('/')
        False
        >>> demoPath = os.path.join(getMoaBase(), 'demo', 'test')
        >>> isMoaDir(demoPath)
        True
        
    """
    makefile = os.path.join(d, 'Makefile')
    l.debug('isMoaDir: checking %s' % makefile)
    if not os.path.exists(makefile):
        return False
    
    #we could run make, but that is rather slow just to check if a Makefile
    #is a proper Makefile - so, we' quickly reading the Makefile to see if
    #it imports __moaBase.mk. If it does - it's probably a Moa Makefile
    isMoa = False
    
    F = open(os.path.join(d, 'Makefile'))
    for line in F.readlines():
        if 'MOABASE' in line:
            isMoa = True
            break
    F.close()        
    return isMoa

def _checkRunlock(d):
    """
    Check if the runlock file actually points to a proper process

    @returns: If the runlock is valid
    @rtype: boolean
    """
    runlockfile = os.path.join(d, 'moa.runlock')

    #does the file exist?
    if not os.path.exists(runlockfile):
        return False
    
    try:
        with open(runlockfile, 'r') as F:    
            pid = F.read().strip()
            pid = int(pid)
    except IOError, e:
        if e.errno == 2: #file does not exist (anymore?)
            return False
        #other error - raise
        raise
    except ValueError, e:
        #the file does not seem be a proper runlock
        if "invalid literal for int()" in e.message:
            #runlock should contain a PID, i.e. an integer
            l.warning("Erroneous lock file (or so it seems) - removing")
            os.unlink(runlockfile)
            return False
        raise

    
    if not pid:
        os.unlink(runlockfile)
        return False

    l.debug("Checking pid %d" % pid)

    processName = commands.getoutput("ps -p %d -o comm=" % pid)
    if processName != 'make':
        l.warning("Stale lock file (or so it seems) - removing")
        os.unlink(runlockfile)
        return False

    return True



def status(d):
    """
    Returns the status of a directory. It will return a one of the following status messages:

       - notmoa - this is not a moa directory
       - waiting - a moa job, not doing anything
       - success - a moa job, not doing anything, but the last (background) run
          was successfull
       - failed - A moa job, not doing anything, but the last (background) run
          failed
       - running - this is a moa job & currently executing (runlock exists)       
       - locked - this job is locked (i.e. a lock file exists)

           >>> status(P_JOB)
           'waiting'
           >>> moa.utils.removeMoaFiles(P_EMPTY)
           >>> status(P_EMPTY)
           'notmoa'
           >>> status(P_LOCKEDJOB)
           'locked'
       
    """
    if not isMoaDir(d):
        return "notmoa"
    lockfile = os.path.join(d, 'lock')
    successfile = os.path.join(d, 'moa.success')
    failedfile = os.path.join(d, 'moa.failed')
    lockfile = os.path.join(d, 'lock')
    runlockfile = os.path.join(d, 'moa.runlock')
    if _checkRunlock(d):
        return "running"
    if os.path.exists(lockfile):
        return "locked"
    if os.path.exists(successfile):
        return "success"
    if os.path.exists(failedfile):
        return "failed"
    return "waiting"

def template(wd):
    """
    Return the template name of this wd
    """
    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    with open(os.path.join(wd, 'Makefile')) as F:
        for line in F.readlines():
            if 'include $(MOABASE)/template' in line \
               and (not '/template/moa/' in line):
                template = line.strip().split('/')[-1].replace('.mk', '')
                return template

reFindTitle=re.compile(r'title\+?= *(.*?) *$')
def getTitle(wd):
    """
    Return the title of a moa job

    @param wd: directory to get the title of
    @type wd: String
    @returns: The title of the project
    @rtype: String
    @raises NotAMoaDirectory
    """
    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    with open(os.path.join(wd, 'moa.mk')) as F:
        for line in F.readlines():
            m = reFindTitle.match(line)
            if not m: continue
            return  m.groups()[0]

    
def info(wd):
    """
    Retrieve a lot of information on a job

    >>> result = info(P_JOB)
    >>> type(result) == type({})
    True
    >>> result.has_key('moa_targets')
    True
    >>> result.has_key('moa_description')
    True
    >>> try: result2 = info('NOTAMOADIR')
    ... except NotAMoaDirectory: 'ok!'
    'ok!'

    :param wd: Moa directory to retrieve info from
    :type wd: String
    
    :raises NotAMoaDirectory: when wd is not a Moa directory or does
       not exists
    
    """

    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    
    rv = {
        'parameters' : {}
        }

    outBaseName = '.moa.%d' % os.getpid()
    l.debug("using %s" % outBaseName)
    rc = runMake.go(
        wd = wd,
        background=False,
        target='info',
        verbose=False,
        captureOut=True,
        captureOutName = outBaseName)
    out = runMake.getOutput(wd, outBaseName)
    #remove the output files
    moa.utils.removeMoaOutfiles(wd, outBaseName)
    
    outlines = out.split("\n")
    while True:
        if len(outlines) == 0: break
        line = outlines.pop(0).strip()
        if not line: continue

        ls = line.split("\t")
        what = ls[0]
        if len(ls) > 1:
            val = " ".join(ls[1:])
        else:
            val = ""
        
        if what == 'moa_title':
            rv['moa_title'] = val
        elif what == 'moa_description':
            rv[what] = val
        elif what == 'moa_targets':
            rv[what] = val.split()
        elif what == 'parameter':
            parname = None            
            pob = {}
            for v in ls[1:]:
                k,v = v.split('=', 1)
                if k == 'mandatory':
                    if v == 'yes': pob[k] = True
                    else: pob[k] = False
                elif k == 'name':
                    parname=v
                elif k in ['value', 'help', 'default', 'type',
                           'category', 'cardinality']:
                    pob[k] = v
                elif k == 'allowed':
                    pob[k] = v.split()
                else:
                    raise ("invalid key in %s" %line)
            if pob.get('cardinality') == 'many':
                pob['value'] = pob.get('value').split()
            rv['parameters'][parname] = pob
    return rv


    
    



