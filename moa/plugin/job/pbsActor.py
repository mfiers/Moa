# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**pbsActor** - Run jobs through PBS
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
#l.setLevel(moa.logger.DEBUG)


def hook_defineCommandOptions(job, parser):
    parser.add_argument('--pbs', action='store_const', const='pbs',
                        dest='actorId', help='Use Pbs as actor')

    parser.add_argument('--pbs_queue', default=None, dest='pbsQueue',
                        help='The Pbs queue to submit this job to')

    parser.add_argument('--pbs_extra', default='', dest='pbsExtra',
                        help='Extra arguments for qsub')

    parser.add_argument('--pbs_req', dest='pbsReq', action='append',
                        help='pbs job requirements')

    parser.add_argument('--pbs_acc', default='', dest='pbsAccount',
                        help='pbs account to charge')

    parser.add_argument('--pbs_dummy', default=False, dest='pbsDummy',
                        action='store_true',
                        help='Do not execute - just create a script to run')


def _writeOlTmpFile(wd, _script):
    #save the file
    tmpdir = os.path.join(wd, '.moa', 'tmp')
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    tf = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='pbs.',
                                     delete=False, suffix='.sh')
    if isinstance(_script, list):
        tf.write("\n".join(_script))
    else:
        tf.write(str(_script))

    tf.close()
    os.chmod(tf.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    return tf.name

@moa.actor.async
def pbsRunner(wd, cl, conf={}, **kwargs):
    """
    Run the job using PBS

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """

    #see if we can get a command
    command = kwargs.get('command', 'unknown')

    if command == 'unknown':
        l.critical("runner should be called with a command")
        sys.exit(-1)

    l.debug("starting pbs actor for %s" % command)
    
    if not command in sysConf.job.data.pbs.scripts:
        sysConf.job.data.pbs.scripts[command] = []
    
    sysConf.job.data.pbs.scripts[command].extend(cl)
    
    return 0


def _prep_pbs_script(wd, conf):

    # this is a trick to get the real path of the log dir - but not of
    # any underlying directory - in case paths are mounted differently
    # on different hosts

    outDir = os.path.abspath(os.path.join(wd, '.moa', 'log.latest'))
    outDir = outDir.rsplit('.moa', 1)[0] + '.moa' + \
        os.path.realpath(outDir).rsplit('.moa', 1)[1]

    sysConf.job.data.pbs.outDir = outDir

    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    #expect the cl to be nothing more than a single script to execute

    outfile = os.path.join(outDir, 'stdout')
    errfile = os.path.join(outDir, 'stderr')

    sysConf.job.data.pbs.outfile = outfile
    sysConf.job.data.pbs.errfile = errfile

    sc = []

    def s(*cl):
        sc.append(" ".join(map(str, cl)))

    s("#!/bin/bash")
    s("#PBS -o %s" % outfile)
    s("#PBS -e %s" % errfile)

    if sysConf.args.pbsQueue:
        s("#PBS -q %s" % sysConf.args.pbsQueue)

    for pbsReq in sysConf.args.pbsReq:
        s("#PBS -l %s" % pbsReq)

    if sysConf.args.pbsAccount:
        s("#PBS -A %s" % sysConf.args.pbsAccount)

    if sysConf.args.pbsExtra.strip():
        s("#PBS %s" % sysConf.args.pbsExtra)

    #give it a reasonable name
    jobname = ("%s" % wd.split('/')[-1])
    s("#PBS -N '%s'" % jobname)

    #dump the configuration in the environment
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

        #this should not happen:
        if ' ' in outk:
            continue

        if isinstance(v, list):
            s("%s='%s'" % (outk, " ".join(v)))
        elif isinstance(v, dict):
            continue
        else:
            s("%s='%s'" % (outk, v))

    s("")
    s("## Run the command")
    s("")
    s("$moa_pbs_worker_script")
    
    s("")
    return sc

def run_pbs_script(wd, command, script):

    #run the pbs script
    
    if sysConf.args.pbsDummy:
        # Dummy mode - do not execute  - just write the script.
        outFile = os.path.join(wd, 'run.%s.pbs' % command)

        with open(outFile, 'w') as F:
            F.write("\n".join(script))
            moa.ui.message("Created pbs submit script: %s" %
                           outFile.rsplit('/', 1)[1])

            moa.ui.message("now run:")
            moa.ui.message("   qsub < %s" % outFile.rsplit('/', 1)[1])
            return -1

    tmpfile = _writeOlTmpFile(wd, sc)

    moa.ui.message("PBS Running %s:" % " ".join(map(str, qsub_cl)))
    moa.ui.message("(copy of) the qsub script: %s" % tmpfile)

    #p = sp.Popen(map(str, qsub_cl), cwd=wd, stdout=sp.PIPE, stdin=sp.PIPE)
    #o, e = p.communicate("\n".join(sc))

    jid = int(o.split(".")[0])
    
    moa.ui.message("Submitted a job to pbs with id %d" % jid)

    if not sysConf.job.data.pbs.jids.get(command):
        sysConf.job.data.pbs.jids[command] = []

    #store the job id submitted
    if not sysConf.job.data.pbs.jids.get(command):
            sysConf.job.data.pbs.jids[command] = []
    if not sysConf.job.data.pbs.get('alljids'):
            sysConf.job.data.pbs.alljids = []
    sysConf.job.data.pbs.jids[command].append(jid)
    sysConf.job.data.pbs.alljids.append(jid)
    l.debug("jids stored %s" % str(sysConf.job.data.pbs.jids))

    return p.returncode


def hook_async_exit(job):
    """
    actually submit the worker job
    """

    #make sure that this is the correct actor
    actor = moa.actor.getActor()
    if actor.__name__ != 'pbsRunner':
        return

    wd = job.wd

    finish_script = None
    prepare_script = None
    run_scripts = None
    cats = set()
    for cat in  sysConf.job.data.pbs.scripts:

        scripts = sysConf.job.data.pbs.scripts[cat]

        if cat == 'finish':
            assert(len(scripts) == 1)
            finish_script = scripts[0]

        elif cat == 'prepare':
            assert(len(scripts) == 1)
            prepare_script = scripts[0]

        elif cat == 'run':
            run_scripts = scripts
            with open(os.path.join(job.wd, 'data.run'), 'w') as F:
                F.write('moa_pbs_worker_script\n')
                for script in scripts:
                    F.write("%s\n" % script)
        else:
            moa.ui.exitError("pbs only works with prepare/run/finish")

    script = _prep_pbs_script(job.wd, job.conf)
    with open(os.path.join(job.wd, 'moa.worker.pbs'), 'w') as F:
        F.write("\n".join(script))

    cl='wsub'

    if prepare_script:
        cl += ' -prolog %s' % prepare_script
    if finish_script:
        cl += ' -epilog %s' % finish_script

    cl += ' -batch moa.worker.pbs -data data.run'

    if sysConf.args.pbsDummy:
        moa.ui.message("Would have executed:")
        moa.ui.message(cl)
        moa.ui.message("dry run:")
        os.system("%s -dryrun"  % cl)
    else:
        os.system("%s"  % cl)

    return
    

    uid = "%s.%s" % (job.wd.split('/')[-1],max(jidlist))
    sysConf.job.data.pbs.uid = uid
    onsuccess = jinja2.Template(OnSuccessScript).render(sysConf)
    onerror = jinja2.Template(OnErrorScript).render(sysConf)




#register this actor globally
sysConf.actor.actors['pbs'] = pbsRunner
sysConf.actor.pbs.jids = []
