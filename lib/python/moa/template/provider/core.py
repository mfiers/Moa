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

import pkg_resources

import Yaco

import moa.logger as l
import moa.resources

from moa.sysConf import sysConf
from moa.template import provider


class Core(provider.ProviderBase):
    
    TEMPLATEBASE = 'template2'

    def hasTemplate(self, tName):
        fname = os.path.join(self.TEMPLATEBASE, '%s.moa' % tName)
        return moa.resources.resourceExists(fname)

    def getTemplate(self, name):
        """
        Returns a Yaco instance of the moa template
        """
        fname = os.path.join(self.TEMPLATEBASE, '%s.moa' % name)
        return Yaco.Yaco(moa.resources.getResource(fname))

    def templateList(self):
        """
        List all Moa package provided templates.

        @returns: a list of all templates included in the Moa package
        @rtype: a list of strings
        """
        r = []
        for f in moa.resources.listResource(self.TEMPLATEBASE):
            if f[-4:] != '.moa':
                continue
            if f[0] == '.': 
                continue
            name = f.replace(".moa", "")
            r.append(f[:-4])
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

        for f in moa.resources.listResource(self.TEMPLATEBASE):
            if not f.find(tName) == 0: continue
            if f[-1] in ['~', '#']: continue
            if f[-4:] == '.moa': continue
            with open(os.path.join(wd, '.moa', 'template.d', f), 'w') as F:
                F.write(moa.resources.getResource(os.path.join(self.TEMPLATEBASE, f)))

