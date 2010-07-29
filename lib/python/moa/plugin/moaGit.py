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
Git
"""
import os
import optparse
import git 

import moa.info
import moa.logger as l
import moa.plugin.newjob

GITROOT = None
GITREPO = None

def defineCommands(data):
    data['commands']['gitlog'] = {
        'desc' : 'display a version control log'
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

def prepare(data):
    #check if we're inside a git repository
    if not data.has_key('projectRoot'):
        return

    wd = data['cwd']

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
    wd = data['cwd']
    global GITROOT
    global GITREPO
    #try to commit this project
    if not GITROOT:
        #no git repository - not registering any files
        return

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
    job = data['newargs'][0]

    if job == 'project':
        #creating  new job - see if we are to create a new repository
        return _gitInit(data)

    #try to commit this project
    if not GITROOT:
        #no git repository - not registering any files
        return
    
    info = moa.info.info(wd)
    index = GITREPO.index
    index.add(info['moa_files'].split())
    index.commit('Inital commit of job "%s"' % info['title'])
    
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
    l.critical("created a git repository at %s" % GITROOT)
    
    info = moa.info.info(wd)
    index = GITREPO.index
    index.add(info['moa_files'].split())
    index.commit('Inital commit of project "%s"' % info['title'])

    #write some data to .gitignore
    with open(os.path.join(wd, '.gitignore'), 'w') as F:
        F.write(".gitignore\n")
        F.write("moa.success\n")
        F.write("moa.out\n")
        F.write("moa.err\n")
        F.write("moa.failed\n")
        F.write("moa.runlock\n")
        
