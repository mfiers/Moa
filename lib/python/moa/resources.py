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
import pkg_resources
import moa.logger

l = moa.logger.getLogger(__name__)


def resourceExists(what):

    in_package = pkg_resources.resource_exists(
        __name__, os.path.join('..', what)) \
        or \
        pkg_resources.resource_exists(
            __name__, os.path.join('..', '..', '..', what))

    if in_package:
        return True

    if os.path.exists(os.path.join('/usr/local/share/moa', what)):
        return True

    return False


def getResource(what):
    """
    Gets a data file from the moa package.

    There are two possible locations where any resource could be,
    either three dirs up, or only one. This depends on if this a
    pypi (one dir up) package or the git package (three dirs up)
    """

    try:
        res = pkg_resources.resource_string(__name__, os.path.join('..', what))
        return res
    except IOError:
        pass

    try:
        # old package structure - or so I'm afraid
        res = pkg_resources.resource_string(
            __name__, os.path.join('..', '..', '..', what))
        return res
    except:
        pass

    usl = os.path.join('/usr/local/share/moa', what)
    if os.path.exists(usl):
        with open(usl) as F:
            res = F.read()
        return res

    raise IOError


def listResource(what):
    """
    List a directory
    """
    usl = os.path.join('/usr/local/share/moa', what)

    if pkg_resources.resource_isdir(__name__, os.path.join('..', what)):
        what = os.path.join('..', what)
        return  pkg_resources.resource_listdir(__name__, what)
    elif pkg_resources.resource_isdir(__name__,
                                      os.path.join('..', '..', '..', what)):
        what = os.path.join('..', '..', '..', what)
        return  pkg_resources.resource_listdir(__name__, what)
    elif os.path.exists(usl):
        return  os.listdir(usl)






