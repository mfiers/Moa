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
MoaJob
"""

import os
import re
import optparse

import moa.project
import moa.logger
import moa.moajob
l = moa.logger.l

import moa.moajob

class MOAINVOCATION:
    """
    A MOA invocation and all metadata that belongs to it
    """

    def __init__(self, wd, options, args):
        self.wd = wd

        self.options = options
        self.args = args
        self.job = None
        
        ### determine what the command is
        self.command = ""
        if len(args) > 0:
            self.command = args[0]
            self.args = args[1:]
            l.info('Starting moa command "%s"' % self.command)
            
        ### Determine project root (if there is one)
        projectRoot = moa.project.findProjectRoot(self.wd)
        if projectRoot:
            l.debug('Project root is %s' % projectRoot)
            os.putenv('MOAPROJECTROOT', projectRoot)
        self.refresh()
        
    def refresh(self):
        """
        Refresh our knowledge of this job.
        """
        self.job = moa.moajob.get()
        if self.job:
            self.job.prepareInvocation(self)
        

moaInvocation = None

def get(options, args):
    global moaInvocation
    if moaInvocation == None:
        moaInvocation = MOAINVOCATION(os.getcwd(), options, args)
    return moaInvocation
        
