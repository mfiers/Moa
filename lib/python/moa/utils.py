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

import os
import sys
import time
import glob
import errno
import readline
import traceback
import subprocess
import contextlib

import moa.utils
import moa.logger as l

def getProcessInfo(pid):
    """
    Return some info on a process
    """
    cl = ('ps --no-heading -fp %s' % (pid)).split()
    p = subprocess.Popen(cl, stdout=subprocess.PIPE)
    out = p.communicate()[0].strip().split(None, 7)
    if not out: return {}
    pi = dict(zip(
        'uid pid ppid c stime tty time cmd'.split(), out))

    #check if this is moa invocation
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
    if os.environ.has_key('MOABASE'):
        MOABASE = os.environ["MOABASE"]
    else:
        MOABASE = '/usr/share/moa'
        #for depending scripts
        os.putenv('MOABASE', MOABASE)
    return MOABASE

def moaDirOrExit(job):
    """
    Check if the job contains a proper Moa job, if not, exit with an
    error message and a non-zero exit code.

    :param job: An instance of :class:`moa.job.Job`
    """
    if not job.isMoa():
        moa.ui.exitError("This command must be executed in a Moa job directory")
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
                    
