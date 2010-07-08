#!/usr/bin/env python
# 
# Copyright 2009 Mark Fiers, Plant & Food Research
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
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
"""
Moa script - utilities
"""

import os
import re
import sys
import time
import glob
import errno
import shutil
import readline
import contextlib

import moa.job
import moa.logger as l
from moa.exceptions import *

# Get a file lock, adapted from:
#  http://code.activestate.com/recipes/576572/
#
@contextlib.contextmanager
def flock(path, wait_delay=.1, max_wait=100):
    waited = 0
    waited_too_long = False
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
            waited += wait_delay
            time.sleep(wait_delay)
            if waited > max_wait:
                waited_too_long = True
                break
            else:
                continue
        else:
            break
    if waited_too_long:
        raise CannotGetAFileLock(path)
    try:
        yield fd
    finally:
        os.unlink(path)

def exit(rc=0):
    for h in l.handlers:
        h.flush()
    sys.exit(rc)


################################################################################
## Handle moa directories

def fsCompleter(text, state):
    if os.path.isdir(text) and not text[-1] == '/': text += '/'
    pos = glob.glob(text + '*')
    try:
        return pos[state]
    except IndexError:
        return None
    
def askUser(prompt, default):
        
    def _rl_set_hook():
        readline.insert_text(default)
    readline.set_completer_delims("\n `~!@#$%^&*()-=+[{]}\|;:'\",<>?")
    readline.set_startup_hook(_rl_set_hook)
    readline.set_completer(fsCompleter)
    readline.parse_and_bind("tab: complete")
    
    vl = raw_input(prompt)
    readline.set_startup_hook() 
    return vl    


    
def renumber(path, fr, to):
    """
    Renumber a moa job

    >>> removeFiles(P_EMPTY, recursive=True)
    >>> fromDir = os.path.join(P_EMPTY, '10.test')
    >>> problemDir = os.path.join(P_EMPTY, '20.problem')
    >>> toDir = os.path.join(P_EMPTY, '20.test')
    >>> os.mkdir(os.path.join(P_EMPTY, '10.test'))
    >>> os.path.exists(os.path.join(P_EMPTY, '10.test'))
    True
    >>> os.path.exists(toDir)
    False
    >>> renumber(P_EMPTY, '10', '20')
    >>> os.path.exists(fromDir)
    False
    >>> os.path.exists(toDir)
    True
    >>> os.mkdir(problemDir)
    >>> renumber(P_EMPTY, '20', '30')
    Traceback (most recent call last):
      File '/opt/moa/lib/python/moa/utils.py', line 114, in renumber
        raise MoaFileError(fullDir)
    MoaFileError: Moa error handling file

    
    @param path: the path to operate in
    @type path: String
    @param fr: number to rename from
    @type fr: String representing a number
    @param to: number to rename to
    @type to: String representing a number
    """

    frDir = None
    toDir = None
    l.debug("moa ren %s %s" % (fr, to))
    for x in os.listdir(path):        
        if x[0] == '.' : continue
        
        fullDir = os.path.join(path, x)

        xsplit = x.split('.')
        if xsplit[0] == fr:
            if frDir:
                l.error("more than one directory starting with %s" % fr)
                raise MoaFileError(fullDir)
            frDir = fullDir
            toDir = os.path.join(path, to + "." + ".".join(xsplit[1:]))
        if xsplit[0] == to:
            l.error("target directory starting with %s already exists" % to)
            raise MoaFileError(fullDir)

    if not frDir:
        l.error("Cannot find a directory starting with %s" % fr)
        raise MoaFileError(path)
    if not toDir:
        l.error("Cannot find a directory starting with %s" % to)
        raise MoaFileError(path)
    
    if not os.path.isdir(frDir):
        l.error("%s is not a directory" % frDir)
        raise MoaFileError(frDir)
    #if not os.path.isdir(toDir):
    #    l.error("%s is not a directory" % toDir)
    #    raise MoaFileError(toDir)

    l.info("renaming: %s" % (frDir))
    l.info("  to: %s" % (toDir))
    os.rename(frDir, toDir)
        
    

################################################################################
## remove & delete data
##


def removeMoaOutfiles(path, outName='moa'):
    """
    Remove only the .out and .err files, based on outName
    """
    for name in ['%s.out' % outName,
                 '%s.err' % outName]:
        ff = os.path.join(path, name)
        if os.path.isfile(ff):
            os.unlink(ff)
            
