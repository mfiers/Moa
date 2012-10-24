# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
moa.provider.core
-----------------

Provides templates from the Moa package.

"""
import os
import shutil

import Yaco
import pkg_resources

import moa.logger
from moa.template import provider


l = moa.logger.getLogger(__name__)


class Core(provider.ProviderBase):

    TEMPLATEBASE = 'template2'
    RESLOC = 'data/templates'

    def hasTemplate(self, tName):
        return pkg_resources.resource_exists(
            'moa', '%s/%s.moa' % (self.RESLOC, tName))

    def getTemplate(self, name):
        """
        Returns a Yaco instance of the moa template
        """
        return Yaco.Yaco(pkg_resources.resource_string(
            'moa', "%s/%s.moa" % (self.RESLOC, name)))

    def templateList(self):
        """
        List all Moa package provided templates.

        @returns: a list of all templates included in the Moa package
        @rtype: a list of strings
        """
        r = []
        for f in pkg_resources.resource_listdir('moa', self.RESLOC):
            if f[-4:] != '.moa':
                continue
            if f[0] == '.':
                continue
            name = f.replace(".moa", "")
            r.append(name)
        return r

    def installTemplate(self, wd, tName):
        """
        Install a template in the directory `wd`
        """
        moaFile = self.getTemplate(tName)
        extraFileDir = os.path.join(wd, '.moa', 'template.d')

        if os.path.isdir(extraFileDir):
            shutil.rmtree(extraFileDir)
        os.makedirs(extraFileDir)

        #print type(moaFile)
        moaFile.save(os.path.join(wd, '.moa', 'template'))

        for f in pkg_resources.resource_listdir('moa', self.RESLOC):
            if not f.find("%s." % tName) == 0:
                continue
            if f[-1] in ['~', '#']:
                continue

            if f[-4:] == '.moa': continue
            with open(os.path.join(wd, '.moa', 'template.d', f), 'w') as F:
                F.write(
                    pkg_resources.resource_string(
                        'moa', "%s/%s" % (self.RESLOC, f)))
