# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**parallelActor** - Run jobs through PARALLEL
-----------------------------------------------------------

"""
import os
import stat
import subprocess as sp
import sys
import tempfile


import jinja2
import moa.logger
import moa.ui
from moa.sysConf import sysConf


l = moa.logger.getLogger(__name__)
# l.setLevel(moa.logger.DEBUG)


def hook_defineCommandOptions(job, parser):
    parser.add_argument('--prl', action='store_const', const='parallel',
                        dest='actorId', help='Use gnu parallel as actor')

    parser.add_argument('--prl_dummy', default=False, dest='parallelDummy',
                        action='store_true',
                        help='Do not execute - just create a script to run')


def _writeOlTmpFile(wd, _script):
    # save the file
    tmpdir = os.path.join(wd, '.moa', 'tmp')
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    tf = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='parallel.',
                                     delete=False, suffix='.sh')
    if isinstance(_script, list):
        tf.write("\n".join(_script))
    else:
        tf.write(str(_script))

    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    return tf.name


@moa.actor.async
def parallelRunner(wd, cl, conf={}, **kwargs):
    """
    Run the job using PARALLEL

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """

    # see if we can get a command
    command = kwargs.get('command', 'unknown')

    if command == 'unknown':
        l.critical("runner should be called with a command")
        sys.exit(-1)

    l.debug("starting parallel actor for %s" % command)

    if not command in sysConf.job.data.parallel.scripts:
        sysConf.job.data.parallel.scripts[command] = []

    sysConf.job.data.parallel.scripts[command].extend(cl)

    return 0


def _prep_parallel_script(wd, conf, job_file, prepare_script=None,
                          finish_script=None):

    # this is a trick to get the real path of the log dir - but not of
    # any underlying directory - in case paths are mounted differently
    # on different hosts - which it SHOULD NOT!!!
    outDir = os.path.abspath(os.path.join(wd, '.moa', 'log.latest'))
    outDir = outDir.rsplit('.moa', 1)[0] + '.moa' + \
        os.path.realpath(outDir).rsplit('.moa', 1)[1]

    sysConf.job.data.parallel.outDir = outDir

    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    # expect the cl to be nothing more than a single script to execute
    outfile = os.path.join(outDir, 'stdout')
    errfile = os.path.join(outDir, 'stderr')

    sysConf.job.data.parallel.outfile = outfile
    sysConf.job.data.parallel.errfile = errfile

    sc = []

    def s(*cl):
        sc.append(" ".join(map(str, cl)))

    s("#!/bin/bash")

    # dump the configuration in the environment
    s("")
    s("## ensure we're in the correct directory")
    s("cd", wd)

    s("")
    s("## Defining moa specific environment variables")
    s("")

    confkeys = sorted(conf.keys())
    for k in confkeys:
        # to prevent collusion, prepend all env variables
        # with 'moa_'
        if k[0] == '_' or k[:3] == 'moa':
            outk = k
        else:
            outk = 'moa_' + k
        v = conf[k]

        # this should not happen:
        if ' ' in outk:
            continue

        # reformat lists
        if isinstance(v, list):
            s("%s='%s'" % (outk, " ".join(v)))
        elif isinstance(v, dict):
            continue
        else:
            s("%s='%s'" % (outk, v))

    if not prepare_script is None:
        s("## Run prepare!")
        s(prepare_script)

    s("")
    s("## Run parallel to execute all commands")
    s("cat %s | parallel '{}'" % job_file)
    s("")

    s("")

    if not finish_script is None:
        s("## Run finish!")
        s(finish_script)
    return sc

def hook_async_exit(job):
    """
    actually submit the worker job
    """

    # make sure that this is the correct actor
    actor = moa.actor.getActor()
    if actor.__name__ != 'parallelRunner':
        return

    wd = job.wd

    finish_script = None
    prepare_script = None
    run_scripts = []

    prepare_script = None
    finish_script = None

    # save the file
    tmpdir = os.path.join(wd, '.moa', 'tmp')
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    run_script_tf = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='parallel.data.',
                                     delete=False, suffix='.txt')

    os.chmod(run_script_tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    tmpdir = os.path.join(wd, '.moa', 'tmp')

    for cat in sysConf.job.data.parallel.scripts:

        scripts = sysConf.job.data.parallel.scripts[cat]


        if cat == 'finish':
            assert(len(scripts) == 1)
            finish_script = scripts[0]


        elif cat == 'prepare':
            assert(len(scripts) == 1)
            prepare_script = scripts[0]

        elif cat == 'run':
            run_scripts = scripts
            for script in scripts:
                run_script_tf.write("%s\n" % script)
        else:
            moa.ui.exitError("parallel only works with prepare/run/finish")

    if len(run_scripts) == 0:
        #no 'run' level scripts - do not do anything.
        moa.ui.message("No jobs to run")
        return

    run_script_tf.close()
    script = _prep_parallel_script(job.wd, job.conf,
                                   job_file=run_script_tf.name,
                                   prepare_script=prepare_script,
                                   finish_script=finish_script)

    if sysConf.args.parallelDummy:

        with open(os.path.join(job.wd, 'moa.parallel.run.sh'), 'w') as F:
            F.write("\n".join(script))

        cl = './moa.parallel.run.sh'

        moa.ui.message("Would have executed:")
        moa.ui.message(cl)
    else:
        tmpdir = os.path.join(wd, '.moa', 'tmp')
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)

        tf = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='parallel.',
                                     delete=False, suffix='.sh')
        tf.write("\n".join(script))
        tf.close()
        os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        moa.ui.message("Executing: %s" % tf.name)
        os.system("%s &" % tf.name)

    return

    uid = "%s.%s" % (job.wd.split('/')[-1], max(jidlist))
    sysConf.job.data.parallel.uid = uid
    onsuccess = jinja2.Template(OnSuccessScript).render(sysConf)
    onerror = jinja2.Template(OnErrorScript).render(sysConf)


# register this actor globally
sysConf.actor.actors['parallel'] = parallelRunner
