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
Job
"""

import os
import re
import sys
import tempfile

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.runMake

#import moa.job.base
#import moa.job.gnumake
#import moa.job.nojob

def getJob(wd):
    """
    Utility funtion to instantiate the correct job class

    Currently, 'there is only one' (that is a Gnu Makefile based
    job
    """
    return Job(wd)

def newJob(wd, **kwargs):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type
    """

    job = Job(wd)
    job.setTemplate(kwargs['template'])
    job.initialize(**kwargs)
    return job
    
def newTestJob(*args, **kwargs):
    """
    Test function - creates a temp directory and uses that to
    instantiate the job in. This function returns the directory where
    the job is created. All parameters are passed on to L{newJob}

        >>> d = newTestJob('traverse')
        >>> type(d) == type('hi')
        True
        >>> os.path.exists(d)
        True
        >>> os.path.exists(os.path.join(d, 'Makefile'))
        True
        >>> job = moa.runMake.MOAMAKE(wd = d, captureErr=True)
        >>> rc = job.run()
        >>> type(rc) == type(1)
        True
    
    @returns: The directory where the job was created
    @rtype: string
    """

    wd = tempfile.mkdtemp()
    if args:
        kwargs['template'] = args[0]               
    job = newJob(wd, **kwargs)
    return wd

class Job(object):
    """
    Placeholder for a job
    """
    
    def __init__(self, wd):
        """        
        """        
        self.wd = wd
        self.confDir = os.path.join(self.wd, '.moa')
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)
        
        self.conf = moa.conf.Config(self)
            
        self.loadTemplate()
        self.loadBackend()
        
               
    def setTemplate(self, name):
        """
        Set a new template for this job
        """ 
        self.template = moa.template.Template(name)
        self.template.save(self.wd)
        self.loadBackend()
        
    def loadTemplate(self):
        """
        Load the template for this job, based on what configuration 
        can be found
        """
        templateFile = os.path.join(self.confDir, 'template')
        if os.path.exists(templateFile):
            templateName = open(templateFile).read()
            self.template = moa.template.Template(templateName)
            return
        
        #no proper config - check if this is an old-style gnumake job
        rc = self._fixOldGnumakeJob()
        if rc: 
            return
        
        #no template found - maybe nothing is installed here
        self.template = moa.template.Template()
        
    def _fixOldGnumakeJob(self):
        """
        'hack' to be able to handle old style gnumake jobs
        """
        makefile = os.path.join(self.wd, 'Makefile')
        if os.path.exists(makefile):
            with open(makefile) as F:
                makedata = F.read()
            if 'MOABASE' in makedata:
                templateName = makedata.split('moa_load,')[1].split(')')[0]
            with open(os.path.join(self.confDir, 'template'), 'w') as F:
                F.write(templateName)
            l.info("assuming old style gnumake template %s" % templateName)
            self.template = moa.template.Template(templateName)
            return True
        return False

    def loadBackend(self):
        """
        load the backend
        """
        backendName = self.template.backend
        try:
            _moduleName = 'moa.backend.%s' % backendName
            _module =  __import__( _moduleName, globals(), locals(), [_moduleName], -1)            
            l.debug("Successfully Loaded module %s" % _moduleName)
        except ImportError, e:
            if str(e) == "No module named %s" % _moduleName:
                l.critical("Backend %s does not exists" % backendName)
            l.critical("Error loading backend %s" % backendName)
            sys.exit(-1)                
            
        self.backend = getattr(_module, '%sBackend' % backendName.capitalize())(self)

    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        """
        self.backend.isMoa()      

    def initialize(self, 
             force=False, 
             **kwargs):
        """
        Initialize a new job in the current wd
        """

        if self.isMoa() and not force:
            l.error("A job does already exists in this directory")
            l.error("specify -f (--force) to override")
            return False     

        #check if a template is defined - if not, use the job template
        if kwargs.has_key('template'):
            if type(kwargs['template']) == type("string"):
                self.setTemplate(kwargs['template'])
                kwargs['template'] = self.template
        else:
            kwargs['template'] = self.template
                    
        self.backend.initialize(**kwargs)
        
