# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.job
-------

"""

import os
import tempfile

import Yaco

import moa.utils
import moa.logger as l
import moa.template
import moa.jobConf

def newJob(wd, template, title, parameters=[]):
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
    :type force: Boolean
    :param parameters: A list of parameters to set for this job
    :type parameters: list of (key, value) tuples
    :rtype: instance of :class:`moa.job.Job`
    
    """
    
    job = Job(wd)
    job.setTemplate(template)
    job.conf.title = title
    for pk, pv in parameters:
        job.conf[pk] = pv
    job.conf.save()

    return job

def newTestJob(template, title="Test job"):
    """    
    for testing purposes - creates a temporary directory and uses that to
    instantiate a job. This function returns the job object created

    >>> job = newTestJob(template = 'adhoc', title='test title')
    >>> assert(isinstance(job, Job))
    >>> assert(os.path.exists(job.wd))
    >>> assert(job.conf.title == 'test title')
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa', 'template')))
    >>> assert(job.template.name == 'adhoc')
    
    :returns: the created job
    :rtype: instance of :class:`moa.job.Job`
    """
    wd = tempfile.mkdtemp()
    job = Job(wd)
    job.setTemplate(template)
    job.conf.title = title
    job.conf.save()
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
      
    def __init__(self, wd):

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd
        
        self.confDir = os.path.join(self.wd, '.moa')
        self.templateFile = os.path.join(self.confDir, 'template')
        self.backend = None
        self.args = []
        
        #used by the backends to store specific data
        self.data = Yaco.Yaco()
        
        self.loadTemplate()

        # then load the job configuration
        self.conf = moa.jobConf.JobConf(self)
        
    def hasCommand(self, command):
        """        
        Check if this job defines a certain command

        .. Warning::
            THIS METHOD DOES NOT WORK PROPERLY YET

        >>> job = newTestJob('unittest')
        >>> assert(job.hasCommand('run'))
        >>> assert(job.hasCommand('run2'))

        """
        if command in self.template.commands.keys():
            return True
        if self.template.backend == 'ruff':
            return self.backend.hasCommand(command)
        else:
            return True

    def checkCommands(self, commands):
        """
        Check commands, and rearrange if there are delegates.
        
        >>> job = newTestJob('unittest')
        >>> assert(job.template.commands.run.delegate == ['prepare', 'run2'])
        >>> assert(job.checkCommands(['run2']) == ['run2'])
        >>> assert(job.checkCommands(['run']) == ['prepare', 'run2'])
        >>> assert(job.checkCommands(['prepare', 'run']) == ['prepare', 'prepare', 'run2'])
        
        :param commands: The list of commands to check
        :type commands: list of strings
        :returns: The checked list of commands
        :rtype: list of strings
        """        
        rv = []
        for command in commands:
            if self.template.commands.get(command, {}).has_key('delegate'):
                rv.extend(self.template.commands[command].delegate)
            else:
                rv.append(command)
        return rv

    def checkConfDir(self):
        """
        Check if the configuration directory exists. If not create it.
        
        >>> job = newTestJob('unittest')
        >>> confdir = os.path.join(job.wd, '.moa')
        >>> assert(os.path.exists(confdir))
        >>> import shutil
        >>> shutil.rmtree(confdir)
        >>> assert(os.path.exists(confdir) == False)
        >>> job.checkConfDir()
        >>> assert(os.path.exists(confdir))
        """
        
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)

            
    def execute(self, command, verbose=False, background=False):
        """
        Execute `command` in the context of this job. Execution is
        alwasy deferred to the backend

        :param command: the command to execute
        :type command: string
        :param verbose: output lots of data
        :type verbose: Boolean        
        :param background: Run this job in the background? If `True`,
           fork and have the parent return immediately. The child
           finishes. If `False`, wait for the job to finish            
        :type background: Boolean

        """
        if not self.backend:
            l.critical("No backend loaded - cannot execute %s" % command)

        if background:
            #Fork
            child = os.fork()
            if child != 0:
                # This is the parent thread - return
                return child
            
            l.debug("In the child thread - start executing - start run %s" % child)
   
        l.debug("executing %s" % command)
        return self.backend.execute(command, verbose = verbose, background = background)
                    
    def prepare(self):
        """
        Prepare this job
        """
        if self.backend and getattr(self.backend, 'prepare', None):
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
        
        if self.backend and getattr(self.backend, 'defineOptions', None):
            self.backend.defineOptions(parser)

    def setTemplate(self, name):
        """
        Set a new template for this job
        """
        self.checkConfDir()
        l.debug("Setting job template to %s" % name)
        #get the template
        moa.template.initTemplate(self.confDir, name)
        self.loadTemplate()
        
    def loadTemplate(self):
        """
        Load the template for this job, based on what configuration 
        can be found
        """
        self.template = moa.template.Template(self.templateFile)
        self.loadBackend()
                
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
            
        self.backend = getattr(module, backendName.capitalize())(self)
        self.initialize()

        
    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        """
        if os.path.exists('.moa'):
            return True

    def initialize(self):
        """
        Initialize a new job in the current wd
        """
        if getattr(self.backend, 'initialize', None):
            l.debug("calling backend to initialize template %s" %
                    self.template.name)
            self.backend.initialize()
        
