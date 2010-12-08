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
moa.actor
---------

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
    """
    A class that standardizes a number of operations around execution
    in the Moa context.
    
    :param wd: Working directory
    :type wd: String
    """
    def __init__(self, wd):
        
        self.wd = wd
        self.sendOutTo = 'stdout'
        self.sendErrTo = 'stderr'
        self.out = ''
        self.err = ''
        self.saveName = os.path.join(wd, 'moa')
        
                
    def setSaveName(self, name):
        self.saveName = name
   
    def setOut(self, to):
        """
        Determine where to send the output. Three possibilities:
        * file (depends on setSaveName)
        * pipe (can be retrieved from the actor.out string)
        * stdout (print to stdout)
        """
        if to == 'file':
            self.sendOutTo = 'file'
        elif to == 'pipe':
            self.sendOutTo = 'pipe'
        else:
            self.sendOutTo = 'stdout'
            
    def setErr(self, to):
        """
        Determine where to send the stderr. Three possibilities:
        * file (depends on setSaveName)
        * pipe (can be retrieved from the actor.err string)
        * stderr (print to stderr)
        """
        if to == 'file':
            self.sendErrTo = 'file'
        elif to == 'pipe':
            self.sendErrTo = 'pipe'
        else:
            self.sendErrTo = 'stderr'
                                
    def setEnv(self, d):
        """
        Setup the environment

        :param d: The data to transfer to the environment
        :type d: dict
        """
        for k in d.keys():
            os.putenv(k, str(d[k]))
            
    def run(self, cl):
        """
        Actually run

        :param cl: The command to execute, for example: `['ls', '/tmp']`            
        :type cl: list of strings        
        :returns: return code of the job
        :rtype: integer
        
        """   
        self.runStartTime = time.time()
        
        l.debug("Starting actor now in %s" % self.wd)
        l.debug(" - with command line: '%s'" % " ".join(cl))
        
        if self.sendOutTo == 'file':
            FOUT = open('%s.out' % self.saveName, 'a')
        elif self.sendOutTo == 'pipe':
            FOUT = subprocess.PIPE
        else:
            FOUT = None

        if self.sendErrTo == 'file':
            FERR = open('%s.err' % self.saveName, 'a')
        elif self.sendErrTo == 'pipe':
            FERR = subprocess.PIPE
        else:
            FERR = None        

        self.p = subprocess.Popen(
            cl, shell=False, cwd = self.wd,
            stdout = FOUT, stderr = FERR)

        l.debug("execution has started with pid %d" % self.p.pid)            
        self.pid = self.p.pid
        
        self.out, self.err = self.p.communicate()

        self.rc = self.p.returncode
        self.runStopTime = time.time()

        if self.sendOutTo == 'file':
            FOUT.close()
        if self.sendErrTo == 'file':
            FERR.close()
                    
        l.debug("Finished execution with rc %d " % self.rc)
        return self.rc

    # def _report(self):
    #     report = "\n".join([
    #         'Process id: %d' % self.pid,
    #         'Return code: %d' % self.rc,
    #         'Command line: %s' % self.commandLine,
    #         'Target: %s' % self.target,
    #         'Working directory: %s' % self.wd,
    #         'Start: %s' % time.asctime(time.localtime(self.runStartTime)),
    #         'End: %s' % time.asctime(time.localtime(self.runStopTime)),
    #         'Duration: %.4f sec' % (self.runStopTime - self.runStartTime)]) + "\n"
        
    #     return report

    # def finish(self):
        
    #     if self.rc == 0:
    #         l.debug("Succesfully finished make in %s" % (self.wd))
    #     else:
    #         if self.verbose:
    #             l.error("Error running make in %s. Return code %s" % (
    #                 self.wd, self.rc))
    #         else:
    #             l.debug("Error running make in %s. Return code %s" % (
    #                 self.wd, self.rc))
                
    #     if self.captureName:
    #         if self.captureOut: os.unlink(self.captureOutName)
    #         if self.captureErr: os.unlink(self.captureErrName)

    # def getOutput(self):
    #     """
    #     Get the output from a moa run
    #     """
    #     if not os.path.exists(self.captureOutName):
    #         return ""
    #     l.debug("reading output from %s" % self.captureOutName)
    #     return open(self.captureOutName).read()

    # def getError(self):
    #     """
    #     Get the stderr of a moa run

    #     @returns: stderr output of this job (if captured)
    #     @rtype: string
    #     """
    #     if not os.path.exists(self.captureErrName):
    #         return ""
    #     l.debug("reading error from %s" % self.captureErrName)
    #     return open(self.captureErrName).read()

