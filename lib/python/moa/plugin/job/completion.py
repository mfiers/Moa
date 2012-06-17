# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**completion** - assists command line completion
------------------------------------------------

Caches a number of variables for command line completion

The data is cached in .moa/completion/*

"""

import os
import time
import socket
from datetime import datetime, timedelta
import subprocess as sp

import moa.logger 
l = moa.logger.getLogger(__name__)

from moa.sysConf import sysConf

def hook_finish(job):
    """
    cache!!
    """
    #print job, job.isMoa()rm
    if not job.isMoa():
        return

    compdir = os.path.join('.moa', 'completion')
    if not os.path.exists(compdir):
        os.makedirs(compdir)

    commandlist = sorted(sysConf.commands.keys())
    with open(os.path.join(compdir, 'commands'), 'w') as F:
        F.write(" ".join(commandlist))
        
    params = job.conf.getPublicParameters()
    with open(os.path.join(compdir, 'parameters'), 'w') as F:
        F.write(" ".join(params))
    return
        

