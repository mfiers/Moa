
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
import moa.args
import moa.template

from moa.sysConf import sysConf


@moa.args.needsJob
@moa.args.command
def refresh(job, args):
    """
    Refresh the template

    Reload the template from the original repository.
    """
    job.refreshTemplate()


def hook_git_finish_refresh():
    sysConf.git.commitJob(sysConf.job, 'moa refresh (%s)' % sysConf.job.wd)


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


# def templateSet(job):
#     """
#     **moa template_set** - set a template parameter.

#     This only works for top level template parameters
#     """
#     template = _getTemplateFromData(job)
#     for i, a in enumerate(sysConf.args):
#         print i,a
#         if i == 0 and not '=' in a: continue
#         elif not '=' in a:
#             moa.ui.exitError("Do not know how to set '%s'" % a)
#         k, v = a.split('=', 1)
#         template[k] = v
#         template.modification_data = time.asctime()
#         template.save()


#@moa.args.addFlag('-d', dest='desc', help='adds a short description')
@moa.args.command
def list(job, args):
    """
    Lists all known local templates

    Print a list of all templates known to this moa installation. This
    includes locally installed templates as well.
    """

    for name in moa.template.templateList():
        if False:  # args.desc:
            # does not work for the time being -
            ti = moa.template.getMoaFile(name)
            txt = moa.ui.fformat(
                '{{bold}}%s:%s{{reset}}:{{cyan}} %s{{reset}}'
                % (name[0], name[1], ti.description),
                f='jinja')
            for line in textwrap.wrap(txt, initial_indent=' - ', width=80,
                                      subsequent_indent='   '):
                print line
        else:
            print '%s:%s' % name


@moa.args.private
@moa.args.command
def template(job, args):
    """
    **moa template** - Print the template name of the current job

    Usage::

        moa template


    """
    moa.ui.fprint(job.template.name)


@moa.args.private
@moa.args.command
def dumpTemplate(job, args):
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
