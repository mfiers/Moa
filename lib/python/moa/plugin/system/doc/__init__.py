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

import jinja2
import socket
import getpass
import datetime
import subprocess

import moa.ui
import moa.args
import moa.utils
import moa.logger
l = moa.logger.getLogger(__name__)
from moa.sysConf import sysConf

from moa.plugin.system.doc import pelican_util


def hook_finish():

    if not sysConf.commands[sysConf.args.command]['logJob']:
        return

    if sysConf.args.command == 'change':
        #this is already taken care of!
        return

    message = moa.ui._textFormattedMessage([
        'changelog', sysConf.args.changeMessage,
        sysConf.doc.changeMessage
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

    if title is None:
        title = txt[0]
        txt = txt[1:]

    txt = "\n".join(txt).rstrip() + "\n"

    #title = "%s" % category.capitalize()

    with open(filename, "w") as F:
        F.write("Title: %s\n" % title)
        F.write("Author: %s\n\n" % getpass.getuser())
        F.write("\n".join(txt))


def _readFromuser(job, header):
    """
    gather blog or changelog information
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

    sys.stdin = oldstdin
    return txt


@moa.args.needsJob
@moa.args.argument('message', nargs='*')
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


    if args.message:
        message = [" ".join(args.message)]
    else:
        message = _readFromuser(
            job,
            header="Enter your BLOG message (ctrl-d on an empty " +
            "line to finish)")

    if sin:
        message.append("\nStdin:\n")
        message.extend(["    " + x for x in sin.split("\n")])


    _writeMessage('blog', message)

    moa.ui.message("Created a blog entry", store=False)
    sysConf.doc.blog = "\n".join(message)

def _getFromStdin():
    import re

    if not sys.stdin.isatty():
        m = sys.stdin.read()
        #print m
        m = re.sub(r'\x1b\[[^m]*m', '', m)
        #print m
        return m
    return ""


@moa.args.needsJob
@moa.args.argument('message', nargs='*')
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
            job,
            header="Enter your CHANGELOG message (ctrl-d on an empty " +
            "line to finish)")

    if sin:
        message.append("\nStdin:\n")
        message.extend(["    " + x for x in sin.split("\n")])

    _writeMessage('change', message)

    moa.ui.message("Created a changelog entry", store=False)
    sysConf.doc.changeMessage = "\n".join(message)


@moa.args.doNotLog
@moa.args.needsJob
@moa.args.command
def pelican(job, args):
    """
    Run pelican :)
    """

    jenv = jinja2.Environment(
        loader=jinja2.PackageLoader('moa.plugin.system.doc'))
    sysConf.plugins.pelican.jenv = jenv

    themedir = os.path.join(os.path.dirname(__file__), 'theme')

    sysConf.doc.server = socket.gethostname()
    peliconf = '.moa/pelican.conf.py'
    renderdir = '.moa/doc/pelican'

    if not os.path.exists('.moa/doc/pages'):
        os.makedirs('.moa/doc/pages')

    #call a plugin hook to let other plugins generate pelican pages
    # (if they want to)

    job.pluginHandler.run('pelican', job=job)
    sysConf.pluginHandler.run('pelican')

    pelican_util.generate_parameter_page(job)
    pelican_util.generate_file_page(job)
    pelican_util.generate_readme_page(job)
    pelican_util.generate_template_page(job)

    jtemplate = jenv.select_template(['pelican.conf.jinja2'])

    txt = jtemplate.render(sysConf)
    with open(peliconf, 'w') as F:
        F.write(txt)

    if not os.path.exists(renderdir):
        os.makedirs(renderdir)

    cl = ('pelican -q -t %s -m md -s .moa/pelican.conf.py ' +
          '-o .moa/doc/pelican/ .moa/doc/') % (themedir)

    l.debug("Executing pelican:")
    l.debug("   %s" % cl)
    subprocess.Popen(cl, shell=True)

    #create a redirect page to the proper index.thml
    pelican_util.generate_redirect(job)


@moa.args.needsJob
@moa.args.command
def readme(job, args):
    """
    Edit the README.md file for this job

    You could, obviously, also edit the file yourself - this is a mere
    shortcut - maybe it will stimulate you to maintain a README file
    """
    subprocess.call(
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
