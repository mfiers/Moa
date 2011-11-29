# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**template** - information on templates
-------------------------------------------

"""
import sys
import time
import optparse
import textwrap

import moa.ui
import moa.utils
import moa.template

from moa.sysConf import sysConf

def hook_defineCommands():
    """
    Set the moa commands for this plugin
    """
    sysConf['commands']['template_dump'] = {
        'desc' : 'Display the raw template description',
        'private': True,
        'call' : dumpTemplate,
        'unittest' : TEMPLATEDUMPTEST
        }
    
    sysConf['commands']['template'] = {
        'desc' : 'Display the template name',
        'private' : True,
        'call' : template,
        'unittest' : TEMPLATETEST,
        }
    
    sysConf['commands']['list'] = {
        'desc' : 'Print a list of all known templates',
        'call' : listTemplates,
        'needsJob' : False,
        'unittest' : LISTTEST,
        }

    sysConf['commands']['refresh'] = {
        'desc' : 'Reload the template',
        'call' : refresh,
        'needsJob' : True,
        'unittest' : REFRESHTEST
        }

    sysConf['commands']['template_set'] = {
        'desc' : 'Set a template parameters',
        'private': True,
        'call' : templateSet,
        }
    

def refresh(job):
    """
    Refresh the template - i.e. reload the template from the central
    repository.
    """
    job.refreshTemplate()

def _getTemplateFromData(job):
    """
    Return a relevant template, either the one specified, or the template
    that the current directory refers to

    :param data: global data structure, containing all relevant information
    :type data: dict
    
    """
    args = sysConf['newargs']
    if len(args) > 0 and not '=' in args[0]:
        template = moa.template.Template(args[0])
    else:
        template = job.template

    if template.name == 'nojob':
        moa.ui.exitError("No template found")

    return template

def templateSet(job):
    """
    **moa template_set** - set a template parameter.

    This only works for top level template parameters
    """
    template = _getTemplateFromData(job)
    for i, a in enumerate(sysConf.args):
        print i,a
        if i == 0 and not '=' in a: continue
        elif not '=' in a:
            moa.ui.exitError("Do not know how to set '%s'" % a)
        k, v = a.split('=', 1)
        template[k] = v
        template.modification_data = time.asctime()
        template.save()
    
def listTemplates(job):
    """
    **moa list** - Print a list of all known templates

    Usage::

        moa list
        moa list -l

    Print a list of all templates known to this moa installation. If
    the option '-l' is used, a short description for each tempalte is
    printed as well.
    """

    for name in moa.template.templateList():
        if sysConf.options.showAll:
            ti = moa.template.getMoaFile(name)
            txt = moa.ui.fformat(
                '{{bold}}%s{{reset}}:{{blue}} %s{{reset}}' % (name, ti.description),
                f='jinja')
            for line in textwrap.wrap(txt, initial_indent=' - ', width=80,
                                      subsequent_indent = '   '):
                print line
        else:
            print name

def template(job):
    """
    **moa template** - Print the template name of the current job

    Usage::

        moa template

        
    """
    moa.ui.fprint(job.template.name)


def dumpTemplate(job):
    """
    **moa template_dump** - Show raw template information

    Usage::

       moa template_dump [TEMPLATE_NAME]

    Show the raw template sysConf.
    """
    template = _getTemplateFromData(job)
    print template.pretty()

LISTTEST = '''
moa list | grep -q "map"
'''

TEMPLATETEST = '''
moa simple -t test -- echo
moa template | grep -q "simple"
'''

TEMPLATEDUMPTEST = '''
moa simple -t test -- echo
out=`moa template_dump`
[[ "$out" =~ "author" ]]
[[ "$out" =~ "backend" ]]
[[ "$out" =~ "'name': 'simple'" ]]
'''

REFRESHTEST = '''
moa simple -t test -- echo

'''
