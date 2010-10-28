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
Handle projects

"""

import os
import re
import sys

import moa.utils
import moa.logger as l
import moa.conf
import moa.job

def _projectRoot(path):
    """
    Is this specific path a project root?    

    >>> wd = moa.job.newTestJob(template='project',
    ...                title = 'test job creation')
    >>> _projectRoot(wd)
    'project'
    >>> wd = moa.job.newTestJob(template='traverse',
    ...                title = 'traverse job creation')
    >>> _projectRoot(wd)
    'notproject'

    """
    if not moa.info.isMoaDir(path):
        return "out"
    template = moa.info.template(path)
    if template != 'project':
        return "notproject"
    return "project"

    
def findProjectRoot(path=None):
    """
    Find the project root of a certain moa job

    >>> wd = moa.job.newTestJob(template='project',
    ...                title = 'test job creation')
    >>> subdir = os.path.join(wd, 'test')
    >>> os.mkdir(subdir)
    >>> job = moa.job.newJob(subdir, template='traverse', title='test')
    >>> result = findProjectRoot(subdir)
    >>> result == wd
    True
    >>> None == findProjectRoot('/usr')
    True

    @param path: The path for which we're looking for the project root, if
      omitted, use the cwd
    @type path: string
    @returns: a tuple, first value indicates if there is a parent project
      the second is the path to the project, the third value is the project
      title
    @rtype: tuple of a boolean and two strings
    """
    if not path:
        path=os.getcwd()
        
    l.debug("Finding project root for %s" % path)
    
    #are we looking at a directory?
    if not os.path.isdir(path):
        l.critical("findProjectRoot must be executed with a directory as ")
        l.critical(" argument, not with:")
        l.critical("  %s" % path)
        sys.exit(-1)

    # start walking up through the tree until we discover

    # remove trailing slash - to make sure that os.path.split
    # works properly
    if path[-1] == '/':
        path = path[:-1]

    #start walking through the parent tree
    cwd = path
    while True:
        res = _projectRoot(cwd)
        if res == 'project':
            return cwd

        cwd = os.path.split(cwd)[0]
        # assuming that we're not creating moa jobs in the system root
        # if you do want to, I'm not going to cooperate.
        if cwd == '/': return None
