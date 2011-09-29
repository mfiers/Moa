# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.sysConf
-----------

Store Moa wide configuration

"""

import os
import sys

import Yaco
 
import moa.logger as l
import moa.utils
import moa.plugin

sysConf = None

USERCONFIGFILE = os.path.join(os.path.expanduser('~'),
                          '.config', 'moa', 'config')


class SysConf(Yaco.Yaco):
    
    def __init__(self):
        
        
        super(SysConf, self).__init__(moa.utils.getResource('etc/config'))

        l.debug("Loading system config: %s" % USERCONFIGFILE)
        if os.path.exists(USERCONFIGFILE):
            self.load(USERCONFIGFILE)

        #prepare the plugins
        self.pluginHandler = moa.plugin.PluginHandler(
            self, self.getPlugins())

    def initialize(self):
        self.pluginHandler.initialize()
        
        
    def getVersion(self):
        """
        Return the version number of this Moa instance
        """
        return moa.utils.getResource('VERSION').strip()

    
    def getPlugins(self):
        tmprv = []        
        for p in self.plugins:
            if self.plugins[p].get('enabled', True):
                tmprv.append((self.plugins[p].get('order', 100), p))
        tmprv.sort()
        return [x[1] for x in tmprv]
    

if sysConf == None:
    sysConf = SysConf()
