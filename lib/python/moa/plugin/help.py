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
Help
----

Generate help
"""

import os
import sys
import time
import shutil
import pydoc
import pprint
import optparse
from subprocess import Popen, PIPE

import jinja2

import moa.job
import moa.utils
import moa.template
import moa.logger as l
import moa.plugin

MOABASE = moa.utils.getMoaBase()

JENV = None
    
def defineCommands(data):
    data['commands']['help'] = {
        'desc' : 'Display help for a template',
        'call' : templateHelp
        }
    data['commands']['welcome'] = {
        'desc' : 'Display a welcome text',
        'call' : welcome
        }

def templateHelp(data):
    """
    """

    job = data['job']
    args = data['newargs']
    if len(args) > 0:
        template = moa.template.Template(args[0])
    else:
        template = job.template

    if template.name == 'nojob':
        return welcome(data)
        #moa.ui.exitError("Either run moa template in a moa job directory, " +
        #                 "or specify a template name")

    #prep the template object for perusion by jinja
    template._categories = {}
    for pn in template.parameters:
        p = template.parameters[pn]
        if not template._categories.has_key(p.category):
            template._categories[p.category] = []
        template._categories[p.category].append(pn)
        
    global JENV
    JENV = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(MOABASE, 'lib', 'jinja2')))

    moaId = template.moa_id
    jinjaTemplate = JENV.get_template('template.help.jinja2')
    pager(jinjaTemplate, template)

def pager(template, templateData):
    """
    render the template & send it to the pager
    """
    mancode = template.render(templateData)
        
    p2 = Popen("nroff -c -mandoc".split(),
               stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p2.stdin.write(mancode)
    doc, err = p2.communicate()
    pydoc.pager(doc)

    
def welcome(data):
    """
    print a welcome message
    """
    moa.ui.fprint("""%%(bold)s%%(blue)sWelcome to MOA!%%(reset)s
Managing command line workflows

%%(bold)sAvailable commands%%(reset)s: %s

You can try: `%%(bold)smoa --help%%(reset)s` for a list of commands,
or read the manual at: %%(green)shttp://mfiers.github.com/Moa/%%(reset)s
"""  % (", ".join(data['commands'].keys())))
