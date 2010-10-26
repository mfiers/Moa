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
Job
"""

import os
import re
import sys
import tempfile

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils
import moa.runMake

import moa.job.base
import moa.job.gnumake
import moa.job.nojob

def getJob(wd):
    """
    Utility funtion to instantiate the correct job class

    Currently, 'there is only one' (that is a Gnu Makefile based
    job
    """
    makefile = os.path.join(wd, 'Makefile')
    if os.path.exists(makefile):
        return moa.job.gnumake.GnuMakeJob(wd)
    else:
        return moa.job.nojob.NoJob(wd)

def newJob(wd, **kwargs):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type
    """

    job = moa.job.gnumake.GnuMakeJob(wd)
    job.new(**kwargs)
    return job                   
    
def newTestJob(*args, **kwargs):
    """
    Test function - creates a temp directory and uses that to
    instantiate the job in. This function returns the directory where
    the job is created. All parameters are passed on to L{newJob}

        >>> d = newTestJob('traverse')
        >>> type(d) == type('hi')
        True
        >>> os.path.exists(d)
        True
        >>> os.path.exists(os.path.join(d, 'Makefile'))
        True
        >>> job = moa.runMake.MOAMAKE(wd = d, captureErr=True)
        >>> rc = job.run()
        >>> type(rc) == type(1)
        True
    
    @returns: The directory where the job was created
    @rtype: string
    """

    wd = tempfile.mkdtemp()
    if args:
        kwargs['template'] = args[0]               
    job = newJob(wd, **kwargs)
    return wd

