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

import moa.logger
import moa.plugin.newjob
l = moa.logger.l
import moa.hooks


def defineCommands(commands):
    commands['gitlog'] = {
        'desc' : 'display a version control log'
        }

def defineOptions(parser):
    parserG = optparse.OptionGroup(parser, 'Version control (Git)')
    
    parserG.add_option('--git-force-init', action='store_true',
                       dest='gitForceInit',
                      help = 'Force initialization of a new git repository, this ' +
                      'deletes the old repository')
    parserG.add_option('--m', action='store',
                       dest='gitMessage',
                      help = 'Commit message for git')
    
    parser.add_option_group(parserG)


def prepare(g):
    if g['options'].gitForceInit:
        os.putenv("MOA_GITFORCEINIT", "yes")
    if g['options'].gitMessage:
        os.putenv("MOA_GITMESSAGE", g['options'].gitMessage)
    elif g['args'] == 'new' and g['options'].title:
        os.putenv("MOA_GITMESSAGE", "Creating: " + g['options'].title)
    elif g['args'] and g['args'][0] == 'set':
        os.putenv("MOA_GITMESSAGE", "moa set '%s'" %
                  " ".join(g['args'][1:]).replace('"',''))
        
    if not g['moaHooks'].has_key('postSet'):
        g['moaHooks']['postSet'] = []


    moa.hooks.add('after', 'set', gitPostSet)
    moa.hooks.add('after', 'new', gitPostNew)
    
def gitPostSet(g):
    """
    Function to run after running conf.set
    """
    l.critical("running git postset")

def gitPostNew(g):
    """
    Run after creating a new job - probably need to store stuff
    in the repos, or, if this is a project -we might even need
    to create a repository
    """
    
    #if template == 'project':
    #    startNewGitRepos(g)
    #l.debug("running git post new for template %s" % template)
    
def startNewGitRepos(g):
    """
    Start a new git repository
    """
    wd = g['wd']
    
