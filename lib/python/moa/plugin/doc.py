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

def prepare_3(data):
    job = data['job']

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

def defineCommands(data):
    """
    Set the moa commands for this plugin
    """
    data['commands']['blog'] = {
        'desc' : 'record a short note',
        'usage' : 'moa blog',
        'call' : blog,
        'needsJob' : True,
        'log' : True
        }


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
    moa.utils.moaDirOrExit(job)

    txt = []
    while True:
        try:
            line = raw_input("")
            txt.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    message = "\n".join(txt)
    with open('moa.description', "a") as F:
        now = datetime.datetime.now()
        F.write("\n")
        header = "%s - %s writes::" % (
            now.isoformat(" "), getpass.getuser()) 
        F.write("%s\n" %  header)
        F.write("%s\n" % ("=" * len(header)))
        F.write(message)
        F.write("\n")
