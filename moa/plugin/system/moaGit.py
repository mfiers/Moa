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
import tempfile

#import git
from sh import git, ErrorReturnCode
import moa.args
import moa.logger
from moa.sysConf import sysConf
import moa.api

l = moa.logger.getLogger(__name__)
l.setLevel(moa.logger.DEBUG)

def _exit_need_git_repo():
    moa.ui.exitError("Enforcing git use - please initialze a git rep")

@moa.api.api
def git_check_repo():
    """
    Check if this directory is inside a git repo

    return False if not, returns the git root if true
    """

    try:
        gitdir = git('rev-parse', git_dir=True).strip()
    except ErrorReturnCode:
        #no git repo here.
        if sysConf.plugins.system.moaGit.enforce:
            _exit_need_git_repo()
        return False

    if gitdir == '.git':
        gitdir = sysConf.job.wd
    else:
        assert(gitdir[-4:] == '.git')
        gitdir = gitdir[:-4]
    return gitdir


def _realCommit(repo, files, wd, message):
    """
    Do the actual commit
    """
    message += "\n\n"
    message += "Committed by the moa/moaGit plugin\n"
    message += "work directory: %s\n" % wd
    message += "command line:\n"
    message += "   %s\n" % " ".join(sys.argv)

    filename = None
    with tempfile.NamedTemporaryFile(delete=False) as F:
        filename = F.name
        F.write(message)

    for f in map(os.path.abspath, files):
        git.add(f, f=True)

    git.commit(F=filename)


def _checkGitIgnore(repo):
    """Approach is simple - we're ignoring everything unless
    specifically added. Both for the moa job in&output files as the
    .moa files. (unless specified differntly in the config
    """

    print repo
    gitignoreFile = os.path.join(repo, '.gitignore')
    if not os.path.exists(gitignoreFile):
        if 'ignore' in sysConf.plugins.system.moaGit:
            to_ignore = sysConf.plugins.system.moaGit.ignore
        else:
            to_ignore = ['*']

        with open(gitignoreFile, 'w') as F:
            for ignore in to_ignore:
                F.write("%s\n" % ignore)

        git.add(gitignoreFile, f=True)
        git.commit(gitignoreFile, m='automatic update of the .gitignore file')

    else:
        l.debug(".gitignore exists - ignoring")

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

    _checkGitIgnore(repo)

    files = set()
    for gl in sysConf.plugins.system.moaGit.commit:
        for f in glob.glob(os.path.join(wd, gl)):
            files.update(set(glob.glob(os.path.join(wd, gl))))

        remove = [x for x in files if x[-1] == '~']
        files.difference_update(remove)

    _realCommit(list(files), wd, message)

@moa.api.api
def git_commit_job(job, message):
    """
    Commit the current job to the repository
    """
    repo = sysConf.api.git_check_repo()
    if not repo: return

    _checkGitIgnore(repo)

    files = []
    files.extend(job.getFiles())
    _realCommit(repo, files, job.wd, message)

@moa.args.needsJob
@moa.args.command
def gitadd(job, args):
    """
    add this job to a git repository
    """
    git_commit_job(job, "add/refresh of %s" % job.wd)


def tag(job):
    repo = sysConf.api.git_check_repo()
    if not repo: return

    tagname = sysConf.args[1]
    message = sysConf.options.message
    l.info('tagging with "%s"' % tagname)
    repo.create_tag(tagname, message=message)


def hook_prepare_3():
    """
    Register a function for submitting a job
    """
    repo = sysConf.api.git_check_repo()


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
