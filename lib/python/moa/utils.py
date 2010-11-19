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
Moa script - random utilities
"""

import os
import re
import sys
import time
import glob
import errno
import shutil
import readline
import traceback
import contextlib

import moa.logger as l
from moa.exceptions import *

# Get a file lock, adapted from:
#  http://code.activestate.com/recipes/576572/
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


def getMoaBase():
    if os.environ.has_key('MOABASE'):
        MOABASE = os.environ["MOABASE"]
    else:
        MOABASE = '/usr/share/moa'
        #for use by depending scripts
        os.putenv('MOABASE', MOABASE)
    return MOABASE

def moaDirOrExit(job):
    """
    Check if the job resides in a moa directory, if not, exit
    with an error message
    """
    if not job.isMoa():
        l.error("This command must be executed in a Moa job directory")
        sys.exit(-1)

def deprecated(func):
    """
    Decorator to flag a function as deprecated
    """
    def depfunc(*args, **kwargs):
        l.critical('Calling deprecated function %s' % func.__name__)
        l.critical("\n" + "\n".join(traceback.format_stack()))
        func(*args, **kwargs)
    return depfunc

################################################################################
##
## readline enabled user prompt
##
################################################################################

## Handle moa directories
def fsCompleter(text, state):
    if os.path.isdir(text) and not text[-1] == '/': text += '/'
    pos = glob.glob(text + '*')
    try:
        return pos[state]
    except IndexError:
        return None
    
def askUser(prompt, d):
    
    def startup_hook():
        readline.insert_text('%s' % d)
  
    readline.set_completer_delims("\n `~!@#$%^&*()-=+[{]}\|;:'\",<>?")
    #readline.set_pre_input_hook(_rl_set_hook)

    readline.set_startup_hook(startup_hook)

    readline.set_completer(fsCompleter)
    readline.parse_and_bind("tab: complete")
    
    vl = raw_input(prompt)

    readline.set_startup_hook() 
    return vl 
    
    
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
