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

## def hook_defineCommands():
 #    sysConf['commands']['history'] = {
 #        'desc' : 'display a version control log',
 #        'call': gitlog
 #        }
 #    sysConf['commands']['tag'] = {
 #        'desc' : 'Tag the current version',
 #        'call': tag
 #        }

def hook_defineOptions():
    sysConf.parser.add_option( '--sge', action='store_const', const='sge',
                               dest='actorId', help='Use SGE as actor' )

def sgeRunner(wd, cl, conf={}):
    """
    Run the job using SGE

    what does this function do?
    - put env in the environment
    - Execute the commandline (in cl)
    - store stdout & stderr in log files
    - return the rc
    """
    
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
    qcl.append('-V')
    qcl.extend(cl)

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
    jid = o.strip().split()[2]
    sysConf.actor.sge.jids.append(jid)
    moa.ui.message("submitted job with sge job id %s " % jid)

    return p.returncode

def hook_postRun():
    """
    Need to exit here, and reconvene once all jobs have executed
    """
    print sysConf.actor.sge.jids

sysConf.actor.actors['sge'] = sgeRunner
sysConf.actor.sge.jids = []
