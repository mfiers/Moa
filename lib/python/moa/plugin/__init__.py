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
import moa.logger
import Yaco
import sys

l = moa.logger.getLogger(__name__)


## Load & handle plugins
class PluginHandler():

    def __init__(self, config):
        """
        Manage the plugins
        """
        self.config = config
        self.pluginList = self.getPluginOrder()
        self.initialize()
        
    def getPluginOrder(self):
        tmprv = []        
        for p in self.config:
            if self.config[p].get('enabled', True):
                tmprv.append((self.config[p].get('order', 100), p))
        return [x[1] for x in sorted(tmprv)]
        
    def initialize(self):
        """
        attempt to load the python modules for each plugin
        """
        
        ## do we have a python module??
        l.debug('Start plugin init')
        for plugin in self.pluginList:
            self.config[plugin] = Yaco.Yaco()

            pyModule = self.config[plugin].module

            try:
                l.debug("trying to load module %s" % pyModule)
                #print plugin, pyModule
                _m =  __import__( pyModule, globals(), locals(), ['git'], -1)
                self.config[plugin]['loaded_module'] = _m
                l.debug("Successfully Loaded module %s" % pyModule)
            except ImportError, e:
                sys.stderr.write("ERROR - Plugin %s is not (properly) installed\n" % plugin)
                if '-v' in sys.argv or '-vv' in sys.argv:
                    raise
                sys.exit(-1)
        
    
    def run(self, command, reverse=False, only=[], **kwargs):
        """
        Executing a plugin hook

        possibly in `reverse` order
        possiby only plugins in the `only` list
        """
        #import traceback
        #print '~' * 80
        #print "\n".join(traceback.format_stack()[-4:-1])
        #print 'calling ', command
        rv = {}
        runOrder = copy.copy(self.pluginList)
        if reverse:
            runOrder.reverse()

        l.debug("plugin command run of hook %s" % command)
                        

        for p in runOrder:
            if only and not p in only:
                continue

            plugin_info = self.config[p]
            if not plugin_info:
                sys.stderr.write("ERROR - potential problem with plugin %s" % p)
                sys.exit()

            m = plugin_info['loaded_module']
            

            if not m.__dict__.has_key('hook_' + command):
                continue


            l.debug("plugin executing hook %s for %s" % (command, p))
            #rv[p]= eval("m.hook_%s" % command)
            rv[p] = getattr(m, "hook_" + command)(**kwargs)
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
