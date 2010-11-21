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
import tempfile

import moa.utils
import moa.logger as l
import moa.template
import moa.jobConf

def getJob(wd):
    """
    Utility funtion to instantiate the correct job class

    Currently, 'there is only one' (that is a Gnu Makefile based
    job
    """
    return Job(wd)

def newJob(wd, template, options=None):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type
    """
    if not options:
        options = {}
        
    return Job(wd, template = template, options = options)
    
def newTestJob(template, **options):
    """
    Test function - creates a temp directory and uses that to
    instantiate the job in. This function returns the directory where
    the job is created. All parameters are passed on to L{newJob}

        >>> job = newTestJob(template = 'adhoc')
        >>> isinstance(job, Job)
        True
        >>> os.path.exists(job.wd)
        True
        >>> os.path.exists(os.path.join(job.wd, '.moa', 'template'))
        True

    
    @returns: The directory where the job was created
    @rtype: string
    """

    wd = tempfile.mkdtemp()
    job = Job(wd, template=template, options=options)
    return job

class Job(object):
    """
    Placeholder for a job
    """
    
    def __init__(self,
                 wd,
                 template = None,
                 options = None):
        """        

        """

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd
        if options:
            self.options = options
        else:
            self.options = {}
        
        self.confDir = os.path.join(self.wd, '.moa')

        self.template = None
        self.backend = None
        self.args = []
        self.options = {}

        #first load the template
        if template:
            self.setTemplate(template)
            self.loadBackend()
            self.initialize()
        else:
            self.loadTemplate()
            self.loadBackend()

        # then load the job configuration
        self.conf = moa.jobConf.JobConf(self)


    def checkConfDir(self):
        """
        Check if the configuration directory exists. If
        not create it.
        """
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)


    def getActor(self):
        """
        Get an actor for this job
        """        
        return moa.actor.Actor(wd = self.wd)

    
    def execute(self, command):
        """
        Execute the job
        """
        l.debug("executing %s" % command)
        if self.backend:
            self.backend.execute(command,
                                 verbose = self.options,
                                 background = self.options.background)
        else:
            l.error("No backend loaded - cannot execute %s" % command)
                    
    def prepare(self):
        """
        Prepare this job
        """
        if self.backend:
            self.backend.prepare()
        
    def defineOptions(self, parser):
        """
        Set command line options
        """
        parser.add_option('-f', '--force', dest='force', action='store_true',
                  help = 'Force an action, if applicable.')

        parser.add_option("-v", "--verbose", dest="verbose",
                  action="store_true", help="verbose output")

        parser.add_option("--bg", dest="background",
                  action="store_true", help="Run moa in the background")
        
        if self.backend:
            self.backend.defineOptions(parser)

    def setTemplate(self, name):
        """
        Set a new template for this job
        """
        self.checkConfDir()
        l.debug("Setting job template to %s" % name)
        self.template = moa.template.Template(name)
        with open(os.path.join(self.confDir, 'template'), 'w') as F:
            F.write(name)
            l.debug('set job in %s to template %s' % (self.wd, name))
        
    def loadTemplate(self):
        """
        Load the template for this job, based on what configuration 
        can be found
        """
        templateFile = os.path.join(self.confDir, 'template')
        if os.path.exists(templateFile):
            templateName = open(templateFile).read()
            l.debug("Loading template %s" % templateName)
            self.template = moa.template.Template(templateName)
            l.debug("Loaded template %s" % self.template.name)
            return
        
        #no template found - maybe nothing is installed here
        self.template = moa.template.Template()
        
    def loadBackend(self):
        """
        load the backend
        """
        backendName = self.template.backend
        l.debug("attempt to load backend %s" % backendName)
        try:
            moduleName = 'moa.backend.%s' % backendName
            module =  __import__( moduleName, globals(),
                                   locals(), [moduleName], -1)            
            l.debug("Successfully Loaded module %s" % moduleName)
        except ImportError, e:
            if str(e) == "No module named %s" % moduleName:
                l.critical("Backend %s does not exists" % backendName)
            l.critical("Error loading backend %s" % backendName)
            raise
            
        self.backend = getattr(
            module, '%sBackend' % backendName.capitalize())(self)

        
    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        """
        return self.backend.isMoa()      

    def initialize(self):
        """
        Initialize a new job in the current wd
        """
        l.debug("calling backend to initialize template %s" %
                self.template.name)
        self.backend.initialize()
        
