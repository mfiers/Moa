# Copyright 2009, 2010 Mark Fiers, Plant & Food Research
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
'Simple' wrapper around subprocess to execute code
"""

import os
import sys
import time
import tempfile
import subprocess

import moa.logger as l
import moa.utils
from moa.exceptions import *

class Actor:
    
    def __init__(self, wd, 
                 captureOut = False,
                 captureErr = False,
                 captureName = None
                 ):
        """
        @param wd: Working directory
        @type wd: String
        @param cl: command line
        @type cl: List of strings
        @param env: Environment - to be saved to the environment before 
           execution
        @type env: Dict
        @param captureOut: Capture the output in log files
        @type captureOut: Boolean
        @param captureErr: Capture the output in log files
        @type captureErr: Boolean
        @param captureName: Basename for the log files that will
            capture the output
        @type captureName: String
        """        
        self.wd = wd
        
        self.captureName = captureName
        self.captureOut = captureOut
        self.captureErr = captureErr
        
        #prepare capturing of output
        self.FERR = None
        self.FOUT = None
        
        if not captureName:
            if os.path.exists(os.path.join(self.wd, '.moa')):
                base = os.path.join(self.wd, '.moa', 'out')
                if not os.path.exists(base):
                    os.makedirs(base)
            else:
                base = self.wd
                
        captureName = os.path.join(base, 'out.%d' % os.getpid())
        self.captureErrName = "%s.err" % captureName
        self.captureOutName = "%s.out" % captureName        
        
    def setEnv(self, d):
        """
        Setup the environment
        """
        for k in d.keys():
            os.putenv(k, str(d[k]))
            
    def run(self, cl, background = False):
        """
        Start a run
        """        
        if background:
            # try to fork
            child = os.fork()
            if child != 0:
                # This is the parent thread - return
                return child

            l.debug("Child thread - start executing - start run %s" % child)
            
            #no questions asked - we're saving the output
            self.captureOut = True
            self.captureErr = True
        
        return self.run2(cl)
        
    def run2(self, cl):
        """
        Really run 
        """
        self.runStartTime = time.time()
        
        l.debug("Starting actor now in %s" % self.wd)
        l.debug(" - with command line: '%s'" % " ".join(cl))
        
        if self.captureOut:
            self.FOUT = open(self.captureOutName, 'w')
        if self.captureErr:
            self.FERR = open(self.captureErrName, 'w')

        self.p = subprocess.Popen(
            cl, shell=False, cwd = self.wd,
            stdout = self.FOUT, stderr = self.FERR)

        l.debug("execution has started with pid %d" % self.p.pid)            
        self.pid = self.p.pid
        
        self.out, self.err = self.p.communicate()

        self.rc = self.p.returncode
        self.runStopTime = time.time()
        
        if self.captureOut:
            self.FOUT.close()
        if self.captureErr:
            self.FERR.close()
            
        l.debug("Finished execution with rc %d " % self.rc)
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

