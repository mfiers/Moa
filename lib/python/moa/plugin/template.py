# Copyright 2009, 2010 Mark Fiers, Plant & Food Research
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
# along with Moa. If not, see <http://www.gnu.org/licenses/>.
"""
Manipulate templates
--------------------

View and edit template definitions
"""
import time
import optparse

import moa.ui
import moa.utils
import moa.logger as l
import moa.template

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['template_dump'] = {
        'desc' : 'Display the raw template description',
        'call' : dumpTemplate,
        }
    
    data['commands']['template'] = {
        'desc' : 'Display the template name',
        'private' : True,
        'call' : template,
        }
    
    data['commands']['list'] = {
        'desc' : 'Print a list of all known templates',
        'call' : listTemplates,
        }

    data['commands']['template_set'] = {
        'desc' : 'Set a template parameters',
        'call' : templateSet,
        }
    
def defineOptions(data):
    parser = data['parser']
    
    parserN = optparse.OptionGroup(data['parser'], "moa list")
    parserN.add_option("-l", "--long", dest="listlong", action='store_true',
                       help="Show a description for moa list")
    data['parser'].add_option_group(parserN)


def _getTemplateFromData(data):
    """
    Return a relevant template, either the one specified, or the template
    that the current directory refers to

    :param data: global data structure, containing all relevant information
    :type data: dict
    
    """
    job = data['job']
    args = data['newargs']
    if len(args) > 0 and not '=' in args[0]:
        template = moa.template.Template(args[0])
    else:
        template = job.template

    if template.name == 'nojob':
        moa.ui.exitError("No template found")

    return template

def templateSet(data):
    """
    **moa template_set** - set a template parameter.

    This only works for top level template parameters
    """
    template = _getTemplateFromData(data)
    args = data['args']
    for i, a in enumerate(data['args']):
        print i,a
        if i == 0 and not '=' in a: continue
        elif not '=' in a:
            moa.ui.exitError("Do not know how to set '%s'" % a)
        k, v = a.split('=', 1)
        template[k] = v
        template.modification_data = time.asctime()
        template.save()
    
def listTemplates(data):
    """
    **moa list** - Print a list of all known templates

    Usage::

        moa list
        moa list -l

    Print a list of all templates known to this moa installation. If
    the option '-l' is used, a short description for each tempalte is
    printed as well.
    """
    options = data['options']
    if options.listlong:
        for job, info in moa.template.listAllLong():
            for line in textwrap.wrap(
                '%%(bold)s%s%%(reset)s:%%(blue)s %s%%(reset)s' % (job, info),
                initial_indent=' - ',
                subsequent_indent = '     '):
                moa.ui.fprint(line)
    else:
        for tFile, tName  in moa.template.listAll():
            print tName

def template(data):
    """
    **moa template** - Print the template name of the current job

    Usage::

        moa template

        
    """
    job = data['job']
    moa.ui.fprint(job.template.name)


def dumpTemplate(data):
    """
    **moa template_dump** - Show raw template information

    Usage::

       moa template_dump [TEMPLATE_NAME]

    Show the raw template data.
    """
    import yaml
    template = _getTemplateFromData(data)
    print yaml.dump(template.get_data())

