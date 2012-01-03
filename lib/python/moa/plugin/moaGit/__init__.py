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
import os
import sys
import git
import glob
import time
import optparse

from moa.sysConf import sysConf
import moa.logger as l
import moa.plugin.newjob

def hook_defineCommands():
    sysConf['commands']['gitlog'] = {
        'desc' : 'display a nicely formatted git log',
        'call': gitlog
        }
    sysConf['commands']['gittag'] = {
        'desc' : 'Tag the current version',
        'call': tag
        }
    sysConf['commands']['gitadd'] = {
        'desc' : 'Add the current job to the git repository',
        'call': gitadd
        }


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
    
def _checkGitIgnore(gitignoreFile):
    """
    See if there is moa dir specific git ignore file - if not create one
    """
    if not os.path.exists(gitignoreFile):
        with open(gitignoreFile, 'w') as F:
            F.write("log\n")
            F.write("log.d/\n")
            F.write("log.latest\n")
            F.write("last_run_id\n")
            F.write("status\n")
            F.write("*.fof\n")
            F.write("*~\n")
            
def _commitDir(wd, message):
    """
    Simpler utility to add files to a repository without
    initiating a moa job object
    """
    repo = sysConf.git.repo
    if not repo: return

    
    moadir = os.path.join(wd, '.moa')
    if not os.path.exists(moadir):
        return
    
    gitignoreFile = os.path.join(wd, '.moa', '.gitignore')
    _checkGitIgnore(gitignoreFile)

    files = set([gitignoreFile])
    for gl in ['.moa/template',
               '.moa/template.d/*',
               '.moa/config',
               'moa.*',
               'Readme', 'README', 'Readme.*',
               'Changelog', 'CHANGELOG', 'Changelog.*' ]:
        
        for f in glob.glob(os.path.join(wd, gl)):
            files.update(set(glob.glob(os.path.join(wd, gl))))
            
        remove = [x for x in files if x[-1] == '~']
        files.difference_update(remove)

    _realCommit(repo, list(files), wd, message)
    #repo.git.commit(os.path.join(wd, '.moa', 'template.d'))
    
def _commit(job, message):
    """
    Commit the current job to the repository
    """
    repo = sysConf.git.repo
    if not repo: return
    
    gitignoreFile = os.path.join(job.wd, '.moa', '.gitignore')
    _checkGitIgnore(gitignoreFile)

    files = [gitignoreFile]
    files.extend(job.getFiles())
    _realCommit(repo, files, job.wd, message)
    #repo.git.commit(os.path.join(job.wd,  '.moa', 'template.d'))
                    
def gitadd(job):
    """
    Add a job to the git repository
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
    sysConf.git.commitJob = _commit
    sysConf.git.commitDir = _commitDir
    sysConf.git.getRepo = _getRepo
    sysConf.git.repo = _getRepo(sysConf.job)
    if not sysConf.git.repo and sysConf.plugin_settings.moaGit.warn:
            moa.ui.warn("Cannot find a git repository!")

def hook_finish():
    """
    Handle all git changes post execution - actually defer to plugin specific calls
    """
    sysConf.pluginHandler.run('git_finish_%s' % sysConf.originalCommand)
        
def gitlog(job):
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
