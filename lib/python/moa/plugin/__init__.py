# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 

"""
Handle Moa commands (i.e. anything that you can run as `moa COMMAND` on the
commandline
"""

import UserDict
import moa.logger as l

import Yaco

## Load & handle plugins
class PluginHandler(UserDict.DictMixin):

    def __init__(self, sysConf):
        """
        Must be called with a global 'system configuration' object
        (Yaco)
        
        """
        ## Determine what plugins are loaded
        self.sysConf = sysConf
        self.pluginList = sysConf.getPlugins()
        self.plugins = {}
        self.sysConf.plugins = self
        
        l.debug("Plugins %s" % ", ".join(self.pluginList))
        ## load the plugins as seperate modules. A plugin does not need to
        self.initialize()

    def initialize(self):
        """
        attempt to load the python part of the plugins
        """
        ## do we have a python module??
        l.debug('Start plugin init')
        for plugin in self.pluginList:
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
        for k in kwargs:
            self.sysConf[k] = kwargs[k]
            
    def run(self, command, reverse=False):
        rv = {}
        toRun = self.pluginList
        if reverse:
            toRun.reverse()
        for p in toRun:
            if not command in dir(self[p]):
                continue
            l.debug("plugin executing hook %s for %s" % (command, p))
            rv['p'] = getattr(self[p], command)(self.sysConf)
        return rv
            
    def runCallback(self, job, command):
        """
        Run a command callback 
        """
        commandInfo = self.sysConf.commands[command]
        commandInfo['call'](job)

    def getAttr(self, attribute):
        """
        A generator that returns all plugins and the
        requested attribute
        """
        for p in self.pluginList:
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
