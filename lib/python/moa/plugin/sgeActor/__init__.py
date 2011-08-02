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
import git 
import time
import optparse
import subprocess

from moa.sysConf import sysConf
import moa.logger as l
import moa.plugin.newjob

def hook_defineOptions():
    sysConf.parser.add_option( '--sge', action='store_const', const='sge',
                               dest='actorId', help='Use SGE as actor' )

def sgeRunner(wd, cl, conf={}, **kwargs):
    """
    Run the job using SGE

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """

    #see if we can get a command
    command = kwargs.get('command', 'unknown')
    if command == 'unknown':
        l.error("runner should be called with a command")

    outDir = os.path.join(wd, '.moa', 'log.latest')
    if not os.path.exists(outDir):
        try:
            os.makedirs(outDir)
        except OSError:
            pass

    #expect the cl to be nothing more than a single script to execute
    outfile = os.path.join(outDir, 'stdout')
    errfile = os.path.join(outDir, 'stderr')
    
    qcl = ['qsub']
    qcl.append('-S')
    qcl.append('/bin/bash')
    qcl.append('-cwd')
    qcl.append('-e')
    qcl.append(errfile)
    qcl.append('-o')
    qcl.append(outfile)

    if command == 'run':
        prep_jids = sysConf.job.data.sge.jids.get('prepare', [])
        #hold until the 'prepare' jobs are done
        if prep_jids: 
            qcl.append('-hold_jid')
            qcl.append(','.join(map(str, prep_jids)))
    elif command == 'finish':
        run_jids = sysConf.job.data.sge.jids.get('run', [])
        #hold until the 'prepare' jobs are done
        if run_jids: 
            qcl.append('-hold_jid')
            qcl.append(','.join(map(str, run_jids)))

    #give it a reasonable name
    if conf.get('runid', None):
        qcl.append('-N')
        qcl.append(str(conf['runid']))

    # make sure the environment is copied
    qcl.append('-V')
    qcl.extend(cl)

    print " ".join(qcl)
    #dump the configuration in the environment
    for k in conf:
        # to prevent collusion, prepend all env variables
        # with 'moa_'
        outk = 'moa_' + k
        v = conf[k]
        if isinstance(v, list):
            os.putenv(outk, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(outk, str(v))

    l.debug("executing %s" % " ".join(qcl))
    moa.ui.message("executing %s" % " ".join(qcl))
    p = subprocess.Popen(qcl, cwd = wd, stdout=subprocess.PIPE)
    o, e = p.communicate()
    jid = int(o.strip().split()[2])
    sysConf.actor.sge.jids.append(jid)
    moa.ui.message("submitted job with sge job id %s " % jid)

    #store the job id submitted
    if not sysConf.job.data.sge.jids.has_key(command):
            sysConf.job.data.sge.jids[command] = []
    sysConf.job.data.sge.jids[command].append(jid)
    return p.returncode

def hook_postRun():
    """
    Need to exit here, and reconvene once all jobs have executed
    """
    #print sysConf.actor.sge.jids

sysConf.actor.actors['sge'] = sgeRunner
sysConf.actor.sge.jids = []
