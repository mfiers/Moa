# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**doc** - Manage job documentation
----------------------------------

Manage project / title / description for jobs

"""

import getpass
import datetime

import moa.ui
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

def hook_prepare_3():
    job = sysConf['job']

    job.template.parameters.title = {
        'optional' : False,
        'help' : 'A short title for this job',
        'type' : 'string',
        'recursive' : False,
        'default' : ''
        }
    
    job.template.parameters.project = {
        'optional' : True,
        'help' : 'Project name',
        'type' : 'string'
        }

def hook_defineOptions():
    sysConf.parser.add_option(
        '-m', action='store',
        dest='message', help = 'Message accompanying this operations - ' + 
        'used for git & changelogs ')

def hook_defineCommands():
    """
    Set the moa commands for this plugin
    """
    sysConf['commands']['blog'] = {
        'desc' : 'record a short note',
        'usage' : 'moa blog',
        'call' : blog,
        'needsJob' : True,
        'log' : True
        }


def _readFromuser(job, header, fileName):
    """
    gather Blog or Changelog information
    """
    moa.utils.moaDirOrExit(job)

    txt = []
    print header, "..."
    while True:
        try:
            line = raw_input("")
            txt.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    sysConf.job.data.blog.txt = "\n".join(txt)

    try:
        with open(fileName) as F:
            oldFile = F.read()
    except IOError:
        oldFile = ""

    with open(fileName, "w") as F:
        now = datetime.datetime.now()
        header = "**%s - %s writes**" % (
            now.strftime("On %A, %d %b %Y %H:%M"), getpass.getuser()) 
        F.write("%s\n\n" %  header)
        F.write("\n    ".join(txt))
        F.write("\n-----\n")
        F.write(oldFile)

def blog(job):
    """
    Allows a user to enter a short note that is appended to
    moa.description (including a timestamp). Use it as follows::

        $ moa blog
        Here you can enter a short, conscise, multi-
        line message describing what you have been
        doing
        [ctrl-d]

    Note: the ctrl-d needs to be given on an empty line. The text is
    appended to moa.desciption. In the web interface this is converted
    to Markdown_.

    .. _Markdown: http://daringfireball.net/projects/markdown/ markdown.
    """
    _readFromuser(
        job, 
        header="enter your blog message (ctrl-d on an empty line to finish)",
        fileName="blog.md")
                  
    
 
