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


def moaRecursiveWalk(wd, callback, data, recursive=True):
    """
    Function used in recursive moa commands -

    this function takes the 'wd', walks through all subdirectories
    (excluding those starting with a '.') and running the callback
    function on that directory.

    If recursive == False - just execute the callback & return
    """
    if not recursive:
        callback(wd, data)
        return

    for path, dirs, files in os.walk(wd):
        if '.moa' in dirs:

            #potentially a moa dir
            #call the callback
            callback(path, data)

            #remove all '.' directories - 
            toRemove = [x for x in dirs if x[0] == '.']
            [dirs.remove(t) for t in toRemove]

@contextlib.contextmanager
def flock(path, waitDelay=.1, maxWait=100):
    """
    Create a file lock

    Adapted from: http://code.activestate.com/recipes/576572/

    

    """
    waited = 0
    waitedTooLong = False
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            waited += waitDelay
            time.sleep(waitDelay)
            if waited > maxWait:
                waitedTooLong = True
                break
            else:
                continue
        else:
            break
    if waitedTooLong:
        raise Exception('CannotGetAFileLock for %s' % path)
    try:
        yield fd
    finally:
        os.unlink(path)

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
    exactly. This seems the most likely source;
    
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
                    

# #def logCaller():
#     def _m(func):
#         def _f(*args, **kwargs):
#             import traceback
#             _n = func.__name__
#             caller = traceback.extract_stack()[-3]
#             print caller
#             for l in  traceback.format_stack():
#                 print l
#                 #    with open("logCallerl.error("calling %s" % func)
#             return func
#         return _f
#     return _m
    
def logCaller(func):
    """
    Profiler decorator
    """
    import traceback
    def _func(*args, **kargs):
        ch = []
        for c in traceback.extract_stack()[:-1]:
            blue = chr(27) + "[37m" + chr(27) + '[46m'
            red = chr(27) + "[37m" + chr(27) + '[41m'
            green = chr(27) + "[37m" + chr(27) + '[42m'
            coloff = chr(27) + "[0m"
            sys.stderr.write(' --- %s%s%s@%s%s%s:%s%05d%s\n' % (
                blue, c[2], coloff,
                green, c[0], coloff,
                red, c[1], coloff))
        res = func(*args, **kargs)
        return res
    return _func

def logCallerVerbose(func):
    """
    Profiler decorator
    """
    import traceback
    def _func(*args, **kargs):
        ch = []
        l.error("### CALLING %s" % func.__name__)
        for c in traceback.extract_stack()[-8:]:
            l.error("### TB %s %s %s" % (
                c[0].split('/')[-1],
                c[2], c[1]))
        l.error("### ARGS %s " % " ".join(args))
        l.error("### KWRG %s" % str(kargs))
        res = func(*args, **kargs)
        return res
    return _func

def profiler2(func):
    """
    Profiler decorator
    """
    import time
    def _func(*args, **kargs):
        start = time.time()
        res = func(*args, **kargs)
        l.critical("executed %s %s" % (func, time.time() - start))
        return res
    return _func
