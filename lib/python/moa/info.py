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


def isMoa(d):
    """ is directory d a 'moa' directory? """

    if not os.path.exists(os.path.join(d, 'Makefile')):
        return False
    
    #we could run make, but that is rather slow just to check if a Makefile
    #is a proper Makefile - so, we' quickly reading the Makefile to see if
    #it imports __moaBase.mk. If it does - it's probably a Moa Makefile

    F = open(os.path.join(d, 'Makefile'))
    for l in F.readlines():
        if '__moaBase' in l:
            isMoa = True
            break
    F.close()
        
    return isMoa

def info(d):
    """ Retrieve a lot of information """
    rv = {'parameters' : {}}
    rc, out, err = dispatcher.runMake(directory = d, args='info', catchOut=True)
    if rc != 0:
        print err
        raise('Error running make %d' % rc)
    
    for line in out.split("\n"):
        if not line: continue
        ls = line.split("\t")
        what = ls[0]
        if what == 'moa_title':
            rv['moa_title'] = ls[1]
        elif what == 'moa_description':
            rv[what] = ls[1]
        elif what == 'moa_targets':
            rv[what] = ls[1].split()
        elif what == 'parameter':
            pob = {}
            if ls[1] == 'required':
                pob['mandatory'] = True
            else:
                pob['mandatory'] = False
            pob['type'] = ls[2]
            pob['value'] = ls[3]
            pob['description'] = ls[4]            
            rv['parameters'][ls[1]] = pob

        

    return rv

    
    



