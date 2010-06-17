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
import optparse
import moa.job
import moa.logger
import moa.plugin
l = moa.logger.l 

#class Newjob(moa.plugin.BasePlugin):
#    pass

def defineCommands(data):
    data['commands']['new'] = {
        'desc' : 'Create a new Moa job in the current directory (unless -d ' + \
            'is defined)',
        'call' : newJob
        }

def defineOptions(data):
    parserN = optparse.OptionGroup(data['parser'], "Moa new")
    data['parser'].set_defaults(title="", directory=".")

    parserN.add_option("-t", "--title", dest="title", help="Job title")
    parserN.add_option("-d", "--directory", 
                       dest="directory",
                       help="Directory to create the new template in (default: .)")
    data['parser'].add_option_group(parserN)

def _parseArgs(args):
    '''
    Parse the arguments
    '''
    if len(args) == 0:
        template = 'traverse'
        params = []
    elif '=' in args[0]:
        template = 'traverse'
        params = args
    else:
        template = args[0]
        params = args[1:]
    return template, params
    
def newJob(data):
    """
    Create a new job 
    """
    cwd = data['cwd']
    options = data['options']
    args = data['newargs']
    template, params = _parseArgs(args)
    l.debug("Creating a new '%s' job" % template)

    if options.directory:
        wd = options.directory

    title = options.title


    moa.job.newJob( template = template,
                    title = title,
                    wd = wd,
                    parameters = params,
                    force = options.force,
            )
