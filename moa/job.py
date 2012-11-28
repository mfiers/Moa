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
import sys
import glob
import tempfile

import lockfile
import Yaco

import shutil

import moa.ui
import moa.args
import moa.actor
import moa.utils
import moa.logger
import moa.plugin
import moa.template
import moa.jobConf
import moa.exceptions
import moa.filesets

l = moa.logger.getLogger(__name__)
from moa.sysConf import sysConf


def newJob(job, template, title, parameters=[], provider=None):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type

    :param job: Job object to fill - needs only wd set.
    :param template: Template name for this job
    :type template: String
    :type force: Boolean
    :param parameters: A list of parameters to set for this job
    :type parameters: list of (key, value) tuples
    :rtype: instance of :class:`moa.job.Job`
    """

    job.setTemplate(template, provider=provider)
    job.load_config()
    job.conf.title = title
    for pk, pv in parameters:
        job.conf[pk] = pv
        moa.ui.message('Setting "%s" to "%s"' % (pk, pv))
    job.conf.save()
    return job


def newTestJob(template, title="Test job", provider=None):
    """
    for testing purposes - creates a temporary directory and uses that to
    instantiate a job. This function returns the job object created

    >>> job = newTestJob(template = 'simple', title='test title')
    >>> assert(isinstance(job, Job))
    >>> assert(os.path.exists(job.wd))
    >>> assert(job.conf.title == 'test title')
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa')))
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa', 'template')))


    ### >>> assert(job.template.name == 'simple')

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
        """

        #prepare the plugins
        self.pluginHandler = moa.plugin.PluginHandler(sysConf.plugins.job)

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd

        l.debug('Instantiating job in %s' % self.wd)

        self.confDir = os.path.join(self.wd, '.moa')

        self.backend = None
        self.args = []
        self.env = {}

        #used by the backends to store specific data
        self.data = Yaco.Yaco()

        # a list of globs that defines what is crucial to a Moa job
        # and what is not.
        self.data.moaFiles = [
            '.moa/template',
            '.moa/template.meta',
            '.moa/template.d/*',
            '.moa/config',
            '.moa/project_uid',
            '.moa/history',
            '.moa/local_bash_history',
            'moa.*',
            '*.md',
            'Readme', 'README', 'Readme.*',
            'Changelog', 'CHANGELOG', 'Changelog.*',
            'blog.*', 'blog'
        ]

        self.init2()

    def init2(self):
        """
        Continue initialization
        """
        if self.wd.split(os.path.sep)[-1] == '.moa':
           #this is a .moa dir = cannot be a job
            return

        self.run_hook('prepare')

        self.loadTemplate()

        self.load_config()
        #prepare filesets (if need be)
        self.run_hook('pre_filesets')
        self.prepareFilesets()
        self.renderFilesets()

    def load_config(self):
        # then load the job configuration
        self.run_hook('pre_load_config')
        self.conf = moa.jobConf.JobConf(self)

    def run_hook(self, hook, **kwargs):
        """
        Shortcut to run a job plugin hook
        """
        self.pluginHandler.run(hook, job=self, **kwargs)

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


        ### >>> assert(job.hasCommand('dummy'))

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


        ## >>> assert(job.template.commands.run.delegate == ['prepare', 'run2'])
        ## >>> assert(job.checkCommands('run2') == ['run2'])
        ## >>> assert(job.checkCommands('run') == ['prepare', 'run2'])
        ## >>> assert(job.checkCommands('prepare') == ['prepare'])

        :param commands: The list of commands to check
        :type commands: list of strings
        :returns: The checked list of commands
        :rtype: list of strings
        """
        rv = []
        if 'delegate' in self.template.commands.get(command, {}):
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

        #Note: this is the function that will be called from argparse
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

        actor = moa.actor.getActor()
        moa.ui.message("loaded %s actor %s" % (actor.category, actor.__name__))

        #figure out what we were really after
        command = args.command

        l.info("Running '%s'" % command)

        #prepare for execution - i.e. prepare log dir, etc..
        self.prepareExecute()

        # unless command == 'run' - just execute it and return the RC
        if command != 'run':
            l.debug("Simple type execute of '%s'" % command)
            rc = self.backend.execute(self, command, args)
            sysConf.rc = rc
            if rc != 0:
                self.pluginHandler.run("post_error", job=self)
                sysConf.pluginHandler.run("post_error")
                moa.ui.exitError("Error running")
            return rc

        # command == 'run' is a special case - this will trigger a series of
        # runs.

        l.debug("Starting RUN")
        for subcommand in ['prepare', 'run', 'finish']:
            self.pluginHandler.run("pre_%s" % subcommand, job=self)
            l.debug("Starting RUN/%s" % subcommand)
            try:
                rc = self.backend.execute(self, subcommand, args)
                l.debug(("executing backend '%s' finished " +
                        "with an rc of %s") % (subcommand, rc))
                if rc != 0:
                    sysConf.rc = rc
                    self.pluginHandler.run("post_error", job=self)
                    sysConf.pluginHandler.run("post_error")
                    moa.ui.exitError("Exit on error")
            except moa.exceptions.MoaCommandDoesNotExist:
                l.debug("%s step is not present" % subcommand)

        self.finishExecute()

        #if async - exit here
        if actor.category == 'async':
            self.pluginHandler.run("async_exit", job=self)
            sysConf.pluginHandler.run("async_exit")
            moa.ui.message("async run started - quiting now")
            sys.exit(0)

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

        for comm in ['unittest', 'prepare', 'finish']:
            if self.hasCommand(comm):
                # this does not have to be defined in the .moa - if it is here
                # we'll register it
                hlp = 'run "%s" for this template' % comm
                cp = cparser.add_parser(
                    comm, help=hlp)
                
                sysConf.commands[comm] = {
                    'desc': hlp,
                    'long': hlp,
                    'source': 'template',
                    'needsJob': True,
                    'call': self.execute
                    }

        for c in self.template.commands:

            cinf = self.template.commands[c]
            hlp = cinf.get('help', '').strip()
            if not hlp:
                hlp = '(Execute template command "%s")' % c

            cp = cparser.add_parser(
                str(c), help=hlp)

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

            self.run_hook('defineCommandOptions', parser=cp)
            sysConf.commands[c] = {
                'desc': hlp,
                'long': hlp,
                'source': 'template',
                'needsJob': True,
                'call': self.execute
            }

    def defineOptions(self, parser):
        """
        Set command line options - deferred to the backend - PER COMMAND

        >>> job = newTestJob('unittest')
        >>> import optparse
        >>> parser = optparse.OptionParser()
        >>> job.defineOptions(parser)

        """
        #self.run_hook('defineOptions', parser=parser)
        if self.backend and getattr(self.backend, 'defineOptions'):
            self.backend.defineOptions(parser)

    def refreshTemplate(self):
        """
        Reload the template into the local .moa/template.d directory

        >>> job = newTestJob('unittest')
        >>> templ = os.path.join(job.confDir, 'template.d', 'unittest.jinja2')
        >>> assert(os.path.exists(templ))
        >>> os.unlink(templ)
        >>> assert(not os.path.exists(templ))
        >>> job.refreshTemplate()
        >>> assert(os.path.exists(templ))

        """
        moa.template.refresh(self.wd)

    def setTemplate(self, name, provider=None):
        """
        Set a new template for this job

        >>> job = newTestJob('unittest')
        >>> job.setTemplate('simple')
        >>> afile = os.path.join(job.confDir, 'template.d', 'simple.jinja2')
        >>> assert(os.path.exists(afile))
        """
        self.checkConfDir()
        l.debug("Setting job template to %s" % name)
        #get the template
        moa.template.installTemplate(self.wd, name, provider=provider)
        self.loadTemplate()

    def loadTemplate(self):
        """

        Load the template for this job, based on what configuration
        can be found
        """
        self.template = moa.template.Template(self.wd)
        l.debug("Job loaded template %s" % self.template.name)
        self.loadBackend()

    def loadBackend(self):
        """
        load the backend
        """
        backendName = self.template.backend

        l.debug("attempt to load backend %s" % backendName)
        try:
            moduleName = 'moa.backend.%s' % backendName
            module = __import__(moduleName, globals(),
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
        Check if this is a Moa directory - Currently,
        this needs to be overridden

        TODO: check if this  ever gets called
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
