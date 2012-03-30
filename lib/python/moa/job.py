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
import glob
import tempfile

import lockfile
import Yaco

import shutil

import moa.ui
import moa.args
import moa.utils
import moa.logger
import moa.plugin
import moa.template
import moa.jobConf
import moa.exceptions
import moa.filesets

l = moa.logger.getLogger(__name__)
from moa.sysConf import sysConf


def newJob(wd, template, title, parameters=[], provider=None):
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
    job.setTemplate(template, provider=provider)
    job.conf.title = title
    for pk, pv in parameters:
        job.conf[pk] = pv
    job.conf.save()
    return job

def newTestJob(template, title="Test job", provider=None):
    """    
    for testing purposes - creates a temporary directory and uses that to
    instantiate a job. This function returns the job object created

    >>> job = newTestJob(template = 'adhoc', title='test title')
    >>> assert(isinstance(job, Job))
    >>> assert(os.path.exists(job.wd))
    >>> assert(job.conf.title == 'test title')
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa')))
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa', 'template')))
    >>> assert(job.template.name == 'adhoc')
    
    :returns: the created job
    :rtype: instance of :class:`moa.job.Job`
    """
    wd = tempfile.mkdtemp()
    job = Job(wd)
    job.setTemplate(template, provider=provider)
    if title:
        job.conf.title = title
    job.conf.save()
    return job

