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
import moa.logger
import moa.conf
import moa.job

l = moa.logger.l

def _projectRoot(path):
    """
    Is this specific path a project root?    

    >>> moa.utils.removeFiles(P_EMPTY, recursive=True)
    >>> _projectRoot(P_EMPTY)
    False
    >>> moa.job.newJob(template = 'project',
    ...                title = 'test job creation',
    ...                wd=P_EMPTY)
    >>> _projectRoot(P_EMPTY)
    True
    >>> moa.utils.removeFiles(P_EMPTY, recursive=True)
    >>> moa.job.newJob(template = 'traverse',
    ...                title = 'test job creation',
    ...                wd=P_EMPTY)
    >>> _projectRoot(P_EMPTY)
    False
    """
    if not moa.info.isMoaDir(path):
        return False
    if moa.info.template(path) != 'project':
        return False
    return True

    
def findProjectRoot(path):
    """
    Find the project root of a certain moa job

    >>> moa.utils.removeFiles(P_EMPTY, recursive=True)
    >>> moa.job.newJob(template = 'project',
    ...                title = 'test project',
    ...                wd=P_EMPTY)
    >>> moa.job.newJob(template = 'traverse',
    ...                title = 'test job creation',
    ...                wd=os.path.join(P_EMPTY, 'test'))
    >>> os.path.exists(os.path.join(P_EMPTY, 'test', 'Makefile'))
    True
    >>> result = findProjectRoot(os.path.join(P_EMPTY, 'test'))
    >>> result[0]
    True
    >>> result[1] == P_EMPTY
    True
    >>> result[2] == 'test project'
    True

    @param path: The path for which we're looking for the project root
    @type path: string
    @returns: a tuple, first value indicates if there is a parent project
      the second is the path to the project, the third value is the project
      title
    @rtype: tuple of a boolean and two stringsg  
    """
    #are we looking at a directory?
    if not os.path.isdir(path):
        l.critical("findProjectRoot must be executed with a directory as ")
        l.critical(" argument, not with:")
        l.critical("  %s" % path)
        sys.exit(-1)

    #start walking up through the tree until we discover

    #remove trailing slash
    if path[-1] == '/':
        path = path[:-1]

    def splitDir(d):
        parent, this = os.path.split(d)
        return parent

    #start walking through the parent tree
    cwd = path
    while True:
        if _projectRoot(cwd):
            title = moa.info.getTitle(cwd)
            l.critical(title)
            return (True, cwd, title)
        cwd = splitDir(cwd)
