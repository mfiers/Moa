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
from moa.sysConf import sysConf

MOABASE = moa.utils.getMoaBase()

JENV = None
    
def hook_defineCommands():
    sysConf['commands']['help'] = {
        'desc' : 'Display help for a template',
        'call' : templateHelp,
        'needsJob' : True,
        'unittest' : TESTHELP
        }
    
    sysConf['commands']['welcome'] = {
        'desc' : 'Display a welcome text',
        'call' : welcome,
        'private' : True,
        'unittest' : TESTWELCOME
        }

def templateHelp(job):
    """
    """

    args = sysConf['newargs']

    tmpjob = None
    if len(args) > 0:
        #create a tmp job
        tmpjob = moa.job.newTestJob(args[0])
        template = tmpjob.template
    else:
        template = job.template

    if template.name == 'nojob':
        return welcome(job)

    #prep the template object for rendering by jinja
    template._categories = {}
    for pn in template.parameters:
        p = template.parameters[pn]
        if p.category:
            cat = str(p.category).strip()
        else:
            cat = ""
        if not template._categories.has_key(cat):
            template._categories[cat] = []
        template._categories[cat].append(pn)

    #if not template.has_key('parameter_category_order'):
    template.parameter_category_order = template._categories.keys()
    template.parameter_category_order.sort()

    print template._categories

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

    
def welcome(job):
    """
    print a welcome message
    """
    clist = sysConf.commands.keys()
    clist.sort()
    commands =  "\n".join(textwrap.wrap(
        ", ".join(clist),
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
        'version' : sysConf.getVersion()
}, f='jinja')


TESTHELP = '''
moa simple -t test -- echo
x=`moa help`
[[ -n "$x" ]]
echo $x | grep -q  "moa simple"
echo $x | grep -q  "SEE ALSO"
echo $x | grep -q  "PARAMETERS"
echo $x | grep -q  "process*"
echo $x | grep -q  "process*"
'''

TESTWELCOME = """
moa welcome | grep -q 'Welcome to MOA'
"""
