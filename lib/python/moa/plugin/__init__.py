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
        successfully_loaded = []
        for plugin in self.pluginList:
            l.debug("Loading plugin %s" % plugin)
            self.config[plugin] = Yaco.Yaco()
            pyModule = self.config[plugin].module
            try:
                #print plugin, pyModule
                _m = __import__(pyModule, globals(), locals(), ['git'], -1)
                self.config[plugin]['loaded_module'] = _m
                successfully_loaded.append(pyModule)
            except ImportError:
                sys.stderr.write(
                    "ERROR - Plugin %s is not (properly) installed\n" % plugin)
                if '-v' in sys.argv or '-vv' in sys.argv:
                    raise
                else:
                    sys.exit(-1)
        l.debug("loaded module %s" % ", ".join(successfully_loaded))

    def run(self, command, reverse=False, only=[], **kwargs):
        """
        Executing a plugin hook

        :param reverse: execute in reverse order
        :param only: execute only the plugins in this list
        :param **kwargs: pass these parameters on to the plugin function
        """
        rv = {}
        runOrder = copy.copy(self.pluginList)
        if reverse:
            runOrder.reverse()

        executed_in = []
        for p in runOrder:
            if only and not p in only:
                continue

            plugin_info = self.config[p]
            if not plugin_info:
                sys.stderr.write(
                    "ERROR - potential problem with plugin %s" % p)
                sys.exit()

            m = plugin_info['loaded_module']

            if not 'hook_' + command in m.__dict__:
                continue

            rv[p] = getattr(m, "hook_" + command)(**kwargs)
            executed_in.append(p)

        if len(executed_in) > 0:
            l.debug("Executed hook %s in %s" % (
                command, ", ".join(executed_in)))
        return rv

    def execute(self, command):
        """
        Run a command callback
        """
        self.run('prepare_3')
        self.run("pre%s" % command.capitalize())

        commandInfo = self.sysConf.commands[command]

        if not call in commandInfo:
            raise Exception(
                "Invalid command - no callback %s" % command)

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
            if a:
                yield p, a


class BasePlugin:
    def __init__(self):
        self.data = {}

    def register(self, **kwargs):
        """
        Register a set of variables for use by the plugin
        """
        self.data.update(kwargs)
