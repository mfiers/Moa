#!/usr/bin/env python
# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.resources
-------------

gets resources from the moa libraries

"""

import os
import sys
import pkg_resources
import moa.logger as l


def resourceExists(what):
    return pkg_resources.resource_exists(
        __name__, os.path.join('..', what)) \
        or \
        pkg_resources.resource_exists(
        __name__, os.path.join('..', '..', '..', what))
    
def getResource(what):
    """
    Gets a data file from the moa package.

    There are two possible locations where any resource could be,
    either three dirs up, or only one. This depends on if this a
    pypi (one dir up) package or the git package (three dirs up)
    """
    
    try:
        res = pkg_resources.resource_string(__name__, os.path.join('..', what))
    except IOError:
        #this is the git-package structure - bit inconvenient really
        res = pkg_resources.resource_string(
            __name__, os.path.join('..','..','..', what))
    return res

def listResource(what):
    """
    List a directory
    """
    
    if pkg_resources.resource_isdir(__name__, os.path.join('..', what)):
        what = os.path.join('..', what)
    else:
        what = os.path.join('..', '..', '..', what)

    return  pkg_resources.resource_listdir(__name__, what)
