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




import os

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
    wd = data['wd']
    options = data['options']
    args = data['newargs']

    params = []
    template = 'traverse'
    
    for a in args:
        if '=' in a:
            params.append(a)
        else:
            template = a

    l.info("Creating a new '%s' job" % template)

    if os.path.exists(os.path.join(
        wd, '.moa', 'template')) and \
        not options.force:
        l.error("Seems that there is already a Moa job in")
        l.error(wd)
        l.error("use -f to override")

    title = options.title
    
    job = moa.job.newJob(wd,
                         template = template,
                         options = options)

    l.debug("Successfully created a %s job" % template)

    if title:
        job.conf['title'] = title
        
    for p in params:
        k,v = p.split('=', 1)
        job.conf.set(k,v)
    job.conf.save()

TESTSCRIPT = """
moa new adhoc -t 'testJob' adhoc_mode=par dummy=nonsense
[[ -f ./Makefile ]] || exer 'No job was created'
grep -q title moa.mk || exer 'title has not been defined'
grep -q dummy moa.mk || exer 'title has not been defined'
"""