def removeMoaFiles(path):
    """
    Removes all moa related files from a directory


        >>> touch(os.path.join(P_EMPTY, 'Makefile'))
        >>> touch(os.path.join(P_EMPTY, 'moa.mk'))
        >>> touch(os.path.join(P_EMPTY, 'lock'))
        >>> touch(os.path.join(P_EMPTY, 'moa.runlock'))
        >>> touch(os.path.join(P_EMPTY, 'test.file'))
        >>> removeMoaFiles(P_EMPTY)
        >>> os.path.exists(os.path.join(P_EMPTY, 'Makefile'))
        False
        >>> os.path.exists(os.path.join(P_EMPTY, 'moa.mk'))
        False
        >>> os.path.exists(os.path.join(P_EMPTY, 'lock'))
        False
        >>> os.path.exists(os.path.join(P_EMPTY, 'moa.runlock'))
        False
        >>> os.path.exists(os.path.join(P_EMPTY, 'test.file'))
        True
        >>> os.unlink(os.path.join(P_EMPTY, 'test.file'))
        
    """
    for name in ['Makefile', 'moa.mk', 'lock', 'moa.runlock',
                 'moa.out', 'moa.err', 'moa.failed', 'moa.success']:
        ff = os.path.join(path, name)
        if os.path.isfile(ff):
            os.unlink(ff)

def touch(path, times=None):
    """
    as the unix 'touch' util
    
    Borrowed from:
    http://stackoverflow.com/questions/1158076/implement-touch-using-python

    >>> wd = moa.job.newTestJob('traverse')
    >>> testFile = os.path.join(wd, 'test.file')
    >>> os.path.exists(testFile)
    False
    >>> touch(testFile)
    >>> os.path.exists(testFile)
    True

    @param path: The filename to touch
    @type path: String    
    """
    with file(path, 'a'):
        os.utime(path, times)

        
        
def removeFiles(path, recursive=False):
    """
    Remove all files from a path, and all subdirectories if
    recursive==True

    >>> removeFiles(P_EMPTY, recursive=True)
    >>> touch(os.path.join(P_EMPTY, 'Makefile'))
    >>> subdir = os.path.join(P_EMPTY, 'test')
    >>> os.mkdir(subdir)
    >>> touch(os.path.join(subdir, 'test'))
    >>> os.path.exists(os.path.join(subdir, 'test'))
    True
    >>> os.path.exists(os.path.join(P_EMPTY, 'Makefile'))
    True
    >>> removeFiles(P_EMPTY)
    >>> os.path.exists(os.path.join(P_EMPTY, 'Makefile'))
    False
    >>> os.path.exists(os.path.join(P_EMPTY, 'test'))
    True
    >>> removeFiles(P_EMPTY, recursive=True)
    >>> os.path.exists(os.path.join(P_EMPTY, 'test'))
    False

    @param recursive: Include all subdirectories
    @type recursive: Boolean
    
    """
    for entry in os.listdir(path):
        this = os.path.join(path, entry)
        if os.path.isfile(this):
            os.unlink(this)
        elif os.path.isdir(this) and recursive:
            shutil.rmtree(this)
        
        
def removeDirectory(path):
    """
    dangerous utility - it complete deletes a directory

       >>> import tempfile
       >>> tempdir = tempfile.mkdtemp()
       >>> os.path.exists(tempdir)
       True
       >>> os.path.isdir(tempdir)
       True
       >>> removeDirectory(tempdir)
       >>> os.path.exists(tempdir)
       False
       
    """
    l.info("Removing %s" % path)
    shutil.rmtree(path)
    l.info("Finished removing %s" % path)


def simple_decorator(decorator):

    """

    This decorator can be used to turn simple functions into
    well-behaved decorators, so long as the decorators are fairly
    simple. If a decorator expects a function and returns a function
    (no descriptors), and if it doesn't modify function attributes or
    docstring, then it is eligible to use this. Simply apply
    E{@}simple_decorator to your decorator and it will automatically
    preserve the docstring and function attributes of functions to
    which it is applied.

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
        for c in traceback.extract_stack()[-4:-1]:
            ch.append("%s:%s:%s" % (
                c[0].split('/')[-1],
                c[2], c[1]))
        l.error("%s called by %s" % (
            func.__name__,
            ", ".join(ch)))
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
