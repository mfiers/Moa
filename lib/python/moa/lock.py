#!/usr/bin/env python
# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
Job locking utilities
"""

import os
from moa.exceptions import *

def lockJob(d):
    """
    Lock a moa directory

        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> lockJob(jobdir)
        >>> os.path.exists(os.path.join(jobdir, 'lock'))
        True
        >>> unlockJob(jobdir)
        >>> os.path.exists(os.path.join(jobdir, 'lock'))
        False
    """
    if not moa.info.isMoaDir(d):
        raise NotAMoaDirectory(d)

    lockFile = os.path.join(d, 'lock')
    
    if os.path.exists(lockFile):
        return True
    
    if not os.access(d, os.W_OK):
        raise MoaPermissionDenied(wd)

    with file(lockFile, 'a'):
        os.utime(lockFile, None)

def unlockJob(d):
    """
    Unlock a moa directory

        >>> import tempfile
        >>> import moa.job
        >>> emptyDir = tempfile.mkdtemp()
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> lockJob(jobdir)
        >>> unlockJob(jobdir)
        >>> os.path.exists(os.path.join(jobdir, 'lock'))
        False
        >>> try:
        ...     unlockJob(emptyDir)
        ...     False
        ... except NotAMoaDirectory: True
        ... except: False
        True
        
    """
    if not moa.info.isMoaDir(d):
        raise NotAMoaDirectory(d)

    lockfile = os.path.join(d, 'lock')
    if not os.path.exists(lockfile):
        return True

    if not os.access(lockfile, os.W_OK):
        raise MoaPermissionDenied(d)
    
    os.unlink(lockfile)
