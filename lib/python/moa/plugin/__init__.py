#moa python plugins
"""
Handle Moa commands (i.e. anything that you can run as `moa COMMAND` on the
commandline
"""

import os
import sys
import UserDict
import moa.logger as l

## Load & handle plugins
class PluginHandler(UserDict.DictMixin):

    def __init__(self, plugins):

        ## Determine what plugins are loaded
        self.plugins = {}
        self.data = {}
        self.allPlugins = plugins
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
                #l.debug("No python plugin module found for %s" % plugin)

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

    def getAttr(self, attribute):
        """
        A generator that returns all plugins and the
        requested attribute
        """
        for p in self.keys():
            a = getattr(self[p], attribute, None)
            if a: yield p, a
        
    # Implement the basic functions for a dict
    #
    def __getitem__(self, item):
        return self.plugins[item]

    def __setitem__(self, item, value):
        self.plugins[item] = value

    def keys(self):
        return self.plugins.keys()

#Should I create a global placeholder for this moa run??
#moaPlugins = Plugins()

class BasePlugin:
    def __init__(self):
        self.data = {}

    def register(self, **kwargs):
        """
        Register a set of variables for use by the plugin
        """
        self.data.update(kwargs)
