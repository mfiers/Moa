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
import sys

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
            sys.exit(-1)

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
        meta.git_branch = self.data.git_branch
        return meta

    def _findRelativeDir(self, wd):

        #find the relative dirname
        repodir = sysConf.git.repo.working_dir
        thisdir = os.path.join(os.path.abspath(wd), '.moa', 'template.d')
        if repodir in thisdir:
            thisdir = thisdir.replace(repodir, '')
            if thisdir[0] == '/':
                thisdir = thisdir[1:]
            else:
                moa.ui.exitError("unexpected local path %s" % thisdir)
        else:
            moa.ui.exitError("unexpected path %s, not in repo %s" % (
                thisdir, repodir))

        return repodir, thisdir, os.getcwd()

    def installTemplate(self, wd, tName):
        """
        Install a template in the directory `wd`
        """

        repo = sysConf.git.repo
        branch = 'master'  # not configurable for the time being

        #safety check
        sysConf.git.callGit(("git commit -m 'prepare git subtree' -a"))
        sysConf.git.callGit(("git diff-index HEAD"))

        if not repo:
            moa.ui.exitError("To use git submodules as templates you " +
                             "need to have the moaGit plugin active " +
                             "and be inside a Git repository")

        git_url = self.gbase % tName

        self.data.git_url = git_url
        self.data.git_branch = branch

        repodir, thisdir, jobdir = self._findRelativeDir(wd)

        #move to the repo base dir for subsequent operations
        moa.ui.message("repository base %s" % repodir)
        os.chdir(repodir)

        message = "Create Moa %s:%s job" % (self.name, tName)

        moa.ui.message("Remote repo at: %s" % git_url)
        moa.ui.message("Remote branch: %s" % branch)
        moa.ui.message("Adding subtree")
        sysConf.git.callGit(("git subtree add --prefix='%s' " +
                             "-m '%s' %s %s") % (
                                 thisdir, message, git_url, branch))

        #and back to the cwd
        os.chdir(jobdir)
        moa.ui.message("Finished creating new job")

    def refresh(self, wd, meta):
        """default operation would be to reinstall, but for git we can
        call git subtree pull

        Note: No branch support (yet)
        """

        repodir, thisdir, jobdir = self._findRelativeDir(wd)
        #move to the repo base dir for subsequent operations
        os.chdir(repodir)

        moa.ui.message('Refreshing job - git subtree pull')
        sysConf.git.callGit(("git subtree pull --prefix='%s' " +
                             " %s %s"
                             ) % (thisdir, meta.git_url, meta.git_branch))
        #and back to the cwd
        os.chdir(jobdir)
