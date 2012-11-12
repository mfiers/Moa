"""
Moa CLI code
"""
import os
import sys

import moa.args
import moa.exceptions
import moa.logger
import moa.ui
from moa.sysConf import sysConf


## Initialize the logger
l = moa.logger.getLogger(__name__)

## define an initial command line parser - so all plugin commands can
## define themselves.
parser, commandparser = moa.args.getParser()


def run_3(wd, exitOnError=True):
    """
    instantiate the job, prepare and run.

    Running means that either a plugin callback is called or the main
    job is executed. Main job execution consists of three steps:

    - prepare
    - run
    - finish

    prepare, run, finish should probably not be overridden by plugin
    callbacks. It is possible to run prepare & finish separately.

    """

    # finally we have a directory to run in - see if this job want to
    # be executed..

    # make sure we're in the correct wd for the rest of the
    # invocation

    os.chdir(wd)

    sysConf.wd = wd

    sysConf.pluginHandler.run('pre_create_job')

    # create the job
    job = moa.job.Job(wd)

    # We should NOT depend on the following (if at all possible)
    sysConf.job = job
    job.defineOptions(parser)
    job.defineCommands(commandparser)

    # Only now the full set of options is parsed
    # first check if there is a command (i.e. any item on sys.argv
    # not starting with a -. If not add the default command
    if  [x for x in sys.argv[1:] if x[0] != '-']:
        args = parser.parse_args()
    else:
        l.debug("Reverting to default command: %s" %
                sysConf.default_command)
        args = parser.parse_args(sys.argv[1:] +
                                 [sysConf.default_command])

    sysConf.args = args
    sysConf.pluginHandler.run('prepare_3')
    l.debug("Command is %s" % sysConf.args.command)

    command = sysConf.args.command
    sysConf.originalCommand = command
    sysConf.command = command

    ## Proper setting of verbosity - after parsing of the
    ## command line
    if sysConf.options.verbose:
        moa.logger.setVerbose()

    #check if we should run this job..
    doRun = sysConf.pluginHandler.run('check_run')
    if (not sysConf.options.force) and False in doRun.values():
        l.warning("Not running job in %s" % wd)
        return

    #see if this is all plugin command callback
    if command in sysConf.commands.keys():
        comInf = sysConf.commands[command]
        if comInf.get('needsJob', False) and not job.isMoa():
            if command == 'status':
                message = "Need a Moa job - try 'moa -h'"
            else:
                message = "'moa %s' needs a job" % command

            moa.ui.message(message)
            sys.exit(-1)

        sysConf.pluginHandler.run('prepare')
        #job.run_hook('prepare') #executed during job initialization
        sysConf.pluginHandler.run('pre%s' % command.capitalize())

        #run the command function
        l.debug("running plugin callback for %s" % command)
        commandFunction = sysConf.commands[command]['call']
        commandFunction(job, args)

        #run finish & post plugin hooks
        sysConf.pluginHandler.run("post%s" % command.capitalize(),
                                  reverse=True)

        job.run_hook('finish')
        sysConf.pluginHandler.run('finish', reverse=True)


def run_2(force_silent=False):
    """
    Are we going to do a recursive run?: check if -r is in the arguments...

    If recursive - check if the command given is a plugin callback or not
    plugin callbacks can have a recursive mode:

    * global - allow recursivity to be handled here
    * local - the callback handles recursive behaviour
    * none - no recursive operation for this template

    non plugin callbacks (commands handled by the backends) are always
    'global'

    """

    # sysConf.pluginHandler.run('prepare_recursion')

    wd = moa.utils.getCwd()
    l.debug("starting run_2 in %s" % wd)

    # never recursive - jump directly into run_3
    try:
        run_3(wd)
    except moa.exceptions.MoaInvalidCommandLine, e:
        parser = e.args[0]
        parser.real_error()

    # sysConf.pluginHandler.run('post_recursion')


def run_1():
    """
    Stage 1 - are we switching to the background?

    if --bg is defined: fork & exit.

    """
    sysConf.pluginHandler.run('prepare_1')
    sysConf.pluginHandler.run('prepare_background')
    sysConf.force_silent = False
    #quick check: are we're backgrounding:
    if '--bg' in sys.argv:
        sysConf.force_silent = True
        child = os.fork()
        if child != 0:
            # This is the parent thread - exit now - all
            sysConf.childPid = child
            sysConf.pluginHandler.run("background_exit")
            moa.ui.message("starting background run")
            sys.exit(0)

    #go to the next stage!
    run_2()

    sysConf.pluginHandler.run('post_background')


def _handle_error(message):
    """
    Try to handle an error situation - i.e. run post_error
    """
    sys.stderr.write("ERROR!\n")
    sys.stderr.write(message + "\n")
    try:
        sysConf.rc = -1
        sysConf.pluginHandler.run("post_error")
    except Exception, e:
        sys.stderr.write("Error - cannot run post_error plugin hook:\n")
        sys.stderr.write(str(e) + "\n\n")


def dispatch():
    """
    Main run - not much has been prepared yet
    """

    ## Initalize system plugins
    sysConf.pluginHandler = moa.plugin.PluginHandler(sysConf.plugins.system)

    sysConf.pluginHandler.run('defineOptions')
    ## A hack to set verbosity before reading command line arguments
    if ('-v' in sys.argv) or ('-vv' in sys.argv):
        moa.logger.setVerbose()

    sysConf.rc = 0

    # check we have the proper version of python
    if sys.version_info < (2, 6):
        raise "Need python >= 2.6 (and < 3.0)"

    try:
        if '--profile' in sys.argv:
            import tempfile
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.close()
            try:
                import cProfile
                import pstats
                cProfile.run('run_1()', tf.name)
                p = pstats.Stats(tf.name)

                moa.ui.message("Profiler output (%s)" % tf.name)
                p.sort_stats('cumulative').print_stats(20)

            except ImportError:
                moa.ui.exitError("Cannot run the profiler - " +
                                 "make sure it is properly installed")
        else:
            run_1()
    except KeyboardInterrupt:
        sysConf.rc = -1
        sysConf.pluginHandler.run("post_interrupt")
        moa.ui.warn("Interrupted")
        if sysConf.options.verbose:
            raise
        else:
            sys.exit(-2)
    except moa.exceptions.MoaDirNotWritable:
        _handle_error("the .moa directory is not writable")
    except IOError, e:
        _handle_error("IOError - maybe the .moa directory is not writable")
        raise e
    except Exception:
        _handle_error("Unexpected error")
        moa.ui.warn("Encountered a run error?")
        raise
