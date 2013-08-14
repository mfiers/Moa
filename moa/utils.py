#!/usr/bin/env python
# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
moa.utils
---------

A set of random utilities used by Moa
"""

from email.mime.text import MIMEText
import fcntl
import os
import smtplib
import struct
import subprocess
import sys
import termios
import traceback

import moa.utils
import moa.logger as l


def sendmail(server, sender, recipient, subject, message):
    """
    Send an email.
    """
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    smtp_server = smtplib.SMTP(server)
    smtp_server.sendmail(sender, [recipient], msg.as_string())
    smtp_server.quit()


def niceRunTime(d):
    """
    Nice representation of the run time
    d is time duration string
    """
    d = str(d)
    if ',' in d:
        days, time = d.split(',')
    else:
        days = 0
        time = d

    hours, minutes, seconds = time.split(':')
    hours, minutes = int(hours), int(minutes)
    seconds, miliseconds = seconds.split('.')
    seconds = int(seconds)
    miliseconds = int(miliseconds)

    if days > 0:
        if days == 1:
            return "1 day, %d hrs" % hours
        else:
            return "%d days, %d hrs" % (days, hours)

    if hours == 0 and minutes == 0 and seconds == 0:
        return "<1 sec"
    if hours > 0:
        return "%d:%02d hrs" % (hours, minutes)
    elif minutes > 0:
        return "%d:%02d min" % (minutes, seconds)
    else:
        return "%d sec" % seconds


def getCwd():
    """
    Do not use os.getcwd() -
    need to make sure symbolic links do not get dereferenced

    hijacked some code from:
    http://stackoverflow.com/questions/123958/how-to-get-set-logical-directory-path-in-python
    """

    cwd = os.environ.get("PWD")
    if cwd is not None:
        return cwd

    # no environment. fall back to calling pwd on shell
    cwd = subprocess.Popen(
        'pwd',
        stdout=subprocess.PIPE).communicate()[0].strip()
    return cwd


def getTerminalSize():
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])


def getProcessInfo(pid):
    """
    Return some info on a process
    """
    cl = ('ps --no-heading -fp %s' % (pid)).split()
    p = subprocess.Popen(cl, stdout=subprocess.PIPE)
    out = p.communicate()[0].strip().split(None, 7)

    if not out:
        return {}

    pi = dict(zip(
        'uid pid ppid c stime tty time cmd'.split(), out))

    # check if this is moa invocation
    if 'python' in pi['cmd'] and \
       'moa' in pi['cmd']:
        pi['moa'] = True
    else:
        pi['moa'] = False
    return pi


def getMoaBase():
    """
    Return MOABASE - the directory where Moa is installed. This
    function also sets an environment variable `MOABASE`

    >>> d = getMoaBase()
    >>> assert(os.path.isdir(d))
    >>> assert(os.path.isfile(os.path.join(d, 'README')))
    >>> assert(os.path.isdir(os.path.join(d, 'lib')))

    :rtype: string (path)
    """
    if 'MOABASE' in os.environ:
        MOABASE = os.environ["MOABASE"]
        return MOABASE

    thif = os.path.dirname(os.path.dirname(__file__))
    if thif[-4:] == '.egg':
        MOABASE = thif
    else:
        MOABASE = '/usr/share/moa'

    # for depending scripts
    os.putenv('MOABASE', MOABASE)
    return MOABASE


def moaDirOrExit(job):
    """
    Check if the job contains a proper Moa job, if not, exit with an
    error message and a non-zero exit code.

    :param job: An instance of :class:`moa.job.Job`
    """
    if not job.isMoa():
        moa.ui.exit("Need a Moa job")
        sys.exit(-1)


def deprecated(func):
    """
    Decorator function to flag a function as deprecated

    :param func: any function
    """
    def depfunc(*args, **kwargs):
        l.critical('Calling deprecated function %s' % func.__name__)
        l.critical("\n" + "\n".join(traceback.format_stack()))
        func(*args, **kwargs)
    return depfunc


def printstack(func):
    """
    Decorator function to print stack

    :param func: any function
    """
    def depfunc(*args, **kwargs):
        l.critical("\n" + "\n".join(traceback.format_stack()[:-1]))
        func(*args, **kwargs)
    return depfunc


def simple_decorator(decorator):
    """
    This decorator can be used to turn simple functions into
    well-behaved decorators, so long as the decorators are fairly
    simple. If a decorator expects a function and returns a function
    (no descriptors), and if it doesn't modify function attributes or
    docstring, then it is eligible to use this. Simply apply
    @simple_decorator to your decorator and it will automatically
    preserve the docstring and function attributes of functions to
    which it is applied.

    Note; I got this code from somehwere, but forgot where
    exactly. This seems the most likely source:

    http://svn.navi.cx/misc/trunk/djblets/djblets/util/decorators.py

    """
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


@simple_decorator
def flog(func):
    """
    A simple logger - uses the :mod:`moa.logger` code to log the
    calling function. Use as a decorator::

        @moa.utils.flog
        def any_function(*args);
            ...

    This is for debugging purposes (obviously)

    :param func: Any python function
    """
    def flogger(*args, **kwargs):
        l.critical("Executing %s" % func.__name__)
        for a in args:
            l.error("  - calling with arg %s" % a)
        for k in kwargs.keys():
            l.error("  - calling with kwargs %s=%s" % (k, kwargs[k]))
        return func(*args, **kwargs)
    return flogger
