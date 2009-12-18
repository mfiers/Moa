#!/usr/bin/env python
# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
Moa script - utilities
"""

import os
import re
import sys
import time
import errno
import shutil
import contextlib

from moa.logger import l
from moa.exceptions import *

# Get a file lock, adapted from:
#  http://code.activestate.com/recipes/576572/
#
@contextlib.contextmanager
def flock(path, wait_delay=.1, max_wait=100):
    waited = 0
    waited_too_long = False
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            waited += wait_delay
            time.sleep(wait_delay)
            if waited > max_wait:
                waited_too_long = True
                break
            else:
                continue
        else:
            break
    if waited_too_long:
        raise CannotGetAFileLock(path)
    try:
        yield fd
    finally:
        os.unlink(path)

def exit(rc=0):
    for h in l.handlers:
        h.flush()
    sys.exit(rc)

def removeDirectory(path, silent=False):
    """
    dangerous utility - it complete deletes a directory

       >>> import tempfile
       >>> tempdir = tempfile.mkdtemp()
       >>> os.path.exists(tempdir)
       True
       >>> os.path.isdir(tempdir)
       True
       >>> removeDirectory(tempdir, silent=True)
       >>> os.path.exists(tempdir)
       False
       
    """
    if silent:
        l.debug("Removing %s" % path)
    else:
        l.warning("Removing %s" % path)
        
    shutil.rmtree(path)

    if silent:
        l.debug("Finished removing %s" % path)
    else:
        l.warning("Finished removing %s" % path)

