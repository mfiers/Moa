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
l = moa.logger.l


class MOAJOB:
    pass

    
class MOAMAKEFILEJOB:
    """
    One placeholder for information on a moa job
    """

    _reFindTemplate = re.compile(r'\$\(call\s+moa_load\s*,\s*(\S*)\s*\)')
    def __init__(self, wd=None):
        """
        Constructor
        """
        l.debug("Initializing a GNU Make job")

        if not wd:
            self.wd = os.getcwd()
        else:
            self.wd = wd
            
        #This is most probably a makefile job
        self.isMoa = False
        self.template = None
        self.makeArgs = []
        self.refresh()

    def prepareInvocation(self, invocation):
        self.invocation = invocation

        # Prepare the arguments for a moaMake call
        if invocation.options.remake:
            self.makeArgs.append('-B')
        if invocation.options.makedebug:
            self.makeArgs.append('-d')
            
        if invocation.options.threads > 1:
            l.debug("Running make with %d threads" % options.threads)
            self.makeArgs.append('-j %d' % invocation.options.threads)

        ## make sure the MOA_THREADS env var is set - this is used from inside
        ## the Makefiles later threads need to be treated different from the
        ## other parameters. multi-threaded operation is only allowed in the
        ## second phase of execution.
        os.putenv('MOA_THREADS', "%s" % options.threads)
                                 
        ## Store all arguments in the environment - we might want to have a
        ## look at them from the Makefiles
        os.putenv("MOAARGS", "%s" %
                  " ".join(["'" + str(x) + "'" for x in args]))

    def refresh(self):
        """
        refresh / initialize this moajob object
        """
        self._makefile = os.path.join(self.wd, 'Makefile')
        
        if not os.path.exists(self._makefile):
            self.isMoa = False
            return
        
        with open(self._makefile) as F:
            self._makefileText = F.read()

        reft = self._reFindTemplate.search(self._makefileText)
        if not reft:
            l.critical("Invalidly formatted Makefile - exitting")
        self.isMoa = True
        self.template = reft.groups()[0]




moaJob = None

def get():
    """
    Initialize the Moa job 
    
    Determine if there is a moa job installed here and if so, what
    kind. This is done so to keep the possibility open to have
    multiple backends (i.e. possibly replacing make at a certain point
    """
    global moaJob

    if moaJob:
        return moaJob
    
    l.debug("Initalizing Moa job")
    if os.path.exists('Makefile'):
        moaJob = MOAMAKEFILEJOB()
    else:
        moaJob = None

    return moaJob
