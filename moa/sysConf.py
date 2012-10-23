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

import Yaco

import moa.logger as l
import moa.resources
import moa.plugin

sysConf = None

USERCONFIGFILE = os.path.join(os.path.expanduser('~'),
                              '.config', 'moa', 'config')


class SysConf(Yaco.Yaco):

    def __init__(self):

        if os.path.exists('/etc/moa/config'):
            with open('/etc/moa/config') as F:
                super(SysConf, self).__init__(F.read())
        else:
            #try the local package
            super(SysConf, self).__init__(
                moa.resources.getResource('etc/config'))

        l.debug("Loading system config: %s" % USERCONFIGFILE)
        if os.path.exists(USERCONFIGFILE):
            self.load(USERCONFIGFILE)

        #assign a runId
        runid = '.moa/last_run_id'
        if os.path.exists(runid):
            lri = open(runid).read().strip()
        else:
            lri = 1

    def getUser(self):
        """
        Get a Yaco representation of the user configuration file
        """
        rv = Yaco.Yaco()
        if os.path.exists(USERCONFIGFILE):
            rv.load(USERCONFIGFILE)
        return rv

    def saveUser(self, conf):
        """
        Save the conf Yaco object as the user config
        """
        conf.save(USERCONFIGFILE)

    def getVersion(self):
        """
        Return the version number of this Moa instance
        """
        return moa.resources.getResource('VERSION').strip()


if sysConf is None:
    sysConf = SysConf()
