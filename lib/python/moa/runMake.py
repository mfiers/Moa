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
moa wrapper for the API 
"""

import os
import sys

import optparse
import subprocess

from  moa.logger import l
from moa import utils

def _startMake(wd, args, verbose = True,
               captureOut = False):
    """
    A function to start Make in a certain directory d with specific args
    
    :param wd: Directory in which to execute make
    :type wd: String
    :param args: Arguments to pass to make
    :type args: String or List of Strings
    :param verbose: Have make be silent or generate lots of output
    :type verbose: Boolean
    :param captureOut: If True the output will be written to moa.out
    and moa.err
    :type captureOut: Boolean    
    """
    l.critical("start execute of make in %s" % wd)
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

def runMake(wd = None, args = [], verbose=True,
            captureOut = False):
    """
    Complete a make run
    """
    if not wd: wd = os.getcwd()
    p = _startMake(wd = wd, args = args, verbose=verbose,
                   captureOut = True)
    (out, err) = p.communicate()
    l.critical("%s" %out)
    l.critical("%s" %err)
    rc = p.returncode
    l.debug("Finished make in %s with return code %s" % (wd, rc))
    return rc

def runMakeAndExit(wd = None, args = [], verbose=True):
    """
    Convenience function - run, report & exit
    """
    l.debug("ji %s %s" % (wd, args))
    rc = runMake(wd=wd, verbose=verbose, args=args)
    sys.exit(rc)


##
## API Command Dispatcher
## 

def execute(d, args = []):
    """
    Execute 'make' in directory d
    """
    __startupMake(d, args)
