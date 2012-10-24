# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
moa.provider
-------------

Provides templates..


"""
import datetime
import os

import Yaco
import moa.exceptions
import moa.logger
import moa.ui
from moa.sysConf import sysConf

l = moa.logger.getLogger(__name__)
#l.setLevel(moa.logger.DEBUG)


class Providers(object):
    """
    A class representing all providers - dispatches requests to the
    correct provider class
    """

    def __init__(self):
        self.providers = {}
        self.order = []

        _order = []
        for pName in sysConf.template.providers.keys():
            pInfo = sysConf.template.providers[pName]

            is_enabled = pInfo.get('enabled', False)
            if not is_enabled is True:
                continue

            priority = pInfo.get('priority', 1)
            assert(isinstance(priority, int))

            #import the correct module
            mod = 'moa.template.provider.%s' % pInfo['class']
            try:
                pMod = __import__(mod, globals(), locals(), [mod], -1)
            except ImportError:
                moa.ui.warn("cannot import template provider %s" % pName)
                continue

            #instantiate the class (mod.Mod())
            self.providers[pName] = \
                getattr(pMod, pInfo['class'].capitalize())(pName, pInfo)
            _order.append((priority, pName))

        _order.sort()
        self.order = [x[1] for x in _order]

    def findProvider(self, tName, pName):
        """
        Get the proper provider given the system configuration, template
        name and the fromProvider request

        Tom made me write this: TOM

        :returns: instantiated provider class
        """
        if pName:
            return self.providers[pName]

        for pName in self.order:
            provider = self.providers[pName]
            if provider.hasTemplate(tName):
                return provider

        #nothing found
        return None

    def getTemplate(self, tName, pName=None):
        """
        Return the (Yaco) template object

        :param tName: Template name
        :param pName: The provider to get the template from - if not provider
          find the first provider that recognizes a template with this name
        :returns: Yaco template object
        """
        provider = self.findProvider(tName, pName)

        if not provider:
            moa.ui.exitError("Cannot find provider for template %s.%s" % (
                provider, tName))
        return provider.getTemplate(tName)

    def templateList(self):
        rv = set()
        for pName in self.order:
            #print self.providers[pName].templateList()
            rv.update(set((pName, x)
                          for x
                          in self.providers[pName].templateList()))
        rv = list(rv)
        rv.sort()
        return rv

    def refreshTemplate(self, wd, meta):
        """Refresh the current template- based on the meta data
        provided

        """

        l.debug("refreshing template in %s" % self.__class__.__name__)
        # instead of finding the old provider - instantiate a new
        # copy of the class stated in `meta`

        #import the correct module
        mod = 'moa.template.provider.%s' % meta['class']
        try:
            pMod = __import__(mod, globals(), locals(), [mod], -1)
        except ImportError:
            moa.ui.exitError("cannot import provider %s" % meta['class'])

        cob = getattr(pMod, meta['class'].capitalize())(meta['provider'], meta)
        cob.refresh(wd, meta)

    def installTemplate(self, wd, tName, pName=None):

        provider = self.findProvider(tName, pName)

        if not provider:
            raise moa.exceptions.InvalidTemplate()

        provider.installTemplate(wd, tName)

        confdir = os.path.join(wd, '.moa')

        meta = provider.getMeta()
        meta.name = tName
        meta.installed = datetime.datetime.now().isoformat()
        provider.saveMeta(meta, confdir)


#base class for all providers
class ProviderBase(object):
    def __init__(self, name, data={}):
        self.name = name
        self.data = data

    def getMeta(self):
        meta = Yaco.Yaco(self.data)
        meta.provider_type = self.__class__.__name__.lower()
        meta.provider = self.name
        return meta

    def saveMeta(self, meta, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        meta.save(os.path.join(dir, 'template.meta'))

    def refresh(self, wd, meta):
        """
        default operation is to reinstall
        """
        self.installTemplate(wd, meta.name)
