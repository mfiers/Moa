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

def _runMake(wd,
             target = "",
             makeArgs = None,
             makefile = "",
             verbose=True,
             threads=1,
             captureOut = False,
             captureErr = False,
             captureOutName='moa'
             ):
    """
    Actually run make
    
    @param wd: Working directory
    @type wd: String
    @param target: Makefile target to execute
    @type target: String
    @param makeArgs: Arguments to pass onto Make
    @type makeArgs: set of Strings
    @param verbose: Verbose output
    @type verbose: Boolean
    @param captureOut: Capture the output in log files
    @type captureOut: Boolean
    @param captureOutName: Basename for the log files that will
      capture the output
    @type captureOutName: String
    @param threads: Number of threads to run Make with
    @type threads: Integer
    
    """
    
    if not makeArgs:
        makeArgs = set()

    if makefile:
        l.debug("executing makefile %s" % makefile)
        makeArgs.add('-f %s' % makefile)
        
    # prepare arguments & environment
    # we do not want all default rules (since we're not compiling
    # software)
    makeArgs.add('-r')

    if verbose:
        # used inside the moa templates
        os.putenv('MOA_VERBOSE', "-v")
    else:
        # -s keeps make silent
        makeArgs.add('-s')

    # most moa templates do not allow threads, but will use them
    # in handle threads very well
    os.putenv('MOA_THREADS', "%s" % threads)
        
    if target: makeArgs.add(target)

    FERR = None
    FOUT = None
    
    if captureErr:
        FERR = open(os.path.join(wd, '%s.err' % captureOutName), 'w')
        os.putenv('MOAANSI', 'no')
    if captureOut:
        FOUT = open(os.path.join(wd, '%s.out' % captureOutName), 'w')

           
    l.debug("Starting Make now in %s" % wd)
    l.debug(" - with arguments: '%s'" % " ".join(makeArgs))
    p = subprocess.Popen(
        ['make'] + " ".join(list(makeArgs)).split(),
        shell=False,
        cwd = wd,
        stdout = FOUT,
        stderr = FERR)

    out,err = p.communicate()
    
    rc = p.returncode
    if rc == 0:
        l.debug("Succesfully finished make in %s" % (wd))
    else:
        if verbose:
            l.error("Error running make in %s. Return code %s" % (wd, rc))
        else:
            l.debug("Error running make in %s. Return code %s" % (wd, rc))
    return rc

# deprecated function name
#def go(*args, **kwargs):
#    runMake(*args, **kwargs)

def go(wd = None,
       target = "",
       makeArgs = set(),
       makefile = "",
       verbose=True,
       threads=1,
       background = False,
       captureOut = None,
       captureErr = None,
       captureOutName='moa',
       exitWhenDone=False ):    
    """
    Run Make
    
    @param captureOut: Capture the output in log files
    @type captureOut: Boolean
    @param captureOutName: Basename for the log files that will
      capture the output
    @type captureOutName: String
    
    """
    if not wd:
        l.warning("runMake needs a directory")
        sys.exit(-1)
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
            l.debug("Parent thread - finish")
            return True
        l.debug("Child (pid=%d). Start make" % child)

    # Unless specified otherwise, just write all output
    # to the terminal
    if captureOut == None:
        captureOut = False

    rc = _runMake(wd = wd,
                  target=target,
                  makeArgs = makeArgs,
                  makefile = makefile,
                  verbose=verbose,
                  threads = threads,
                  captureErr = captureErr,
                  captureOut = captureOut,
                  captureOutName = captureOutName )

    if background:
        if rc == 0:
            F = open(os.path.join(wd, 'moa.success'), 'w')
            F.write("%s" % rc)
            F.close()
        else:
            F = open(os.path.join(wd, 'moa.failed'), 'w')
            F.write("%s" % rc)
            F.close()
    else:            
        return rc
        
    if exitWhenDone:
        sys.exit(rc)
    
def runMakeGetOutput(wd, **kwargs):
    """
    Run runmake, wait for it to finish & return the output -
    we capture the output in a random name (to preven collisions)

    """
    outName = 'moa.%d' % os.getpid()
    l.debug("runMakeGetOutput in %s kwargs %s" % (wd, kwargs))

    kwargs['captureOut'] = True
    kwargs['captureOutName'] = outName
    kwargs['background'] = False
    go(wd, **kwargs)
    output = getOutput(wd, outName)
    moa.utils.removeMoaOutfiles(wd, outName)
    return output

def getOutput(wd, outName='moa'):
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

    @param wd: the Moa directory
    @type wd: String
    @param outName: Basename of the output to retrieve
    @type outName: String
    """
    outfile = os.path.join(wd, '%s.out' % outName)
    if not os.path.exists(outfile):
        return ""    
    return open(outfile).read()

def getError(wd, outName='moa'):
    """
    Get the stderr of a moa run

    >>> F = open(os.path.join(P_EMPTY, 'moa.err'),'w')
    >>> F.write('tsterr')
    >>> F.close()
    >>> getError(P_EMPTY) == 'tsterr'
    True

    @param wd: the Moa directory
    @type wd: String
    @param outName: Basename of the output to retrieve
    @type outName: String
    """
    errfile = os.path.join(wd, '%s.err' % outName)
    if not os.path.exists(errfile):
        return ""    
    return open(errfile).read()

