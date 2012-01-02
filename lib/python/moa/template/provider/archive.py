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

Provides templates from a local archive directory

"""
import os
import sys
import shutil
import tarfile

import Yaco

import moa.utils
import moa.logger as l

from moa.sysConf import sysConf
from moa.template import provider


class Archive(provider.ProviderBase):

    def __init__(self, name, data):
        super(Archive, self).__init__(name, data)
        self.directory = os.path.abspath(
            os.path.expanduser(
                data.get('directory',
                         '~/.config/moa/archive'
                         ).strip()))

        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
            except OSError:
                #probably not allowed to do so..
                pass

    def saveMeta(self, meta, filename):
        """
        No meta - not refreshable
        """
        pass

    def hasTemplate(self, tName):
        fname = os.path.join(self.directory, '%s.tar.gz' % tName)
        return os.path.isfile(fname)

    def getTemplate(self, name):
        """
        Returns a Yaco instance of the moa template
        """
        return Yaco.Yaco()

    def templateList(self):
        """
        List all Moa package provided templates.

        @returns: a list of all templates included in the Moa package
        @rtype: a list of strings
        """
        r = []
        for f in os.listdir(self.directory):
            if f[-7:] != '.tar.gz':
                continue
            if f[0] == '.': 
                continue
            name = f.replace(".moa", "")
            r.append(f[:-7])
        return r

    def installTemplate(self, wd, tName):
        """
        Install a template in the directory `wd`
        """

        tarFile = os.path.join(self.directory, '%s.tar.gz' % tName)
        moa.ui.message("Unpacking %s" % tarFile)
        tf = tarfile.open(tarFile)
        tf.extractall()
        tf.close()
