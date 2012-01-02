# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**archive** - pack / unpack Moa trees 
-------------------------------------

"""

import os
import sys
import glob
import tarfile

from moa.sysConf import sysConf
import moa.ui
import moa.logger as l
import moa.plugin.newjob

def hook_defineCommands():
    sysConf['commands']['pack'] = {
        'desc' : 'pack a moa tree',
        'call': pack
        }
    sysConf['commands']['unpack'] = {
        'desc' : 'unpack a moa tree',
        'call': unpack
        }

def _findPackName(job, packdir):
    """
    Find a name for the pack archive
    """
    packname = os.path.join(packdir, '%s.moa.tar.gz' % job.conf.jobid)
    i = 0
    while os.path.exists(packname):
        i += 1
        packname = os.path.join(packdir, '%s.%2d.moa.tar.gz' % (job.conf.jobid,i))
    return packname
    
def pack(job):
    """
    
    """
    args = sysConf.args
    if len(args) == 1:
        packdir = os.path.expanduser(sysConf.plugins.pack.get('dir', '~'))
    else:
        packdir = os.path.expanduser(args[1])
        if not os.path.isdir(packdir):
            moa.ui.exitError("target directory (%s) does not exist" % packdir)

    if not os.path.exists(packdir):
        moa.ui.message("Creating directory for Moa packs at %s" % packdir)
        os.makedirs(packdir)
        
    packfile = _findPackName(job, packdir)
    moa.ui.message('Storing archive at: %s' % packfile)
    

def unpack():
    pass
