# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**help** - generate help
------------------------

"""

import os
import sys
import pydoc
import textwrap
import subprocess as sp

import jinja2

import moa.job
import moa.utils
import moa.template
import moa.plugin

MOABASE = moa.utils.getMoaBase()

JENV = None
    
def defineCommands(data):
    data['commands']['help'] = {
        'desc' : 'Display help for a template',
        'call' : templateHelp,
        'needsJob' : True
        }
    
    data['commands']['welcome'] = {
        'desc' : 'Display a welcome text',
        'call' : welcome,
        'private' : True
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

    for t in job.template.commands:
        print t
    sys.exit()
    
    if template.name == 'nojob':
        return welcome(data)

    #prep the template object for rendering by jinja
    template._categories = {}
    for pn in template.parameters:
        p = template.parameters[pn]
        cat = str(p.category).strip()
        if not template._categories.has_key(cat):
            template._categories[cat] = []
        template._categories[cat].append(pn)
    global JENV
    JENV = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(MOABASE, 'lib', 'jinja2')))

    jinjaTemplate = JENV.get_template('template.help.jinja2')
    pager(jinjaTemplate, template)

def pager(template, templateData):
    """
    render the template & send it to the pager
    """
    mancode = template.render(templateData)
    p2 = sp.Popen("nroff -c -mandoc".split(),
               stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    p2.stdin.write(mancode)
    doc, err = p2.communicate()
    pydoc.pager(doc)

    
def welcome(data):
    """
    print a welcome message
    """
    commands =  "\n".join(textwrap.wrap(
        ", ".join(data['commands'].keys()),
        subsequent_indent='   ',
        initial_indent='                   ',
        )).lstrip()
    
    moa.ui.fprint("""{{bold}}{{blue}}Welcome to MOA!{{reset}} (v %(version)s)

{{bold}}Available commands{{reset}}: %(commands)s

Try:
* `{{bold}}moa --help{{reset}}` for information on running the `{{green}}moa{{reset}}` command.
* `{{bold}}moa help{{reset}}` inside a moa job directory for information on the operation
  of that template
* reading the manual at: {{green}}http://mfiers.github.com/Moa/{{reset}}
"""  % {'commands' : commands,
        'version' : data['sysConf'].getVersion()
}, f='jinja')
