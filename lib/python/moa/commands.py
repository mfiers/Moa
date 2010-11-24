#!/usr/bin/env python
#
# Copyright 2009 Mark Fiers
# Plant & Food Research
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
moa.commands
============

Handle Moa commands (i.e. anything that you can run as `moa COMMAND` on the
commandline

"""

import os
import sys
import textwrap
import UserDict
import moa.logger as l


## Command definitions
class Commands(UserDict.DictMixin):

    def __init__(self):
        self.commands = {}

    #
    # Implement the basic functions for a dict
    #
    def __getitem__(self, item):
        return self.commands[item]

    def __setitem__(self, item, value):
        self.commands[item] = value

    def keys(self):
        rv = []
        for k in self.commands.keys():
            if not self.commands[k].get('private', False):
                rv.append(k)
        return rv

    def hasCallback(self, command):
        if self[command].has_key('call') and \
           type(self[command]['call']) == types.FunctionType:
            return True
        else:
            return False
        
    def executeCallback(self, invocation):
        c = self[i.command]
        self[c]['call'](i)
    
    
    def generateUsageString(self, usageHeader):
        u = usageHeader
        commands = self.keys()
        commands.sort()
        for _c in commands:
            if self[_c].get('private', False):
                continue
            u += "\n".join(
                textwrap.wrap(
                    '%s: %s' % (_c, self[_c]['desc']),
                    initial_indent=' - ',
                    subsequent_indent = '     ')) + "\n"
        return u

