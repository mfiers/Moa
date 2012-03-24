#!/usr/bin/env python
# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
import os
import sys
import time
import logging
from logging import DEBUG, INFO, WARNING, CRITICAL

import traceback
LOGGER  = logging.getLogger('moa')

handler = logging.StreamHandler()

logmark = chr(27) + '[0;45mMOA' + \
          chr(27) + '[0m ' 

logging.basicConfig(format=logmark + '%(levelname)s|%(asctime)s|%(name)s # %(message)s', datefmt='%y/%m/%d %H:%M:%S')

def exitError(message=""):
    l.critical("Deprecated function call - do not use logger.exitError, but moa.ui.exitError")
    if message:
        LOGGER.fatal(message)
    sys.exit(-1)

def setLevel(level):
    if level == logging.DEBUG:
        LOGGER.setLevel(logging.DEBUG)        
    else:
        LOGGER.setLevel(level)
    
def setVerbose():
    LOGGER.setLevel(logging.DEBUG)

def setSilent():
    LOGGER.setLevel(logging.CRITICAL)

def setWarning():
    LOGGER.setLevel(logging.WARNING)

def setInfo():
    LOGGER.setLevel(logging.INFO)

def _callLogger(logFunc, args, kwargs):
    if len(args) == 1:
        logFunc(args[0])
    elif args:
        logFunc(", ".join(map(str, args)))
    if kwargs:
        for k in kwargs.keys():
            logFunc(" - %s : %s" % (k, kwargs[k]))

def getLogger(name):
    return logging.getLogger(name)
    
def debug(*args, **kwargs):
    _callLogger(LOGGER.debug, args, kwargs)

def info(*args, **kwargs):
    _callLogger(LOGGER.info, args, kwargs)

def warning(*args, **kwargs):
    _callLogger(LOGGER.warning, args, kwargs)

def error(*args, **kwargs):
    _callLogger(LOGGER.error, args, kwargs)


def critical(*args, **kwargs):
    _callLogger(LOGGER.critical, args, kwargs)

    