class Job(object):
    """
    Class defining a single job

    Note - in the moa system, there can be only one current job - many
    operations try to access the job in sysConf 

    >>> wd = tempfile.mkdtemp()
    >>> job = Job(wd)
    >>> assert(isinstance(job, Job))
    >>> assert(job.template.name == 'nojob')    
    """
      
    def __init__(self, wd):
        """
        :param wd: The directory containing the job
        :param register: Register this job in the sysConf? Usually this should be yes
        """

        #prepare the plugins
        self.pluginHandler = moa.plugin.PluginHandler(sysConf.plugins.job)

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd

        self.run_hook('prepare')
        
        self.confDir = os.path.join(self.wd, '.moa')
        self.templateFile = os.path.join(self.confDir, 'template')
        self.templateMetaFile = os.path.join(self.confDir, 'template.d', 'meta')
        

        self.backend = None
        self.args = []
        self.env = {}
        
        #used by the backends to store specific data
        self.data = Yaco.Yaco()

        # a list of globs that defines what is crucial to a Moa job
        # and what is not.
        self.data.moaFiles = [
            '.moa/template',
            '.moa/template.d/*',
            '.moa/config',
            '.moa/history',
            '.moa/local_bash_history',
            'moa.*',
            '*.md',
            'Readme', 'README', 'Readme.*',
            'Changelog', 'CHANGELOG', 'Changelog.*',
            'blog.*', 'blog'
            ]

        self.loadTemplate()
        self.loadTemplateMeta()

        # then load the job configuration
        self.run_hook('pre_load_config')
        self.conf = moa.jobConf.JobConf(self)
        
        #prepare filesets (if need be)o
        self.run_hook('pre_filesets')
        self.prepareFilesets()
        self.renderFilesets()


    def run_hook(self, hook):
        """
        Shortcut to run a job plugin hook
        """
        self.pluginHandler.run(hook, job=self)
        
    def prepareFilesets(self):
        moa.filesets.prepare(self)

    def renderFilesets(self):
        moa.filesets.render(self)
        
    def getFiles(self):
        """
        Return all moa files - i.e. all files crucial to this job.

        """
        rv = set()
        for gl in self.data.moaFiles:
            rv.update(set(glob.glob(os.path.join(self.wd, gl))))

        remove = [x for x in rv if x[-1] == '~']
        rv.difference_update(remove)
        return list(rv)
    
    def hasCommand(self, command):
        """        
        Check if this job defines a certain command

        .. Warning::
            THIS METHOD DOES NOT WORK PROPERLY YET

        >>> job = newTestJob('unittest')
        >>> assert(job.hasCommand('run'))
        >>> assert(not job.hasCommand('dummy'))

        """
        if command in self.template.commands.keys():
            return True
        if self.template.backend == 'ruff':
            return self.backend.hasCommand(command)
        else:
            return True

    def checkCommands(self, command):
        """
        Check command, and rearrange if there are delegates.
        
        >>> job = newTestJob('unittest')
        >>> assert(job.template.commands.run.delegate == ['prepare', 'run2'])
        >>> assert(job.checkCommands('run2') == ['run2'])
        >>> assert(job.checkCommands('run') == ['prepare', 'run2'])
        >>> assert(job.checkCommands('prepare') == ['prepare'])
        
        :param commands: The list of commands to check
        :type commands: list of strings
        :returns: The checked list of commands
        :rtype: list of strings
        """        
        rv = []
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
            
    def execute(self, job, args, **kwargs):
        """
        Execute `command` in the context of this job. Execution is
        alwasy deferred to the backend

        #Note: Uncertain how to test verbose & silent

        :param verbose: output lots of data
        :type verbose: Boolean        
        :param silent: output nothing
        :type silent: Boolean        

        """

        # want to be certain that we're not mixing things up - this is
        # a called with ourselves as the first argument (well first &
        # second) - not really necessary - but required for the plugin
        # command calls.
        assert(job == self)
        
        if not self.backend:
            moa.ui.exitError("No backend loaded - cannot execute %s" % command)

        #figure out what we were really after
        command = args.command

        #prepare for execution - i.e. prepare log dir, etc..
        self.prepareExecute()
        
        #unless command == 'run' - just execute it and return the RC
        if command != 'run':
            sysConf.rc =  self.backend.execute(self, command, args)
            self.finishExecute()
            return sysConf.rc
        
        # command == 'run' is a special case - this will trigger a series of
        # runs.

        for subcommand in ['prepare', 'run', 'finish']:
            try:
                rc = self.backend.execute(self, subcommand, args)
                l.debug(("executing backend '%s' finished "+
                        "with an rc of %s") % (subcommand, rc))
                if rc != 0:
                    sysConf.rc = rc
                    sysConf.pluginHandler.run("post_error")
                    return rc
            except moa.exceptions.MoaCommandDoesNotExist:
                l.debug("%s step is not present" % subcommand)
        
        self.finishExecute()

        return sysConf.rc

    def prepareExecute(self):
        """
        Give this job a chance to prepare for execution.
        
        """

        #organize a run id..
        runIdFile = os.path.join(self.confDir, 'last_run_id')
        sysConf.runId = 1
        lock = lockfile.FileLock(runIdFile)
        
        try:
            with lock:
                old_id = 0
                if os.path.exists(runIdFile):
                    with open(runIdFile) as F:
                        _o = F.read().strip()
                        try:
                            old_id = int(_o)
                        except:
                            pass
                sysConf.runId = old_id + 1
                with open(runIdFile, 'w') as F:
                    F.write("%s" % sysConf.runId)
        except lockfile.LockFailed, e:
            if 'failed to create' in str(e):
                raise moa.exceptions.MoaDirNotWritable()
            raise

        #create a new folder for logging
        logDir = os.path.join(self.confDir, 'log.d', '%d' % sysConf.runId)
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        
        #and a shortcut to that folder
        latestDir = os.path.join(self.confDir, 'log.latest')
        if os.path.exists(latestDir):
            try:
                os.remove(os.path.join(self.confDir, 'log.latest'))
            except OSError:
                #possibly not a link, but a folder - post copying -
                #try that
                shutil.rmtree(os.path.join(self.confDir, 'log.latest'))
                
        os.symlink('log.d/%d' % sysConf.runId, latestDir)

        l.debug("Acquired job id %s" % sysConf.runId)              

        #see if the backend wants to do something
        if self.backend and getattr(self.backend, 'prepare', None):
            self.backend.prepare()

        
    def finishExecute(self):
        """
        Finish the run!
        """
        if self.backend and getattr(self.backend, 'finish', None):
            self.backend.finish()            
                

    def defineCommands(self, commandparser):
        """
        Register template commands with the argparser
        """
        parser, cparser = moa.args.getParser()
        
        for c in self.template.commands:
            cinf = self.template.commands[c]
            hlp = cinf.get('help', '').strip()
            if not hlp:
                hlp = '(Execute template command "%s")' % c
                
            cp = cparser.add_parser(
                str(c), help=hlp)
            
            cp.add_argument(
                "-r", "--recursive", dest="recursive", action="store_true",
                default="false", help="Run this job recursively")

            cp.add_argument(
                "-v", "--verbose", dest="verbose", action="store_true",
                help="Show debugging output")
            
            cp.add_argument(
                "--bg", dest="background", action="store_true",
                help="Run moa in the background (implies -s)")

            cp.add_argument(
                "--profile", dest="profile", action="store_true",
                help="Run the profiler")
            
            cp.add_argument(
                "-j", dest="threads", type=int,
                default=1, help="No threads to use when running Ruffus")

            sysConf.commands[c] = {
                'desc' : hlp,
                'long' : hlp,
                'source' : 'template',
                'recursive' : 'global',
                'needsJob' : True,
                'call' : self.execute }
        
    def defineOptions(self, parser):
        """
        Set command line options - deferred to the backend
        
        >>> job = newTestJob('unittest')
        >>> import optparse
        >>> parser = optparse.OptionParser()
        >>> job.defineOptions(parser)

        """
        if self.backend and getattr(self.backend, 'defineOptions'):
            self.backend.defineOptions(parser)
                
    def refreshTemplate(self):
        """
        Reload the template into the local .moa/template.d directory

        >>> job = newTestJob('unittest')
        >>> templateFile = os.path.join(job.confDir, 'template.d', 'unittest.jinja2')
        >>> assert(os.path.exists(templateFile))
        >>> os.unlink(templateFile)
        >>> assert(not os.path.exists(templateFile))
        >>> job.refreshTemplate()
        >>> assert(os.path.exists(templateFile))
        
        """
        moa.template.refresh(self.wd)
        
    def setTemplate(self, name, provider = None):
        """
        Set a new template for this job

        >>> job = newTestJob('unittest')
        >>> job.setTemplate('adhoc')
        >>> afile = os.path.join(job.confDir, 'template.d', 'adhoc.mk')
        >>> assert(os.path.exists(afile))
        """
        self.checkConfDir()
        l.debug("Setting job template to %s" % name)
        #get the template
        moa.template.installTemplate(self.wd, name, provider = provider)
        self.loadTemplate()
        
    def loadTemplate(self):
        """
        
        Load the template for this job, based on what configuration 
        can be found
        """
        self.template = moa.template.Template(self.templateFile)
        l.debug("Job loaded template %s" % self.template.name)
        self.loadBackend()

    def loadTemplateMeta(self):
        """        
        Load the template meta data for this job, based on what configuration 
        can be found
        """
        self.templateMeta = Yaco.Yaco()
        if os.path.exists(self.templateMetaFile):
            self.templateMeta.load(self.templateMetaFile)
        l.debug("Job loaded template metadata")

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
            l.critical("!! Error loading backend %s" % backendName)
            raise
            
        #self.backend = getattr(module, backendName.capitalize())(self)
        self.backend = getattr(module, 'load')(self)
        self.initialize()

        
    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        #weird; uncertain if this ever gets called
        
        """
        if not os.path.exists(os.path.join(self.wd, '.moa')):
            return False
        if str(self.template.name).lower() == 'noJob':
            return False
        return True
                              

    def initialize(self):
        """
        Initialize a new job in the current wd
        """
        if getattr(self.backend, 'initialize', None):
            l.debug("calling backend to initialize template %s" %
                    self.template.name)
            self.backend.initialize()
        


####
# nose tests

