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
Run GNU Make
"""

import os
import sys

import optparse
import subprocess

from  moa.logger import l
import moa.info
from moa.exceptions import *

def _startMake(wd, args, verbose = True,
               captureOut = False):
    """
    Start Make

    A function that starts Make (but does not wait for it to finish)
    in directory `wd`
    
    :param wd: Directory in which to execute make
    :type wd: String
    :param args: Arguments to pass to make
    :type args: String or List of Strings
    :param verbose: Have make be silent or generate lots of output
    :type verbose: Boolean
    :param captureOut: If True the output will be written to moa.out
    and moa.err
    :type captureOut: Boolean
    :raises NotMoaDirectory: If ``wd`` is not a Moa directory    
    """

    l.debug("attempting to start make in %s" % wd)

    if not moa.info.isMoaDir(wd):
        raise NotAMoaDirectory(wd)

    if type(args) == type("str"):
        args = args.split()

    args.insert(0, '-r')
    if not verbose:
        args.insert(0, '-s')

    if captureOut:
        FOUT = open(os.path.join(wd, 'moa.out'), 'a')
        FERR = open(os.path.join(wd, 'moa.err'), 'a')
        os.putenv('MOAANSI', 'no')
    else:
        FOUT = None
        FERR = None

        os.putenv('MOAANSI', 'yes')
        
    args.insert(0, 'make')
    p = subprocess.Popen(
        args,
        shell=False,
        cwd = wd,
        stdout = FOUT,
        stderr = FERR)
    return p

def runMake(wd = None, args = [], verbose=True, captureOut = False):
    """
    Run Make and wait for it to finish
    """    
    if not wd: wd = os.getcwd()
    try:
        p = _startMake(wd = wd, args = args, verbose=verbose,
                       captureOut = captureOut)
    except NotAMoaDirectory:
        l.critical("Attempt to execute Moa in a non-moa directory")
        sys.exit(1)        
        
    p.communicate()
    rc = p.returncode
    l.debug("Finished make in %s with return code %s" % (wd, rc))
    return rc

def runMakeGetOutput(wd = None, args = [], verbose=True):
    """
    Run Make and wait for it to finish
    """    
    if not wd: wd = os.getcwd()
    try:
        p = _startMake(wd = wd, args = args, verbose=verbose, captureOut = True)
    except NotAMoaDirectory:
        l.critical("Attempt to execute Moa in a non-moa directory")
        sys.exit(1)        
        
    p.communicate()
    rc = p.returncode
    if rc == 0:
        l.debug("Finished make in %s with return code %s" % (wd, rc))
    else:
        l.critical("Finished make in %s with non zero rc %s" % (wd, rc))
        sys.exit(rc)

    output = open(os.path.join(wd, 'moa.out')).read()
    return output

def runMakeAndExit(wd = None, args = [], verbose=True):
    """
    Convenience function - run, report & exit
    """
    l.debug("ji %s %s" % (wd, args))
    try:
        rc = runMake(wd=wd, verbose=verbose, args=args)
    except NotAMoaDirectory:
        l.critical("Attempt to execute Moa in a non-moa directory")
        sys.exit(1)        
    sys.exit(rc)


##
## API Command Dispatcher
## 

def execute(d, args = []):
    """
    Execute 'make' in directory d
    """
    __startupMake(d, args)
