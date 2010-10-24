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
import moa.logger as l
import moa.plugin

def defineCommands(data):
    data['commands']['new'] = {
        'desc' : "Create a new Moa job in the current directory " +
                 "(unless -d is defined)",
        'call' : newJob
        }

def defineOptions(data):
    parser = data['parser']
    parserN = optparse.OptionGroup(data['parser'], "Moa new")
    data['parser'].set_defaults(title="", directory=".")

    parserN.add_option("-t", "--title", dest="title", help="Job title")

    try:
        parser.add_option("-d", dest="directory",
                      help="Create/unpack the job/pipeline in this directory")
        
    except optparse.OptionConflictError:
        pass #could have been defined in plugin/pack.py

    data['parser'].add_option_group(parserN)

def newJob(data):
    """
    Create a new job 
    """
    wd = data['cwd']
    options = data['options']
    args = data['newargs']

    params = []
    template = 'traverse'
    
    for a in args:
        if '=' in a:
            params.append(a)
        else:
            template = a

    l.debug("Creating a new '%s' job" % template)

    if options.directory:
        wd = options.directory

    title = options.title
    job = moa.job.getJob(wd)
    job.new( template = template,
             title = title,
             parameters = params,
             force = options.force)

TESTSCRIPT = """
moa new adhoc
moa new -d subdir adhoc

"""
