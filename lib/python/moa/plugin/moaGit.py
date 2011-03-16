# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
**moaGit** - maintain a git repository with job information
-----------------------------------------------------------

"""
import os
import sys
import git 
import time
import optparse

import moa.logger as l
import moa.plugin.newjob

GITROOT = None
GITREPO = None

def defineCommands(data):
    data['commands']['history'] = {
        'desc' : 'display a version control log',
        'call': gitlog
        }
    data['commands']['tag'] = {
        'desc' : 'Tag the current version',
        'call': tag
        }

    
def defineOptions(data):
    parserG = optparse.OptionGroup(
        data['parser'], 'Version control (Git)')
    
    parserG.add_option('--git-force-init', action='store_true',
                       dest='gitForceInit',
                      help = 'Force initialization of a new git repository, this ' +
                      'deletes the old repository')
    parserG.add_option('--m', action='store',
                       dest='gitMessage', 
                      help = 'Commit message for git')
    
    data['parser'].add_option_group(parserG)

def tag(data):
    global GITREPO
    if not GITREPO:
        l.info("no repository is initialized")
        return

    tagname = data['args'][1]
    message = data['options'].gitMessage
    l.info('tagging with "%s"' % tagname)
    GITREPO.create_tag(tagname, message=message)

def prepare(data):
    #check if we're inside a git repository
    if not data.has_key('projectRoot'):
        return

    projectRoot = data['projectRoot']
    l.debug("seeing if %s is a git repos" % projectRoot)
    repo = git.Repo(projectRoot)
    
    global GITROOT
    global GITREPO
    GITROOT = projectRoot
    GITREPO = repo
    
    l.debug("found a git root at %s " % GITROOT)

def postSet(data):
    """
    Execute just after setting a parameter
    """
    global GITROOT
    global GITREPO
    #try to commit this project
    if not GITROOT:
        #no git repository - not registering any files
        return

    l.debug("committing postset")
    index = GITREPO.index
    index.commit('Set %s ' % " ".join(data['newargs']))
    
    
def postNew(data):
    """
    To be executed just after the 'moa new' command
    """    
    wd = data['cwd']
    global GITROOT
    global GITREPO

    l.debug("running git post new hook")
    l.debug('GITROOT %s' % GITROOT)

    template = 'traverse'
    for a in data['newargs']:
        if '=' in a: continue
        template = a
        
    if template == 'project':
        # creating new project - see if we need to create a
        # new repository
        return _gitInit(data)

    #try to commit this project
    if not GITROOT:
        #no git repository - not registering any files
        return
    
    info = moa.info.info(wd)
    index = GITREPO.index
    index.add(info['moa_files'].split())
    index.commit('Inital commit of job "%s"' % info['title'])

def gitlog(data):
    """
    Print a log to screen
    """
    global GITREPO
    global GITROOT

    if not GITREPO:
        l.info("noting to report - no repo")
        return

    tags = {}
    
    for t in GITREPO.tags:
        print t.commit
        tags[t.commit] = t

    for c in GITREPO.iter_commits():
        #if str(c) in tags.keys()
        t = time.strftime("%d %b %Y %H:%M", time.localtime(c.authored_date))

        if c in tags.keys():
            print " tag| %s" % tags[c]
        
        print "%3s | %s | %s" % (c.count(), t, c.message)
    
def _gitInit(data):
    """
    Initialize a git repository
    """    
    global GITREPO
    global GITROOT
    if GITROOT:
        l.critical("trying to initialize a git repository wihtin a git repository")
        sys.exit(-1)

    wd = data['cwd']
    
    GITROOT = wd
    GITREPO =  git.Repo.init(GITROOT)
    l.info("created a git repository at %s" % GITROOT)
    
    info = moa.info.info(wd)
    index = GITREPO.index
    index.add(info['moa_files'].split())
    index.commit('Settin up project "%s"' % info['title'])

    #write some data to .gitignore
    with open(os.path.join(wd, '.gitignore'), 'w') as F:
        F.write(".*\n")
        F.write("moa.success\n")
        F.write("moa.out\n")
        F.write("moa.err\n")
        F.write("moa.failed\n")
        F.write("moa.runlock\n")
        
