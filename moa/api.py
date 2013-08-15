#!/usr/bin/env python
"""
functions that allow plugins to register API functions for use in other parts of the system
"""

import re
import copy
import argparse
import inspect
from moa.sysConf import sysConf

from Yaco import Yaco
import moa.ui
import moa.exceptions
import moa.utils
import moa.logger as l

#make sure api is i sysConf
if not 'api' in sysConf:
    sysConf.api = Yaco()


#
# Decorators - @api
#

def _apify(f, name):
    """
    Register the function
    """
    #try:
    #    assert(inspect.getargspec(f).args == ['job', 'args'])
    #except AssertionError:
    #    moa.ui.exitError(("Command function for %s seems invalid " +
    #                      "- contact a developer") % name)

    l.debug("registering command in the internal API %s" % name)
    _desc = f.__doc__.strip().split("\n", 1)

    if len(_desc) == 2:
        shortDesc, longDesc = _desc
        longDesc = longDesc
    else:
        shortDesc = _desc[0]
        longDesc = ''

    if longDesc:
        longDesc = moa.utils.removeIndent(longDesc)

    # sysConf.commands[name] = {
    #     'desc': shortDesc,
    #     'long': longDesc,
    #     'recursive': 'gbobal',
    #     'logJob': True,
    #     'needsJob': False,
    #     'call': f,
    #     'cp': cp,
    # }

    sysConf.api[name] = f

def api(f):
    """
    Decorator for any function in moa - name is derived from function name
    """
    return _apify(f, f.__name__)


def apiName(name):
    """
    Decorate a function as a moa command with the option to specify a
    name for the function
    """
    def decorator(f):
        return _apify(f, name)
    return decorator

