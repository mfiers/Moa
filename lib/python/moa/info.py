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
Directory info utilities
"""

import os
import re
import sys

from moa.logger import l
from moa import dispatcher
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

    if not os.path.exists(os.path.join(d, 'Makefile')):
        return False
    
    #we could run make, but that is rather slow just to check if a Makefile
    #is a proper Makefile - so, we' quickly reading the Makefile to see if
    #it imports __moaBase.mk. If it does - it's probably a Moa Makefile
    isMoa = False
    
    F = open(os.path.join(d, 'Makefile'))
    for l in F.readlines():
        if '$(MOABASE)' in l:
            isMoa = True
            break
    F.close()        
    return isMoa

def isLocked(d):
    """
    Is this directory locked?

        >>> result = isLocked(TESTPATH)
        >>> type(result) == type(True)
        True
        >>> moa.lock.lockJob(TESTPATH)
        >>> isLocked(TESTPATH)
        True
        >>> moa.lock.unlockJob(TESTPATH)
        >>> isLocked(TESTPATH)
        False
        >>> try: isLocked(NOTMOADIR)
        ... except NotAMoaDirectory:
        ...   'Fine'
        'Fine'
        
    """    
    if not isMoaDir(d):
        raise NotAMoaDirectory(d)

    if os.path.exists(os.path.join(d, 'lock')):
        return True
    return False
    

def info(d):
    """
    Retrieve a lot of information on a job

        >>> result = info(TESTPATH)
        >>> type(result) == type({})
        True

    """


    rv = {
        'parameters' : {}

        }
    rc, out, err = dispatcher.runMake(directory = d, args='info', catchout=True)

    if rc != 0:
        print err
        raise('Error running make %d' % rc)

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

    
    



