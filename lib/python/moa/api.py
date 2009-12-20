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
moa API

A collection of functions forming the MOA API

"""
__docformat__ = "restructuredtext en"
__authors__ = "Mark Fiers, William Demchick"

import os
import sys

import moa.info
import moa.dispatcher
import moa.conf
import moa.job
from moa.exceptions import *
from moa.logger import l

MOABASE = os.environ['MOABASE']

def getMoaBase():
    """
    Returns the value of the MOABASE environment variable. MOABASE
    should point to the root of the Moa installation

    >>> r = getMoaBase()
    >>> type(r) == type('')
    True
    >>> os.path.exists(os.path.join(r, 'bin', 'moa'))
    True

    :returns: MOABASE
    :rtype: String
    """
    return moa.info.getMoaBase()


def isMoaDir(wd):
    """
    Is directory 'wd' a Moa directory?
    
    >>> isMoaDir(TESTPATH)
    True
    >>> isMoaDir(NOTMOADIR)
    False

    :param wd: directory to check
    :type wd: String
    :returns: is wd a Moa directory
    :rtype: Boolean    
    """
    return moa.info.isMoaDir(wd)

def status(wd):
    """
    Returns the status of a directory. It will return a one of the following status messages:

    - notadir - this is not an accessible directory
    - notmoa - this is not a moa directory
    - waiting - a moa job, not doing anything
    - running - this is a moa job & currently executing (runlock exists)       
    - locked - this job is locked (i.e. a lock file exists)

    >>> result = status(TESTPATH)
    >>> result in ['waiting', 'locked', 'running']
    True
    >>> result = status(NOTMOADIR)
    >>> result == 'notmoa'
    True

    :param wd: Directory to return the status of
    :type wd: String
    """
    return moa.info.status(wd)
    
def getInfo(wd):
    """
    Return information on a moa directory with the following keys:

        moa_targets
           A list of callable targets for this job (i.e. you can use
           by running ``moa TARGET``
        moa_description
           A short description (from the job template) what this job
           aims to do
        parameters
          A dictionary of parameters for this job. The keys in this
          dictionary is the name of the parameter

    Each parameter values is again a dictionary with following keys:

        mandatory    
          This parameter is mandatory. If not provided, execution will
          fail (Boolean)      
        help    
          A short help text explaining the function of this parameter
          (String)
        default
          The default value of this parameter, if applicable (String)      
        value
          The current value of this parameter (String)          
        cardinality        
          (``one`` or ``many``). The cardinality desribes how many
          values a parameter is allowed to have. In the case of
          ``one``, this parameter expects only one value. If
          cardinality if ``many``, the parameter accepts multiple
          values. It is important to note that GNU Make defines lists
          as a space separated string - a sentence is automatically a
          list of variables. There is no way to distinguish between a
          cardinality ``one`` parameter with as value ``a b c`` and a
          cardinality ``many`` parameter with the values [``a``,
          ``b``, ``c``].           
        type
          (string) The type of this variables. can be:
          
          - ``string``
          - ``directory``
          - ``file``
          - ``float``
          - ``integer``
          - ``set``

          Note that there is currently no type checkin in the moa core.
        allowed    
          (array) A list of allowed values, if of type set


    >>> result = getInfo(TESTPATH)
    >>> type(result) == type({})
    True
    >>> result.has_key('moa_targets')
    True
    >>> result.has_key('moa_description')
    True
    >>> result.has_key('parameters')
    True
    >>> parameters = result['parameters']
    >>> parameters.has_key('title')
    True
    >>> p_title = parameters['title']
    >>> p_title.has_key('category') and p_title.has_key('mandatory')
    True
    >>> p_title.has_key('help') and p_title.has_key('default')
    True
    >>> p_title.has_key('value') and p_title.has_key('allowed')
    True
    >>> p_title.has_key('cardinality') and p_title.has_key('type')
    True
    >>> try: result2 = getInfo('NOTAMOADIR')
    ... except NotAMoaDirectory: 'ok!'
    'ok!'
    
    :param wd: Directory to get information from
    :type wd: String
    :returns: information on the job
    :rtype: Dictionary
    :raises NotAMoaDirectory: If wd is not a moa directory
    """
    return moa.info.info(wd)


def getParameter(wd, key):
    """
    Gets a parameter from a Moa job.

    This function reads the value of parameter 'key' from the moa.mk
    file. If 'path' is not a folder.

    When requesting a non-existing parameter, the function returns an
    empty string. This is the fastest solution. If you want to know if
    a parameter exists, use the `getInfo` function.

    >>> title = getParameter(TESTPATH, 'title')
    >>> type(title) == type('string')
    True
    >>> len(title) > 0
    True
    >>> try: getParameter('/', 'title')
    ... except NotAMoaDirectory: 'ok!'
    'ok!'
    >>> result = getParameter(TESTPATH, 'NotExisitingParameter')
    >>> type(result) == type("")
    True
    >>> len(result) == 0
    True

    :param wd: directory to get a parameter from
    :type wd: String
    :param key: Name of the parameter to retrieve (for example 'title')
    :type key: String
    :returns: The value of the parameter
    :rtype: String
    :raises NotAMoaDirectory: If ``wd`` is not a Moa directory.
    """
    return moa.conf.getVar(wd, key)

def setParameter(wd, key, value):
    """
    Set a parameter

    Set the parameter ``key`` in path ``wd`` to value ``value``.
    
    >>> setParameter(TESTPATH, 'title', 'test setParameter')

    :param wd: the Moa directory to use
    :type wd: String
    :param key: The name of the parameter to set
    :type key: String
    :param value: The value to set the parameter to.
    :type value: String
    :raises NotAMoaDirectory: If ``wd`` is not a Moa directory.
        
    """    
    moa.conf.setVar(wd, key, value)


def appendParameter(wd, key, value):
    """
    Append the value to parameter 'key' (in path x)

        >>> result = appendParameter(TESTPATH, 'title', 'b')
    """    
    moa.conf.setVar(wd, key, value)


def templateList():
    """
    Return a list of valid moa templates

        >>> result = templateList()
        
    """
    return moa.job.list()

def newJob(*args, **kwargs):
    """
    Creates a new job

        >>> removeMoaFiles(EMPTYDIR)
        >>> newJob('traverse',
        ...        title = 'test creating of jobs',
        ...        directory=EMPTYDIR)
        >>> removeMoaFiles(EMPTYDIR)
        
    """
    moa.job.newJob(*args, **kwargs)

def removeMoaFiles(wd):
    """
    Removes moa related files from a directory (but leaves all other
    files in place). The function deletes the following files:
    
    - Makefile
    - moa.mk
    - lock
    - moa.runlock

    The function does not check if `wd` is a moa directory or not.

    >>> makefile = os.path.join(EMPTYDIR, 'Makefile')
    >>> moamk = os.path.join(EMPTYDIR, 'moa.mk')
    >>> newJob('traverse',
    ...        directory=EMPTYDIR,
    ...        title='test removeMoaFiles')
    >>> removeMoaFiles(EMPTYDIR)
    >>> os.path.exists(os.path.join(EMPTYDIR, 'Makefile'))
    False
    >>> os.path.exists(os.path.join(EMPTYDIR, 'moa.mk'))
    False
    >>> removeMoaFiles(NOTMOADIR)
    
    
    :param wd: The pathname of the directory from which the Moa
        files are to be removed
    :type wd: String
    """
    moa.utils.removeMoaFiles(wd)


#Depreacted, these will be removed once William has changed his code
def is_directory_moa(wd):
    l.debug("is_directory_moa is deprecated!")
    return isMoaDir(wd)

def get_moa_info(wd):
    l.debug("is_directory_moa is deprecated!")
    return getMoaInfo(wd)

def set_moa_parameter(wd, key, value):
    moa.conf.setVar(wd, key, value)

def get_moa_parameter(wd, key):
    return getParameter(wd, key)
