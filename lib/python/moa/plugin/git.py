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

def defineCommands(commands):
    commands['gitlog'] = 'display a version control log'

def defineOptions(parser):
    parserG = optparse.OptionGroup(parser, 'Version control (Git)')
    
    parserG.add_option('--git-force-init', action='store_true',
                       dest='gitForceInit',
                      help = 'Force initialization of a new git repository, this ' +
                      'deletes the old repository')
    parserG.add_option('-m', action='store',
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
