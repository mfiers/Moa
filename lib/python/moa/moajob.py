# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
MoaJob
"""

import os
import re
import optparse

import moa.project
import moa.logger as l


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
