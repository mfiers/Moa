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
from moa.sysConf import sysConf
import Yaco

## Load & handle plugins
class PluginHandler():

    def __init__(self):
        """
        Must be called with a global 'system configuration' object
        (Yaco)
        
        """
        ## Determine what plugins are loaded
        self.sysConf = sysConf
        self.pluginList = sysConf.getPlugins()
        #self.sysConf.plugins = self
        
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
                sysConf.plugins[plugin]['module'] = _m
                l.debug("Successfully Loaded module %s" % pyModule)
            except ImportError, e:
                if not str(e) == "No module named %s" % plugin:
                    raise
                #l.debug("No python plugin module found for %s" % plugin)
            
    def register(self, **kwargs):
        """
        Keep track of a dictionary of data that might be used by any
        of the plugins - this seems cleaner than relying on using
        globals. - or actually - we're relying on one global now -
        called sysConf.

        Think this is outdated -it is just as easy to manipulate
        sysConf directly.
        """
        for k in kwargs:
            self.sysConf[k] = kwargs[k]
            
    def run(self, command, reverse=False):
        rv = {}
        runOrder = self.pluginList
        if reverse:
            runOrder.reverse()
        for p in runOrder:
            m = sysConf.plugins[p].module
            if not hasattr(m, command):
                continue
            l.debug("plugin executing hook %s for %s" % (command, p))
            rv['p'] = getattr(m, command)(sysConf)
        return rv
            
    def runCallback(self, job, command):
        """
        Run a command callback 
        """
        commandInfo = sysConf.commands[command]
        commandInfo['call'](job)

    def getAttr(self, attribute):
        """
        A generator that returns all plugins and the
        requested attribute
        """
        for p in self.pluginList:
            a = getattr(sysConf.plugins[p], attribute, None)
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
