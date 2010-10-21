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
import moa.logger as l

## Load & handle plugins
class Plugins(UserDict.DictMixin):

    def __init__(self):
        ## Determine what plugins are loaded
        self.plugins = {}
        self.data = {}
        self.allPlugins = moa.info.getPlugins()        
        l.debug("Plugins %s" % ", ".join(self.allPlugins))
        ## load the plugins as seperate modules. A plugin does not need to
        self.initialize()

    def initialize(self):
        """
        attempt to load the python part of the plugins
        """
        ## do we have a python module??
        l.debug('Start plugin init')
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

    def register(self, **kwargs):
        """
        Keep track of a dictionary of data that might be used
        by any of the plugins - this seems cleaner than relying
        on using globals
        """
        self.data.update(kwargs)
            
    def run(self, command):
        for p in self.keys():
            if not command in dir(self[p]):
                continue
            l.debug("plugin executing hook %s for %s" % (command, p))
            getattr(self[p], command)(self.data)
            
    def runCallback(self, command):
        """
        Run a plugin callback 
        """
        command['call'](self.data)
            
    # Implement the basic functions for a dict
    #
    def __getitem__(self, item):
        return self.plugins[item]

    def __setitem__(self, item, value):
        self.plugins[item] = value

    def keys(self):
        return self.plugins.keys()

#Should I create a global placeholder for this moa run??
moaPlugins = Plugins()

