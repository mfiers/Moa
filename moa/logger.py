#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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


class MoaFormatter(logging.Formatter):
    """
    A somewhat more advanced formatter
    """

    def formatTime(self, record, datefmt):
        return time.strftime("%d%m%y:%H%M%S")

    def format(self, record):
        """
        Defines two extra fields in the record class, upon formatting:
        - visual, a visual indication of the severity of the message
        - tb, a formatted traceback, used when sending mail
        @param record: the log message record
        """
        record.coloff = chr(27) + "[0m"
        record.colon = chr(27) + "[1m"

        if record.levelno <= logging.DEBUG:
            record.colon = chr(27) + "[30m" + chr(27) + "[47m"
            record.visual = "#DBUG "
            record.vis1 = "DBG"
        elif record.levelno <= logging.INFO:
            record.colon = chr(27) + "[30m" + chr(27) + "[42m"
            record.visual = "#INFO "
            record.vis1 = "INF"
        elif record.levelno <= logging.WARNING:
            record.visual = "#WARN "
            record.colon = chr(27) + "[30m" + chr(27) + "[46m"
            record.vis1 = "WRN"
        elif record.levelno <= logging.ERROR:
            record.visual = "#ERRR "
            record.vis1 = "ERR"
            record.colon = chr(27) + "[30m" + chr(27) + "[43m"
        else:
            record.colon = chr(27) + "[30m" + chr(27) + "[41m"
            record.visual = "#CRIT "
            record.vis1 = "CRT"

        record.blue = chr(27) + "[34m"
        record.green = chr(27) + "[32m"

        record.msg = " ".join(str(record.msg).split(" "))

        #check if we're on a tty, if not, reset colon/coloff
        if not sys.stdout.isatty():
            record.colon = ""
            record.coloff = ""

        trext = traceback.extract_stack()
        if len(trext) > 11:
            caller = trext[-11]
        else:
            caller = trext[0]

        record.file = caller[0]
        module = os.path.basename(record.file).replace('.py', '')
        if module == '__init__':
            module = os.path.basename(
                record.file.replace('/__init__.py', '')) + '.m'

        record.module = module
        record.lineno = str(caller[1])
        record.function = caller[2]

        #check if there is an env variable that prevents ANSI
        #coloring
        if 'MOAANSI' in os.environ and \
           os.environ['MOAANSI'] == 'no':
            record.blue = ""
            record.green = ""
            record.colon = ""
            record.coloff = ""

        try:
            fmtter = logging.Formatter.format(self, record)
        except TypeError:
            print "Error with record %s" % record
            print dir(record)
            print record.args
            print 'msg:', record.msg
            print record.module
            raise

        return fmtter

LOGGER = logging.getLogger()
handler = logging.StreamHandler()
logmark = chr(27) + '[0;45mⲮ' + chr(27) + '[0m'

normalFormatter = MoaFormatter(logmark + '%(colon)s%(vis1)s%(coloff)s ' +
                               '%(name)s - %(message)s')
handler.setFormatter(normalFormatter)
LOGGER.addHandler(handler)

#logging.basicConfig(format=logmark +
#                    ' %(name)s - %(message)s',
#                    datefmt='%y/%m/%d %H:%M:%S')


def exitError(message=""):
    l.critical("Deprecated function call - do not " +
               "use logger.exitError, but moa.ui.exitError")
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
