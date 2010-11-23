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
moa.job
-------

"""

import os
import tempfile

import moa.utils
import moa.logger as l
import moa.template
import moa.jobConf

def newJob(wd, template, title):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type

    >>> wd = tempfile.mkdtemp()
    >>> job = newJob(wd, template='blast', title='test')
    >>> assert(isinstance(job, Job))
    >>> assert(job.template.name == 'blast')
    >>> assert(job.conf.title == 'test')
    
    :param wd: Directory to create this job in, note that this
       directory must already exists
    :param template: Template name for this job
    :type template: String
    :rtype: instance of :class:`moa.job.Job`
    
    """
    job = Job(wd, template = template)
    job.conf.title = title
    return job

def newTestJob(template, title="Test job"):
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
    job = Job(wd, template=template)
    job.conf.title = title
    return job

class Job(object):
    """
    Class defining a single job

    >>> wd = tempfile.mkdtemp()
    >>> job = Job(wd)
    >>> assert(isinstance(job, Job))
    >>> assert(job.template.name == 'nojob')
    
    :param wd: The directory containing the job
    :param template: The template a job should have. If undefined,
        read the template from `./.moa/template`
    :param options: Additional options to feed to this job
    """
    
    def __init__(self,
                 wd,
                 template = None):

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd
        
        self.confDir = os.path.join(self.wd, '.moa')

        self.template = None
        self.backend = None
        self.args = []

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
        Check if the configuration directory exists. If not create it.
        """
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)


    def getActor(self):
        """
        Get an instance of :class:`moa.actor.Actor` for this job.

        :rtype: instance of :class:`moa.actor.Actor`
        """        
        return moa.actor.Actor(wd = self.wd)

    
    def execute(self, command, verbose=False, background=False):
        """
        Execute `command` in the context of this job. Execution is
        alwasy deferred to the backend

        :param command: the command to execute
        :type command: string
        
        """
        l.debug("executing %s" % command)
        if self.backend:
            self.backend.execute(command,
                                 verbose = verbose,
                                 background = background)
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
        
