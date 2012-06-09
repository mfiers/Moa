# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**sgeActor** - Run jobs through SGE
-----------------------------------------------------------

"""
import os
import sys
import stat
import time
import tempfile
import optparse
import subprocess as sp

from moa.sysConf import sysConf
import moa.logger as l
import moa.ui

l = moa.logger.getLogger(__name__)
#l.setLevel(moa.logger.DEBUG)

def hook_defineCommandOptions(job, parser):
    parser.add_argument( '--ol', action='store_const', const='openlava',
                               dest='actorId', help='Use OpenLava as actor' )

    parser.add_argument( '--olq', default='normal', dest='openlavaQueue', 
                         help='The Openlava queue to submit this job to' )

    parser.add_argument( '--oln', default=1, type=int, dest='openlavaSlots', 
                         help='The number of cores the jobs requires')

    parser.add_argument( '--olm', default=1, dest='openlavaHost', 
                         help='The host to use for openlava')

def openlavaRunner(wd, cl, conf={}, **kwargs):
    """
    Run the job using OPENLAVA

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

    l.debug("starting openlava actor for %s" % command)

    outDir = os.path.realpath(os.path.abspath(os.path.join(wd, '.moa', 'log.latest')))
    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    #expect the cl to be nothing more than a single script to execute
    outfile = os.path.join(outDir, 'stdout')
    errfile = os.path.join(outDir, 'stderr')
    
    bsub_cl = ['bsub']

    sc = []
    def s(*cl):
        sc.append(" ".join(map(str, cl)))

    s("#!/bin/bash")
    s("cd", wd)
    bsub_cl.extend(["-o", outfile])
    bsub_cl.extend(["-e", errfile])
    bsub_cl.extend(["-q", sysConf.args.openlavaQueue])


    if '--oln' in sys.argv:
        slots = sysConf.args.openlavaSlots
    else:
        slots = sysConf.job.conf.get('threads', sysConf.args.openlavaSlots)

    bsub_cl.extend(["-n", slots])

    if '--olm' in sys.argv:
        bsub_cl.extend(["-m", sysConf.args.openlavaHost])

    lastJids = []

    #if len(sysConf.job.data.openlava.get('jidlist', [])) > 1:
    #    lastJids = sysConf.job.data.openlava.get('jidlist')[-1]

    if command == 'run':
        prep_jids = sysConf.job.data.openlava.jids.get('prepare', [])
        #hold until the 'prepare' jobs are done
        #l.critical("Prepare jids - wait for these! %s" % prep_jids)
        for j in prep_jids: 
            bsub_cl.extend(["-w", "'done(%d)'" % j])
    elif command == 'finish':
        run_jids = sysConf.job.data.openlava.jids.get('run', [])
        #hold until the 'prepare' jobs are done
        for j in run_jids: 
            bsub_cl.extend(["-w", "'done(%d)'" % j])

    #give it a reasonable name
    jobname = "%s/%s" % (str(conf['runid']), command)
    if conf.get('runid', None):
        bsub_cl.extend(["-J", jobname])
        #s("#BSUB-J %s" % jobname)

    # make sure the environment is copied
    #qcl.append('-V')
    #qcl.extend(cl)

    #print " ".join(qcl)
    #dump the configuration in the environment
    s("")
    s("## Defining moa specific environment variables")
    s("")
      
    for k in conf:
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

    s(*cl)

    #save the file
    tmpdir = os.path.join(wd, '.moa', 'tmp')
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    tmpfile = tempfile.NamedTemporaryFile(dir=tmpdir, prefix='openlava.', 
                                         delete=False, suffix='.sh')
    tmpfile.write("\n".join(sc))
    tmpfilename = os.path.realpath(os.path.abspath(tmpfile.name))
    tmpfile.close()
    os.chmod(tmpfile.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        
    l.debug("executing bsub")
    moa.ui.message("Submitting job to openlava")
    bsub_cl.append(tmpfilename)
    moa.ui.message("Executing")
    moa.ui.message(" ".join(map(str, bsub_cl)))
    p = sp.Popen(map(str, bsub_cl), cwd = wd, stdout=sp.PIPE)
    o,e = p.communicate()
    
    jid = int(o.split("<")[1].split(">")[0])

    if not sysConf.job.data.openlava.jids.has_key(command):
        sysConf.job.data.openlava.jids[command] = []

    moa.ui.message("submitted job with openlava job id %s " % jid)
    #store the job id submitted
    if not sysConf.job.data.openlava.jids.has_key(command):
            sysConf.job.data.openlava.jids[command] = []
    sysConf.job.data.openlava.jids[command].append(jid)
    l.debug("jids stored %s" % str(sysConf.job.data.openlava.jids))
    return p.returncode

def hook_postRun():
    """
    Need to exit here, and reconvene once all jobs have executed
    """
    #print sysConf.actor.openlava.jids

#ergister this actor globally
sysConf.actor.actors['openlava'] = openlavaRunner
sysConf.actor.openlava.jids = []
