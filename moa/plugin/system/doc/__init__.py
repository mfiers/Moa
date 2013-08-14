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
import datetime
import getpass
import os
import pwd
import socket
import subprocess as sp
import sys
import time

import jinja2
import moa.args
import moa.logger
import moa.ui
from moa.sysConf import sysConf


l = moa.logger.getLogger(__name__)


def hook_prepare_3():
    job = sysConf['job']

    job.template.parameters.title = {
        'optional': False,
        'help': 'Job title',
        'recursive': False,
        'type': 'string'}


def hook_finish():

    if not sysConf.commands[sysConf.args.command]['logJob']:
        return

    if sysConf.args.command == 'change':
        #this is already taken care of!
        return

    message = moa.ui._textFormattedMessage([
        'changelog', sysConf.args.changeMessage,
        sysConf.plugins.doc.changeMessage
    ])

    if message:
        _writeMessage(
            category='change',
            txt=message)


def hook_defineOptions():
    sysConf.argParser.add_argument(
        '-m', action='store',
        dest='changeMessage', help='Change message for this operation')


def _writeMessage(category, txt, title=None):
    """
    Append a markdown formatted message to either CHANGELOG or BLOG

    :param category: the category of message
    :param title: an optional title for the message
    :type title: string
    :param txt: message to save
    :type txt: array of strings
    """

    dirname = os.path.join('.moa', 'doc', category)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    now = datetime.datetime.now()

    filename = os.path.join(dirname, '%s_%d%d%d_%d%d%d.md' % (
        category, now.year, now.month, now.day,
        now.hour, now.minute, now.second))

    while txt[0].strip() == "":
        txt = txt[1:]

    if title is None or title.strip() == "":
        title = '%s %d/%d/%d %d:%d:%d' % (
            category, now.year, now.month, now.day,
            now.hour, now.minute, now.second)

    txt = "\n".join(txt).rstrip() + "\n"

    #:date: 2010-10-03 10:20
    with open(filename, "w") as F:
        F.write("Title: %s\n" % title)
        F.write("Author: %s\n" % getpass.getuser())
        F.write("Date: %s\n\n" % (
            now.strftime("%Y-%m-%d %H:%M")))
        F.write(txt)


def _readFromuser(job, ):
    """
    get a message from the user
    """

    oldstdin = sys.stdin
    sys.stdin = open('/dev/tty')
    txt = []
    print "Enter your message. First line is used as title."
    print "Ctrl-d on an empty line to finish..."
    while True:
        try:
            line = raw_input("")
            txt.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    sys.stdin = oldstdin
    return txt


@moa.args.needsJob
@moa.args.argument('message', nargs='*')
@moa.args.argument('-t', '--title', help='mandatory job title')
@moa.args.command
def blog(job, args):
    """
    Add an entry to the job blog (in .moa/doc/blog/)

    Allows a user to maintain a blog for this job. Use as
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

    if args.title is None:
        moa.ui.exitError("Please provide a blog title using -t")

    sin = _getFromStdin()

    if args.message:
        message = [" ".join(args.message)]
    else:
        message = _readFromuser(
            job)

    if sin:
        message.append("\nStdin:\n")
        message.extend(["    " + x for x in sin.split("\n")])

    _writeMessage('blog', message, title=args.title)

    moa.ui.message("Created a blog entry", store=False)
    sysConf.plugins.doc.blog = "\n".join(message)


def _getFromStdin():
    import re

    if not sys.stdin.isatty():
        m = sys.stdin.read()
        m = re.sub(r'\x1b\[[^m]*m', '', m)
        return m
    return ""


def _readArticle(filename):
    article = {}
    body = []
    with open(filename) as F:
        #read header
        for line in F:
            if not ':' in line:
                break

            key, val = line.split(':', 1)
            if not key in ['Title', 'Author', 'Date']:
                break
            article[key] = val.strip()

        body.append(line)
        for line in F:
            body.append(line)

    while body and not(body[0].strip()):
        body = body[1:]
    while body and not(body[-1].strip()):
        body = body[:-1]

    article['Body'] = body

    if 'Date' in article:
        article['Date'] = datetime.datetime.strptime(
            article['Date'], "%Y-%m-%d %H:%M")
    else:
        article['Date'] = time.ctime(os.path.getctime(file))

    if not 'Author' in article:
        stat_info = os.stat(filename)
        uid = stat_info.st_uid
        article['Author'] = pwd.getpwuid(uid)[0]

    return article


@moa.args.needsJob
@moa.args.doNotLog
@moa.args.argument('no_entries', type=int, default=10, nargs='?',
                   help="No of changelog entries to show (default 10)")
@moa.args.command
def changelog(job, args):
    """
    Print a changelog to stdout
    """
    _show_stuff('change', args.no_entries)


@moa.args.needsJob
@moa.args.doNotLog
@moa.args.argument('no_entries', type=int, default=10, nargs='?',
                   help="No of blog entries to show (default 10)")
@moa.args.command
def showblog(job, args):
    """
    Print a changelog to stdout
    """
    _show_stuff('blog', args.no_entries)


def _show_stuff(category, no_messages):
    stuff_dir = os.path.join('.moa', 'doc', category)
    #use shell shortcut to find the latest messages
    cl = 'ls %s -t | head -%d' % (stuff_dir, no_messages)
    P = sp.Popen(cl, shell=True, stdout=sp.PIPE)
    out, _ = P.communicate()
    for entry in out.split("\n"):
        entry = entry.strip()
        if not entry:
            continue
        fname = os.path.join(stuff_dir, entry)
        article = _readArticle(fname)
        print "%s  %s" % (article['Date'], article['Author'])
        print "    Title: %s\n" % article['Title']
        for line in article['Body']:
            print "    %s" % line.rstrip()
        print "\n"


@moa.args.needsJob
@moa.args.argument('message', nargs='*')
@moa.args.argument('-t', '--title', help='mandatory job title')
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

    if args.message:
        message = [" ".join(args.message)]
    else:
        message = _readFromuser(
            job)

    if sin:
        message.append("\nStdin:\n")
        message.extend(["    " + x for x in sin.split("\n")])

    _writeMessage('change', message, title=args.title)

    moa.ui.message("Created a changelog entry", store=False)
    sysConf.plugins.doc.changeMessage = "\n".join(message)

@moa.args.needsJob
@moa.args.command
def readme(job, args):
    """
    Edit the README.md file for this job

    You could, obviously, also edit the file yourself - this is a mere
    shortcut - maybe it will stimulate you to maintain a README file
    """
    sp.call(
        os.environ.get('EDITOR', 'nano').split() + ['README.md'])


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
