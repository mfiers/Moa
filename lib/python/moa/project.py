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
import moa.job

def _projectRoot(job):
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

    if not job.isMoa():
        return "out"

    template = job.template
    if template.name != 'project':
        return "notproject"
    
    return "project"

    
def findProjectRoot(job):
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
        
    l.debug("Finding project root for job in %s" % job.wd)
    
    # start walking up through the tree until we discover

    #start walking through the parent tree
    lookAt = job
    while True:
        res = _projectRoot(lookAt)
        if res == 'project':
            return lookAt

        newPath = os.path.split(lookAt.wd)[0]
        
        if newPath == '/':
            return None
        
        lookAt = moa.job.getJob(newPath)
        
        # assuming that we're not creating moa jobs in the system root
        # if you do want to, I'm not going to cooperate.
        if lookAt.wd == '/': return None
