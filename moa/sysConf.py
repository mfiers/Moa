# Copyright 2009-2012 Mark Fiers
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
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pkg_resources


import Yaco

import moa.logger
import moa.plugin

l = moa.logger.getLogger(__name__)
sysConf = None

#user configuration file ~/.config/moa/config
USERCONFIGFILE = os.path.join(os.path.expanduser('~'),
                              '.config', 'moa', 'config')

#system wide configuration file: /etc/moa/config
SYSCONFIGFILE = os.path.join('etc', 'moa', 'config')

def _interpret_var(v):
    try:
        return int(v)
    except:
        pass
    try:
        return float(v)
    except:
        pass

    if v.lower() == 'true':
        return True
    if v.lower() == 'false':
        return False

    return '"%s"' % v


class SysConf(Yaco.Yaco):

    def __init__(self):
        #first load the package default
        l.debug("loading package configuration file")
        super(SysConf, self).__init__(
            pkg_resources.resource_string('moa', 'data/etc/config'))

        #then see if the system config file exists
        if os.path.exists(SYSCONFIGFILE):
            l.debug("loading system configuration file")
            self.load(SYSCONFIGFILE)

        #and the user config file
        if os.path.exists(USERCONFIGFILE):
            l.debug("loading user configuration file")
            self.load(USERCONFIGFILE)

        # assign a runId
        # TODO: must that be done here?
        #       what happens with lri??
        runid = '.moa/last_run_id'
        if os.path.exists(runid):
            lri = open(runid).read().strip()
        else:
            lri = 1

        #finally, map environment variables on top of config
        if self.has_key('environ'):
            for k, v in self.environ.items():
                if not k in os.environ:
                    continue
                venv = _interpret_var(os.environ[k])
                cp = self
                for sv in v.split('.'):
                    cp = cp[sv]
                cp = venv
                l.debug("Environment override %s with %s" % (v, venv))
                exec('self.%s = %s' % (v, venv))
                #print eval('self.%s' % v)

        else: print self.keys()

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
        return pkg_resources.get_distribution("moa").version


if sysConf is None:
    sysConf = SysConf()
