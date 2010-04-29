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
import time
import tempfile
import subprocess

from  moa.logger import l
import moa.info
import moa.utils
from moa.exceptions import *

class MOAMAKE:
    """
    A wrapper for running Make

    """
    def __init__(self,
                 wd,
                 target = "",
                 makeArgs = None,
                 makefile = "",
                 background = False,
                 verbose=False,
                 stealth=False,
                 threads=1,
                 captureOut = None,
                 captureErr = None,
                 captureName = 'moa' ):
        """
        @param wd: Working directory
        @type wd: String
        @param target: Makefile target to execute
        @type target: String
        @param makeArgs: Arguments to pass onto Make
        @type makeArgs: list of Strings
        @param verbose: Verbose output
        @type verbose: Boolean
        @param stealth: Run stealthily - do not write moa.success 
        @type stealth: Boolean
        @param captureOut: Capture the output in log files
        @type captureOut: Boolean
        @param captureName: Basename for the log files that will
            capture the output
        @type captureName: String
        @param threads: Number of threads to run Make with
        @type threads: Integer
        """
        
        self.wd = wd
        self.target = target
        self.makefile = makefile
        self.verbose = verbose
        self.stealth = stealth
        self.background = background
        self.threads = threads
        self.captureName = captureName
        self.captureOut = captureOut
        self.captureErr = captureErr

        #for k in self.__dict__.keys():
        #    l.critical("%s %s" % (k, self.__dict__[k]))

        # determine if we need to capture the output
        # if undefined (captureOut == None!).
        # default to True when backgrounding, otherwise
        # not
        if self.captureOut == None:
            if self.background: self.captureOut = True
            else: self.captureOut = False
        if self.captureErr == None:
            if self.background: self.captureErr = True
            else: self.captureErr = False
        
        if makeArgs == None:
            self.makeArgs = []
        else:
            self.makeArgs = makeArgs

        if self.target:
            self.makeArgs.append(self.target)

        #see if we need to run with another makefile
        #that Makefile in the cwd
        if makefile:
            self.makeArgs.append('-f')
            self.makeArgs.append(self.makefile)
            
        # -r make Make not use its default rules
        # mostly aimed at compiling & building software
        if not '-r' in self.makeArgs:
            self.makeArgs.append('-r')
            
        if self.verbose:
            # used inside the moa templates
            os.putenv('MOA_VERBOSE', "-v")
        else:
            # -s keeps make silent
            if not '-s' in self.makeArgs:
                self.makeArgs.append('-s')
                
        # most moa templates do not allow threads, but will use them
        # in handle threads very well
        os.putenv('MOA_THREADS', "%s" % threads)

        #prepare capturing of output
        self.FERR = None
        self.FOUT = None

        self.captureErrName = ""
        self.captureOutName = ""
        
        if self.captureErr:
            #do not want any ANSI colored output
            #l.critical('preparing caperr %s'% self.captureErr)
            os.putenv('MOAANSI', 'no')
            if self.captureName == 'tempfile':
                self.FERR = tempfile.NamedTemporaryFile(
                    delete=False,
                    prefix='tmpMoaErr')
                self.captureErrName = self.FERR.name
            else:
                self.captureErrName = os.path.join(wd, '%s.err' % self.captureName)
                self.FERR = open(self.captureErrName, 'w')

        if self.captureOut:
            if self.captureName == 'tempfile':
                self.FOUT = tempfile.NamedTemporaryFile(
                    delete=False,
                    prefix='tmpMoaOut')
                self.captureOutName = self.FOUT.name
            else:
                self.captureOutName = os.path.join(wd, '%s.out' % self.captureName)
                self.FOUT = open(self.captureOutName, 'w')


    def run(self):
        """
        Start Make
        """

        if self.background:
            # try to fork
            child = os.fork()
            if child != 0:
                # This is the parent thread - return
                return child
            l.debug("Child thread - start executing - start run %s" % child)

        self.runStartTime = time.time()
        
        #remove the last job status
        if not self.stealth:
            if os.path.exists(os.path.join(self.wd, 'moa.success')):
                os.unlink(os.path.join(self.wd, 'moa.success'))
            if os.path.exists(os.path.join(self.wd, 'moa.failed')):
                os.unlink(os.path.join(self.wd, 'moa.failed'))

        l.debug("Starting Make now in %s" % self.wd)
        l.debug(" - with arguments: '%s'" % str(self.makeArgs))
        self.commandLine = " ".join(["make"] + self.makeArgs)
        
        self.p = subprocess.Popen(
            ['make'] + self.makeArgs,
            shell=False,
            cwd = self.wd,
            stdout = self.FOUT,
            stderr = self.FERR)

        if self.FOUT:
            self.FOUT.close()
        if self.FERR:
            self.FERR.close()
            
        l.debug("Make has started with pid %d" % self.p.pid)
        self.pid = self.p.pid
        self.out, self.err = self.p.communicate()
        self.rc = self.p.returncode
        self.runStopTime = time.time()
        
        #write a success or error file
        if not self.stealth:
            if self.rc == 0:
                F = open(os.path.join(self.wd, 'moa.success'), 'w')
                F.write(self._report())
                F.close()
            else:
                F = open(os.path.join(self.wd, 'moa.failed'), 'w')
                F.write(self._report())
                F.close()

        l.debug("Make has finished with rc %d " % self.rc)
        return self.rc

    def _report(self):
        report = "\n".join([
            'Process id: %d' % self.pid,
            'Return code: %d' % self.rc,
            'Command line: %s' % self.commandLine,
            'Target: %s' % self.target,
            'Working directory: %s' % self.wd,
            'Start: %s' % time.asctime(time.localtime(self.runStartTime)),
            'End: %s' % time.asctime(time.localtime(self.runStopTime)),
            'Duration: %.4f sec' % (self.runStopTime - self.runStartTime)]) + "\n"
        
        return report

    def finish(self):
        
        if self.rc == 0:
            l.debug("Succesfully finished make in %s" % (self.wd))
        else:
            if self.verbose:
                l.error("Error running make in %s. Return code %s" % (
                    self.wd, self.rc))
            else:
                l.debug("Error running make in %s. Return code %s" % (
                    self.wd, self.rc))
                
        if self.captureName:
            if self.captureOut: os.unlink(self.captureOutName)
            if self.captureErr: os.unlink(self.captureErrName)

    def getOutput(self):
        """
        Get the output from a moa run
        """
        if not os.path.exists(self.captureOutName):
            return ""
        l.debug("reading output from %s" % self.captureOutName)
        return open(self.captureOutName).read()

    def getError(self):
        """
        Get the stderr of a moa run

        @returns: stderr output of this job (if captured)
        @rtype: string
        """
        if not os.path.exists(self.captureErrName):
            return ""
        l.debug("reading error from %s" % self.captureErrName)
        return open(self.captureErrName).read()

def go(*args, **kwargs):
    """convenience function"""
    job = MOAMAKE(*args, **kwargs)
    rc = job.run()
    return rc

    
def runMakeGetOutput(wd, **kwargs):
    """
    Run runmake, wait for it to finish & return the output -
    we capture the output in a random name (to preven collisions)

    """
    l.debug("runMakeGetOutput in %s kwargs %s" % (wd, kwargs))
    kwargs['background'] = False
    kwargs['captureOut'] = True
    kwargs['captureName'] = 'tempfile'
    job = MOAMAKE(wd, **kwargs)
    job.run()
    output = job.getOutput()
    job.finish()
    return output
