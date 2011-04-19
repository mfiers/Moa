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

sysConf = None

USERCONFIGFILE = os.path.join(os.path.expanduser('~'),
                          '.config', 'moa', 'config')

class SysConf(Yaco.Yaco):
    
    def __init__(self):
        
        
        super(SysConf, self).__init__(moa.utils.getResource('etc/config'))

        l.debug("Loading system config: %s" % USERCONFIGFILE)
        if os.path.exists(USERCONFIGFILE):
            self.load(USERCONFIGFILE)
              
    def getVersion(self):
        """
        Return the version number of this Moa instance
        """
        return moa.utils.getResource('VERSION').strip()

    
    def getPlugins(self):
        rv = self.get('plugins', [])
        for p in self.get('plugins_extra', []):
            if p in rv: continue
            rv.append(p)
        return rv

#This function is not necessary??? or is it??
def getPlugins():
    return sysConf.getPlugins()

if sysConf == None:
    sysConf = SysConf()
