# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.commands
============

Handle Moa commands (i.e. anything that you can run as `moa COMMAND` on the
commandline


.. todo::
    See if this module can go. It doesn't seem to be doing much. If it
    stays - convert to Yaco.
   
"""

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

    def getAll(self):
        return self.commands.keys()
        
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

