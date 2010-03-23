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

#@moa.utils.profiler2
def _startMake(wd,
               makeArgs = [],
               verbose = True,
               captureOut = False,
               extraMakeParameters = [],
               captureOutName = 'moa'):
    """
    Start Make

    A function that starts Make (but does not wait for it to finish)
    in directory `wd`
    
    @param wd: Directory in which to execute make
    @type wd: String
    @param makeArgs: Arguments to pass to make
    @type makeArgs: String or List of Strings
    @param verbose: Have make be silent or generate lots of output
    @type verbose: Boolean
    @param captureOut: If True the output will be written to moa.out
      and moa.err
    @type captureOut: Boolean
    @param extraMakeParameters: Extra parameters to pass to make (such as -B)
    @type extraMakeParameters: List of Strings
    @param captureOutName: Basename of the file where the moa output
        will be captured.
    @type captureOutName: String
    @raises NotMoaDirectory: If ``wd`` is not a Moa directory    
    """

    l.debug("attempting to start make in %s" % wd)     
    
    if captureOut:
        FOUT = open(os.path.join(wd, '%s.out' % captureOutName), 'w')
        FERR = open(os.path.join(wd, '%s.err' % captureOutName), 'w')
        os.putenv('MOAANSI', 'no')
    else:
        FOUT = None
        FERR = None
        
    makeArgs.insert(0, 'make')
    l.debug("RUNNING MAKE %s" % " ".join(makeArgs))
    p = subprocess.Popen(
        makeArgs,
        shell=False,
        cwd = wd,
        stdout = FOUT,
        stderr = FERR)
    return p


def _runMake(wd = None, target = "", makeArgs = [],
             verbose=True, captureOut = False, threads=1,
             extraMakeParameters= [],
             captureOutName='moa'
             ):

    """
    Actually run make
    
    @param wd: Working directory
    @type wd: String
    @param target: Makefile target to execute
    @type target: String
    @param makeArgs: Arguments to pass onto Make
    @type makeArgs: List of Strings
    @param verbose: Verbose output
    @type verbose: Boolean
    @param extraMakeParameters: Extra parameters to pass to make (such as -B)
    @type extraMakeParameters: List of Strings
    @param captureOut: Capture the output in log files
    @type captureOut: Boolean
    @param captureOutName: Basename for the log files that will
      capture the output
    @type captureOutName: String
    @param threads: Number of threads to run Make with
    @type threads: Integer
    
    """
    
    if not moa.info.isMoaDir(wd):
        raise NotAMoaDirectory(wd)

    #prepare arguments & environment
    l.debug("Incoming make parameters %s" % makeArgs)
    if type(makeArgs) == type("str"):
        makeArgs = makeArgs.split()

    l.debug("Extra parameters for make %s" % extraMakeParameters)
    for extraParam in extraMakeParameters:
        makeArgs.insert(0,extraParam)

    #we do not want all default rules (since we're not compiling software)
    makeArgs.insert(0, '-r')

    if verbose:
        os.putenv('MOA_VERBOSE', "-v")
    else:
        makeArgs.insert(0, '-s')

    os.putenv('MOA_MAKE_PARAMETERS', " ".join(makeArgs))
    os.putenv('MOA_THREADS', "%s" % threads)
    l.debug("moa make parameters: %s" % " ".join(makeArgs))
        
    if target:
        makeArgs.insert(0, target)

    p = _startMake(wd = wd,
                   makeArgs = makeArgs,
                   verbose=verbose,
                   extraMakeParameters = extraMakeParameters,
                   captureOut = captureOut,
                   captureOutName=captureOutName)
    out,err = p.communicate()
    
    rc = p.returncode
    if rc == 0:
        l.debug("Succesfully finished make in %s" % (wd))
    else:
        l.debug("Error running make in %s. Return code %s" % (wd, rc))
    return rc

def go(wd = None,
       target = "",
       makeArgs = [],
       extraMakeParameters=[],
       verbose=True,
       threads=1,
       background = False,
       captureOut = None,
       captureOutName='moa',
       exitWhenDone=False ):    
    """
    Run Make
    
    @param captureOut: Capture the output in log files
    @type captureOut: Boolean
    @param extraMakeParameters: Extra parameters to pass to Make
    @type extraMakeParameters: List of Strings
    @param captureOutName: Basename for the log files that will
      capture the output
    @type captureOutName: String
    
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
            l.debug("Parent thread - finish")
            return True
        l.debug("Child (pid=%d). Start make" % child)

    # Unless specified otherwise, just write all output
    # to the terminal
    if captureOut == None:
        captureOut = False

    l.debug("starting _runMake with target '%s', args %s " % (
            target, makeArgs))
    rc = _runMake(wd = wd,
                  target=target,
                  makeArgs = makeArgs,
                  extraMakeParameters = extraMakeParameters,
                  verbose=verbose,
                  threads = threads,
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
    
def runMakeGetOutput(*args, **kwargs):
    """
    Run runmake, wait for it to finish & return the output -
    we capture the output in a random name (to preven collisions)

    """
    outName = 'moa.%d' % os.getpid()
    l.debug("runMakeGetOutput args %s kwargs %s" % (args, kwargs))
    if not kwargs.has_key('wd'):
        wd = os.getcwd()
        kwargs['wd'] = wd
    else: 
        wd = kwargs['wd']

    kwargs['captureOut'] = True
    kwargs['captureOutName'] = outName
    kwargs['background'] = False
    go(*args, **kwargs)
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

