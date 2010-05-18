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
Define moa hooks
"""

import os
from moa.exceptions import *
import moa.info
import moa.logger
l = moa.logger.l

moaHooks = {}

def _getHookName(when, command):
    """
    Determine the name of this function hook
    """
    
    if not when in ['before', 'after']:
        l.critical("invalid hook definition: %s" % when)
        sys.exit(-1)

    if when == 'before':
        hookName = 'pre%s' % command.capitalize()
    else:
        hookName = 'post%s' % command.capitalize()

    return hookName

def add(when, command, function):
    """
    store a function hook for later execution
    """
    hookName = _getHookName(when, command)
    
    if not moaHooks.has_key(hookName):
        moaHooks[hookName] = []
    moaHooks[hookName].append(function)

def run(when, command, g):
    """
    Execute the hookds
    """
    hookName = _getHookName(when, command)
    for f in moaHooks.get(hookName, []):
        f(g)
