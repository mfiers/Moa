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

A collection of functions that serve an API

Note that all doctests here are extremely basic - we only test if the
functions can be called - without error. Real testing of functionality
is in the respective modules

"""

import os
import sys

import moa.info
import moa.dispatcher
import moa.conf
import moa.template
from moa.logger import l

MOABASE = os.environ['MOABASE']

def getMoaBase():
    """
    Returns MOABASE

        >>> result = getMoaBase()
    
    """
    return moa.info.getMoaBase()


def isMoaDir(path):
    """
    Is directory 'path' a Moa directory?
    
        >>> result = isMoaDir(TESTPATH)
        
    """
    return moa.info.isMoaDir(path)

def isLocked(path):
    """
    Is a moa directory locked? (i.e. not allowed to execute)

        >>> result = isLocked(TESTPATH)
        
    """
    return moa.info.isLocked(path)
    
    
def getInfo(path):
    """
    Return information on a moa directory

        >>> result = getInfo(TESTPATH)

    """
    return moa.info.info(path)


def getParameter(path, key):
    """
    Get a parameter

        >>> demoPath = os.path.join(getMoaBase(), 'demo', 'test')
        >>> title = getParameter(demoPath, 'title')
        >>> type(title) == type('string')
        True
        >>> len(title) > 0
        True

        #see if it can handle non-moa directories
        >>> getParameter('/', 'title')
        False

        #and a non existing variable
        >>> result = getParameter(demoPath, 'NotExisitingParameter')
        >>> type(result) == type("")
        True
        >>> len(result) == 0
        True
        
    """
    return moa.conf.getVar(path, key)

def setParameter(path, key, value):
    """
    Set the parameter 'key' (in path x) to a cerain value
    
        >>> setParameter(TESTPATH, 'title', 'test setParameter')
        
    """    
    moa.conf.setVar(path, key, value, silent=True)


def appendParameter(path, key, value):
    """
    Append the value to parameter 'key' (in path x)

        >>> result = appendParameter(TESTPATH, 'title', 'b')
    """    
    moa.conf.setVar(path, key, value, silent=True)


def templateList():
    """
    Return a list of valid moa templates

        >>> result = templateList()
        
    """
    return moa.template.list()



#Depreacted - for a more uniform style of naming
def is_directory_moa(path):
    l.debug("is_directory_moa is deprecated!")
    return isMoaDir(path)

def get_moa_info(path):
    l.debug("is_directory_moa is deprecated!")
    return getMoaInfo(path)

def set_moa_parameter(path, key, value):
    moa.conf.setVar(path, key, value)

def get_moa_parameter(path, key):
    return getParameter(path, key)
