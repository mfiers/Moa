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
import moa.utils
from moa.exceptions import *

def _startMake(wd, makeArgs, verbose = True,
               captureOut = False):
    """
    Start Make

    A function that starts Make (but does not wait for it to finish)
    in directory `wd`
    
    :param wd: Directory in which to execute make
    :type wd: String
    :param makeArgs: Arguments to pass to make
    :type makeArgs: String or List of Strings
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

    if type(makeArgs) == type("str"):
        makeArgs = makeArgs.split()

    makeArgs.insert(0, '-r')
    
    if not verbose:
        makeArgs.insert(0, '-s')

    if captureOut:
        FOUT = open(os.path.join(wd, 'moa.out'), 'w')
        FERR = open(os.path.join(wd, 'moa.err'), 'w')
        os.putenv('MOAANSI', 'no')
    else:
        FOUT = None
        FERR = None
        os.putenv('MOAANSI', 'yes')
        
    makeArgs.insert(0, 'make')
    p = subprocess.Popen(
        makeArgs,
        shell=False,
        cwd = wd,
        stdout = FOUT,
        stderr = FERR)
    return p


def _runMake(wd = None, target = "", makeArgs = [],
             verbose=True, captureOut = False, threads=1):

    """
    Actually run make
    """
    
    os.putenv('MOA_THREADS', "%s" % threads)    
    if verbose:
        os.putenv('MOA_VERBOSE', "-v")
        
    if target:
        makeArgs.insert(0, target)

    p = _startMake(wd = wd, makeArgs = makeArgs, verbose=verbose,
                   captureOut = captureOut)
    out,err = p.communicate()
    
    rc = p.returncode
    if rc == 0:
        l.debug("Succesfully finished make in %s" % (wd))
    else:
        l.debug("Error running make in %s. Return code %s" % (wd, rc))
    return rc

def go(wd = None, target = "", makeArgs = [],
       verbose=True, threads=1, background = False,
       captureOut = None, exitWhenDone=False):
    """
    Run Make
    """
    if not wd:
        wd = os.getcwd()

    if background:
        
        # Unless defined otherwise, write the output to
        # moa.out and moa.err when backgrounding
        if captureOut == None: captureOut = True

        if os.path.exists(os.path.join(wd, 'moa.success')):
            os.unlink(os.path.join(wd, 'moa.success'))
        if os.path.exists(os.path.join(wd, 'moa.failed')):
            os.unlink(os.path.join(wd, 'moa.failed'))
        # try to fork
        child = os.fork()
        if child != 0:
            l.debug("Parent: return & be done with it")
            return True
        l.debug("Child (pid=%d). Start make" % child)

    # Unless specified otherwise, just write all output
    # to the terminal
    if captureOut == None:
        captureOut = False
        
    rc = _runMake(wd = wd,
             target=target,
             makeArgs = makeArgs,
             verbose=verbose,
             threads = threads,
             captureOut = captureOut)

    if background:
        if rc == 0:
            F = open(os.path.join(wd, 'moa.success'), 'w')
            F.write("%s" % rc)
            F.close()
        else:
            F = open(os.path.join(wd, 'moa.failed'), 'w')
            F.write("%s" % rc)
            F.close()
     
        
    if exitWhenDone:
        sys.exit(rc)
    
def runMakeGetOutput(*args, **kwargs):
    """
    Run runmake, wait for it to finish & return the output
    """
    wd = kwargs['wd']
    kwargs['captureOut'] = True
    kwargs['background'] = False
    runMake(*args, **kwargs)
    return getOutput(wd)

def getOutput(wd):
    """
    Get the output from a moa run

    >>> moa.utils.removeMoaFiles(P_EMPTY)
    >>> F = open(os.path.join(P_EMPTY, 'moa.out'),'w')
    >>> F.write('tst')
    >>> F.close()
    >>> getOutput(P_EMPTY) == 'tst'
    True
    >>> moa.utils.removeMoaFiles(P_EMPTY)
    >>> getOutput(P_EMPTY) == ''
    True

    :param wd: the Moa directory
    :type wd: String

    """
    outfile = os.path.join(wd, 'moa.out')
    if not os.path.exists(outfile):
        return ""    
    return open(outfile).read()

def getError(wd):
    """
    Get the stderr of a moa run

    >>> F = open(os.path.join(P_EMPTY, 'moa.err'),'w')
    >>> F.write('tsterr')
    >>> F.close()
    >>> getError(P_EMPTY) == 'tsterr'
    True

    :param wd: the Moa directory
    :type wd: String

    """
    errfile = os.path.join(wd, 'moa.err')
    if not os.path.exists(errfile):
        return ""    
    return open(errfile).read()

