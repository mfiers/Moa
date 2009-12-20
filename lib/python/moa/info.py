#!/usr/bin/env python
# 
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
__docformat__ = "restructuredtext en"


import os
import re
import sys

from moa.logger import l
from moa import runMake
from moa.exceptions import *
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

def status(d):
    """
    Returns the status of a directory. It will return a one of the following status messages:

       - notmoa - this is not a moa directory
       - waiting - a moa job, not doing anything
       - running - this is a moa job & currently executing (runlock exists)       
       - locked - this job is locked (i.e. a lock file exists)

           >>> status(TESTPATH)
           'waiting'
           >>> status(NOTMOADIR)
           'notmoa'
           >>> status(LOCKEDMOADIR)
           'locked'
       
    """
    if not isMoaDir(d):
        return "notmoa"
    lockfile = os.path.join(d, 'lock')
    runlockfile = os.path.join(d, 'moa.runlock')
    if os.path.exists(runlockfile):
        return "running"
    if os.path.exists(lockfile):
        return "locked"
    return "waiting"
    
def info(wd):
    """
    Retrieve a lot of information on a job

    >>> result = info(TESTPATH)
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
    
    out = \
        runMake.runMakeGetOutput(wd = wd, args='info')

    outlines = out.split("\n")
    while True:
        if len(outlines) == 0: break
        line = outlines.pop(0).strip()
        if not line: continue

        ls = line.split("\t")
        what = ls[0]
        if len(ls) > 1:
            val = ls[1]
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


    
    



