# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**moaGit** - maintain a git repository with job information
-----------------------------------------------------------

"""
import glob
import os
import subprocess as sp
import sys
import time

import git
import moa.args
import moa.logger
from moa.sysConf import sysConf

l = moa.logger.getLogger(__name__)
l.setLevel(moa.logger.DEBUG)


def _callGit(cl):
    moa.ui.message("executing %s" % cl)
    return sp.call(cl, shell=True)


def _getRepo(job):
    """
    Return the git repository object
    """

    wd = job.wd
    try:
        repo = git.Repo(wd)
        return repo
    except git.InvalidGitRepositoryError:
        return None


def _checkInRepo(job):
    """
    Check if we're inside a repository
    """
    rc = sp.call(['git status --porcelain -uno'].split())
    if rc == 0:
        l.debug("In a git repository (%s)" % job.wd)
        return True
    else:
        l.debug("NOT in a git repository (%s)" % job.wd)
        return False


def _realCommit(repo, files, wd, message):
    """
    Do the actual commit
    """
    message += "\n\n"
    message += "Committed by the moa/ moaGit plugin\n"
    message += "work directory: %s\n" % wd
    message += "command line:\n"
    message += "   %s\n" % " ".join(sys.argv)

    repo.index.add(map(os.path.abspath, files))

    if (len(repo.heads) == 0) or (repo.is_dirty()):
        moa.ui.message("Committing changes to git")
        repo.index.commit(message)
    else:
        l.debug("Skipping git add - repository is not dirty")

    #now try to remove all deleted files under wd
    repo.git.add(u="")
    try:
        repo.git.commit(m='"remove deleted files"')
    except git.exc.GitCommandError:
        pass


def _checkGitIgnore(wd):
    """Approach is simple - we're ignoring everything unless
    specifically added. Both for the moa job in&output files as the
    .moa files. (unless specified differntly in the config
    """

    gitignoreFile = os.path.join(wd, '.gitignore')
    if not os.path.exists(gitignoreFile):
        if 'ignore' in sysConf.plugins.system.moaGit:
            to_ignore = sysConf.plugins.system.moaGit.ignore
        else:
            to_ignore = ['*']
        with open(gitignoreFile, 'w') as F:
            for ignore in to_ignore:
                F.write("%s\n" % ignore)


def _commitDir(wd, message):
    """
    Simpler utility to add files to a repository without
    initiating a moa job object
    """
    repo = sysConf.git.repo
    if not repo:
        return

    moadir = os.path.join(wd, '.moa')

    if not os.path.exists(moadir):
        return

    #_checkGitIgnore(wd)

    files = set()
    for gl in sysConf.plugins.system.moaGit.commit:
        for f in glob.glob(os.path.join(wd, gl)):
            files.update(set(glob.glob(os.path.join(wd, gl))))

        remove = [x for x in files if x[-1] == '~']
        files.difference_update(remove)

    _realCommit(repo, list(files), wd, message)


def _commit(job, message):
    """
    Commit the current job to the repository
    """
    repo = sysConf.git.repo
    if not repo:
        return

    #_checkGitIgnore(job.wd)

    files = []
    files.extend(job.getFiles())
    _realCommit(repo, files, job.wd, message)

    #repo.git.commit(os.path.join(job.wd,  '.moa', 'template.d'))


@moa.args.needsJob
@moa.args.command
def gitadd(job, args):
    """
    add this job to a git repository
    """
    l.debug("adding to git %s" % job.wd)
    _commit(job, "add/refresh of %s" % job.wd)


def tag(job):
    repo = _getRepo(job)
    if not repo:
        moa.ui.exitError("Not inside a git repository")
        return

    tagname = sysConf.args[1]
    message = sysConf.options.message
    l.info('tagging with "%s"' % tagname)
    repo.create_tag(tagname, message=message)


def hook_prepare_3():
    """
    Register a function for submitting a job
    """
    sysConf.git.commit = _commit
    sysConf.git.active = True
    sysConf.git.callGit = _callGit
    sysConf.git.commitJob = _commit
    sysConf.git.commitDir = _commitDir
    sysConf.git.getRepo = _getRepo
    sysConf.git.repo = _getRepo(sysConf.job)
    if not sysConf.git.repo and sysConf.plugin_settings.moaGit.warn:
            moa.ui.warn("Cannot find a git repository!")

def hook_finish():
    """

    Handle all git changes post execution - actually defer to
    plugin specific calls

    """
    if sysConf.git.repo is None:
        return
    sysConf.pluginHandler.run('git_finish_%s' % sysConf.originalCommand)


def hook_postNew():
    """Handle all git changes post New - checking if this is a new
    'project'. If so, and there is no git repo yet - create one

    """
    if sysConf.git.repo:
        return

    # was a 'project' created? If not return
    if sysConf.job.template.name != 'project':
        return

    #create a .gitignore file
    _checkGitIgnore(sysConf.job.wd)

    moa.ui.warn("Creating a new git repository")
    sysConf.git.repo = git.Repo.init(sysConf.job.wd)
    _commit(sysConf.job, "New Moa Project")


@moa.args.needsJob
@moa.args.command
def gitlog(job, args):
    """
    Print a log to screen
    """
    repo = _getRepo(job)
    if not repo:
        l.info("noting to report - no git repository found")
        return

    tags = {}

    for t in repo.tags:
        tags[t.commit] = t

    for c in repo.iter_commits():
        t = time.strftime("%d %b %Y %H:%M", time.localtime(c.authored_date))

        if c in tags.keys():
            print " tag| %s" % tags[c]

        print "%3s | %s | %s" % (c.count(), t, c.message.split("\n")[0])
