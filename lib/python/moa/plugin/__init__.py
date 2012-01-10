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

import copy
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
        attempt to load the python modules for each plugin
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
                moa.ui.exitError("Plugin %s is not installed" % plugin)
        
    
    def run(self, command, reverse=False):
        """
        Executing a plugin hook
        """
        rv = {}
        runOrder = copy.copy(self.pluginList)
        if reverse:
            runOrder.reverse()

        l.debug("plugin execution order %s" % ", ".join(runOrder))

        for p in runOrder:
            m = self.plugins[p].module
            if hasattr(m, command):
                l.warning("plugin %s has what looks like an invalid hook "
                          "(%s) definition" % (
                    p, command))
            if not m.__dict__.has_key('hook_' + command):
                continue

            l.debug("plugin executing hook %s for %s" % (command, p))
            #rv[p]= eval("m.hook_%s" % command)
            rv[p] = getattr(m, "hook_" + command)()
        return rv
            
    def execute(self, command):
        """
        Run a command callback 
        """
        self.run('prepare_3')
        self.run("pre%s" % command.capitalize())

        commandInfo = self.sysConf.commands[command]

        if not commandInfo.has_key('call'):
            raise Exception("Invalid command - no callback %s" % command) 

        commandInfo['call'](self.sysConf.job)
        
        self.run("post%s" % command.capitalize(), reverse=True)
        self.run('finish', reverse=True)


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
