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
class PluginHandler():

    def __init__(self, sysConf, pluginList):
        """
        Manage the plugins
        """

        self.plugins = {}
        self.pluginList = pluginList
        self.sysConf = sysConf
        
    def initialize(self):
        """
        attempt to load the python part of the plugins
        """
        ## do we have a python module??
        l.debug('Start plugin init')
        for plugin in self.pluginList:
            self.plugins[plugin] = Yaco.Yaco()

            pyModule = 'moa.plugin.%s' % plugin
            try:
                _m =  __import__( pyModule, globals(), locals(), ['git'], -1)
                self.plugins[plugin]['module'] = _m
                l.debug("Successfully Loaded module %s" % pyModule)
            except ImportError, e:
                if not str(e) == "No module named %s" % plugin:
                    raise
                #l.debug("No python plugin module found for %s" % plugin)
            
    def run(self, command, reverse=False):
        """
        Executing a plugin hook
        """
        rv = {}
        runOrder = self.pluginList
        if reverse:
            runOrder.reverse()
        for p in runOrder:
            m = self.plugins[p].module
            if hasattr(m, command):
                l.warning("plugin %s has what looks like an invalid hook (%s) definition" % (
                    p, command))
            if not hasattr(m, 'hook_' + command):
                continue
            l.debug("plugin executing hook %s for %s" % (command, p))
            rv[p] = getattr(m, "hook_" + command)()
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
            a = getattr(self.plugins[p], attribute, None)
            if a: yield p, a

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
