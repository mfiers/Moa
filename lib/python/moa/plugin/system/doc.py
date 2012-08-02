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
import os
import sys
import getpass
import datetime
import subprocess

import moa.ui
import moa.args
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

# def hook_prepare_3():
#     if not job.template.parameters.has_key('title'):
#         job.template.parameters.title = {
#             'optional' : False,
#             'help' : 'A short and consise title for this job',
#             'type' : 'string',
#             'recursive' : False,
#             }

def hook_finish():

    job = sysConf['job']
    
    if not sysConf.commands[sysConf.args.command]['logJob']:
        return

    message = moa.ui._textFormattedMessage(
        [sysConf.args.changeMessage,
         sysConf.doc.changeMessage] )
    
    if message:
        _appendMessage(
            fileName="CHANGELOG.md",
            txt = message)
    
def hook_defineOptions():
    sysConf.argParser.add_argument(
        '-m', action='store',
        dest='changeMessage', help = 'Change message for this operation')

def _appendMessage(fileName, txt):
    """
    Append a markdown formatted message to either CHANGELOG or BLOG

    :param txt: message to save
    :type txt: array of strings
    """
    try:
        with open(fileName) as F:
            oldFile = F.read()
    except IOError:
        oldFile = ""

    with open(fileName, "w") as F:
        now = datetime.datetime.now()
        header = "**%s - %s changes**" % (
            now.strftime("On %A, %d %b %Y %H:%M"), getpass.getuser()) 
        F.write("%s\n\n" %  header)
        F.write("    " + "\n    ".join(txt))
        F.write("\n-----\n")
        F.write(oldFile)

def _readFromuser(job, header, fileName):
    """
    gather Blog or CHANGELOG information
    """

    #moa.utils.moaDirOrExit(job)

    oldstdin = sys.stdin
    sys.stdin = open('/dev/tty')
    txt = []
    print header, "..."
    while True:
        try:
            line = raw_input("")
            txt.append(line)
        except (EOFError, KeyboardInterrupt):
            break
        
    _appendMessage(fileName, txt)
    sys.stdin = oldstdin
    return txt

@moa.args.command
def blog(job, args):
    """
    Add an entry to the job blog (BLOG.md)

    Allows a user to maintain a blog for this job (in BLOG.md). Use as
    follows::

        $ moa blog
        Enter your blog message (ctrl-d on an empty line to finish)

        ... enter your message here ..
        
        [ctrl-d]

    Note: the ctrl-d needs to be given on an empty line. The text is
    appended to moa.desciption. In the web interface this is converted
    to Markdown_.

    .. _Markdown: http://daringfireball.net/projects/markdown/ markdown.
    """

    sin = _getFromStdin()


    message = _readFromuser(
        job, 
        header="Enter your blog message (ctrl-d on an empty line to finish)",
        fileName="BLOG.md")

    if sin:
        message.append("\nStdin:\n")
        message.extend(["   " + x for x in sin.split("\n")])

    moa.ui.message("Created a blog entry", store=False)
    sysConf.doc.blog = message

def _getFromStdin():
    import re
    
    if not sys.stdin.isatty():
        m = sys.stdin.read()
        #print m
        m = re.sub(r'\x1b\[[^m]*m', '', m)
        #print m
        return m
    return ""

@moa.args.command
def change(job, args):
    """
    Add entry to CHANGELOG.md
    
    This function allows the user to add an entry to CHANGELOG.md
    (including a timestamp). Use it as follows::

        $ moa change
        Enter your changelog message (ctrl-d on an empty line to finish)

        ... enter your message here ..
        
        [ctrl-d]

    Note: the ctrl-d needs to be given on an empty line. The text is
    appended to moa.desciption. In the web interface this is converted
    to Markdown_.

    .. _Markdown: http://daringfireball.net/projects/markdown/ markdown.

    Note the same can be achieved by specifying the -m parameter
    (before the command - for example:

    `moa -m 'intelligent remark' set ...`

    Note. It is also possible to cat some text into moa change:

    wc -l | moa change 

    Moa will still query you for a message and append the data from
    stdin to the message
    

    """

    sin = _getFromStdin()

    message = _readFromuser(
        job, 
        header="Enter your CHANGELOG message (ctrl-d on an empty " +
        "line to finish)", fileName="CHANGELOG.md")

    if sin:
        message.append("\nStdin:\n")
        message.extend(["   " + x for x in sin.split("\n")])

    moa.ui.message("Created a changelog entry", store=False)
    sysConf.doc.changeMessage = "\n".join(message)


@moa.args.command
def readme(job, args):
    """
    Edit the README.md file for this job

    You could, obviously, also edit the file yourself - this is a mere
    shortcut - maybe it will stimulate you to maintain a README file
    """    
    subprocess.call(os.environ.get('EDITOR','nano').split() + ['README.md'])

def _update_git(filename):
    """
    Check if a file is under version control & commit changes    
    """
    job = sysConf.job
    if not sysConf.git.repo:
        #repo is not initalized..(not in a repository?)
        return
    
    if os.path.exists(filename):    
        sysConf.git.repo.index.add([filename])
        sysConf.git.commitJob(job, 'Worked on %s in  %s' % (filename, job.wd))
        
    
def hook_git_finish_readme():
    """
    Execute just after setting running moa readme
    """
    _update_git('README.md')

def hook_git_finish_blog():
    """
    Execute just after setting running moa blog
    """
    _update_git('BLOG.md')


def hook_git_finish_change():
    """
    Execute just after setting running moa blog
    """
    _update_git('CHANGELOG.md')
