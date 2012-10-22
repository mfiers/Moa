# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
moa.provider.GitModule
-----------------------

Uses git repo's as templates by installing them as a submodule

"""
import os

import Yaco
import moa.logger
import moa.ui
from moa.sysConf import sysConf
from moa.template import provider


l = moa.logger.getLogger(__name__)
l.setLevel(moa.logger.DEBUG)

class Gitmodule(provider.ProviderBase):

    def __init__(self, name, data):
        super(Gitmodule, self).__init__(name, data)
        if not 'base' in self.data:
            l.critical("template provider %s is not properly installed" %
                       self.name)
            l.critical("need a git base location")
        self.gbase = self.data['base']

    def hasTemplate(self, tName):
        return False

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
        return []

    def getMeta(self):
        meta = super(Gitmodule, self).getMeta()
        meta.remote = self.data.remote
        meta.git_url = self.data.git_url
        return meta

    def installTemplate(self, wd, tName):
        """
        Install a template in the directory `wd`
        """

        repo = sysConf.git.repo
        if not repo:
            moa.ui.exitError("To use git submodules as templates you " +
                             "need to have the moaGit plugin active " +
                             "and be inside a Git repository")

        git_url = self.gbase + tName

        #first find a good name for the remote
        remote_id = 0
        remote_names = [r.name for r in repo.remotes]
        while True:
            remote_name = '%s_%s__%02d' % (self.name, tName, remote_id)
            if not remote_name in remote_names:
                break
            remote_id += 1

        #create a new remote
        self.data.remote = remote_name
        self.data.git_url = git_url

        #find the relative dirname
        repodir = repo.working_dir
        thisdir = os.path.join(os.path.abspath(wd), '.moa', 'template.d')
        if repodir in thisdir:
            thisdir = thisdir.replace(repodir, '')
            if thisdir[0] == '/':
                thisdir = thisdir[1:]
            else:
                moa.ui.exitError("unexpected local path %s" % thisdir)

        #move to the repo base dir
        remember_wd = os.getcwd()
        os.chdir(repodir)

        moa.ui.message("creating a new git remote %s %s" % (
            remote_name, git_url))
        moa.ui.message("for the repo at: %s" % git_url)
        sysConf.git.callGit('git remote add -f %s %s' % (remote_name, git_url))

        moa.ui.message("merging")
        sysConf.git.callGit('git merge -s ours --no-commit %s/master' %
                            (remote_name))
        moa.ui.message("git read-tree")
        sysConf.git.callGit('git read-tree --prefix=%s -u %s/master' %
                            (thisdir, remote_name))

        sysConf.git.callGit(('git commit -a  -m "merged %s:%s ' +
                             'as a template in %s"')
                            % (self.name, tName, thisdir))

        #and back to the cwd
        os.chdir(remember_wd)
        moa.ui.message("Finished adding group")

    def refresh(self, wd, meta):
        """
        default operation is to reinstall
        """
        l.debug('refreshing! - call git pull')
        cl = 'git pull -s subtree %s master' % meta.remote
        sysConf.git.callGit(cl)
