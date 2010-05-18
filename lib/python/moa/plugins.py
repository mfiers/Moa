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
Handle Moa commands (i.e. anything that you can run as `moa COMMAND` on the
commandline
"""

import os
import sys
import UserDict
import moa.info
from moa.logger import l
from moa.commands import moaCommands

## Load & handle plugins
class MOAPLUGINS(UserDict.DictMixin):

    def __init__(self):
        ## Determine what plugins are loaded
        self.plugins = {}
        self.allPlugins = moa.info.getPlugins()        
        l.debug("Plugins %s" % self.allPlugins)
        ## load the plugins as seperate modules. A plugin does not need to
        self.initialize()

    def initialize(self):
        """
        attempt to load the python part of the plugins
        """
        ## do we have a python module??
        l.debug('Start plugin initalization')
        for plugin in self.allPlugins:
            pyModule = 'moa.plugin.%s' % plugin
            try:
                _m =  __import__( pyModule, globals(), locals(), ['git'], -1)
                self.plugins[plugin] = _m
                l.debug("Successfully Loaded module %s" % pyModule)
            except ImportError, e:
                if not str(e) == "No module named %s" % plugin:
                    raise
                l.debug("No python plugin module found for %s" % plugin)

    def registerCommands(self, moaCommands):
        for p in self.loadedPlugins(hasFunction='defineCommands'):
            l.critical("command registration for %s" % p)
            p.defineCommands(moaCommands)

    def registerOptions(self, parser):
        for p in self.loadedPlugins(hasFunction='defineOptions'):
            p.defineOptions(parser)

    def prepare(self, moaInvocation):
        for p in self.loadedPlugins(hasFunction='prepare'):
            p.prepare(moaInvocation)


    # Implement the basic functions for a dict
    #
    def __getitem__(self, item):
        return self.plugins[item]

    def __setitem__(self, item, value):
        self.plugins[item] = value

    def keys(self):
        return self.plugins.keys()

    def loadedPlugins(self, hasFunction=None):
        """
        Returns a loaded plugin modules
        """
        for p in self.allPlugins:
            if not self.has_key(p): continue
            if hasFunction and \
               not hasFunction in dir(p):
                l.critical('ignoring %s' % p
                continue            
            yield self[p]

#Create a global placeholder for this moa run
moaPlugins = MOAPLUGINS()

