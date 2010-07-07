#!/usr/bin/env python
#
# Copyright 2009 Mark Fiers
# Plant & Food Research
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
import os
import sys
import logging
import traceback

class XTRFormatter(logging.Formatter):
    """
    A somewhat more advanced formatter
    """

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
            record.vis1 = "DEBUG:"
        elif record.levelno <= logging.INFO:
            record.colon = chr(27) + "[30m" + chr(27) + "[42m"
            record.visual = "#INFO "
            record.vis1 = "INFO:"
        elif record.levelno <= logging.WARNING:
            record.visual = "#WARN "
            record.colon = chr(27) + "[30m" + chr(27) + "[46m"
            record.vis1 = "WARNING:"
        elif record.levelno <= logging.ERROR:
            record.visual = "#ERRR "
            record.vis1 = "ERROR:"
            record.colon = chr(27) + "[30m" + chr(27) + "[43m"
        else:
            record.colon = chr(27) + "[30m" + chr(27) + "[41m"
            record.visual = "#CRIT "
            record.vis1 = "CRITICAL:"

        record.msg = " ".join(record.msg.split(" "))
        #check if we're on a tty, if not, reset colon/coloff
        if not sys.stdout.isatty():
            record.colon = ""
            record.coloff = ""

        #check if there is an env variable that prevents ANSI
        #coloring
        if os.environ.has_key('MOAANSI') and \
           os.environ['MOAANSI'] == 'no':
            record.colon = ""
            record.coloff = ""
            
        return logging.Formatter.format(self, record)

class XTRFormatterD(logging.Formatter):
    """
    A somewhat more advanced formatter
    """

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
            record.vis1 = "DEBUG:"
        elif record.levelno <= logging.INFO:
            record.colon = chr(27) + "[30m" + chr(27) + "[42m"
            record.visual = "#INFO "
            record.vis1 = "INFO"
        elif record.levelno <= logging.WARNING:
            record.visual = "#WARN "
            record.colon = chr(27) + "[30m" + chr(27) + "[46m"
            record.vis1 = "WARNING"
        elif record.levelno <= logging.ERROR:
            record.visual = "#ERRR "
            record.vis1 = "ERROR"
            record.colon = chr(27) + "[30m" + chr(27) + "[43m"
        else:
            record.colon = chr(27) + "[30m" + chr(27) + "[41m"
            record.visual = "#CRIT "
            record.vis1 = "CRITICAL"

        t = []
        stack = traceback.extract_stack()[:-9]
        for s in stack:
            t.append("%s @ %s:%s : %s" % (s[2], s[0], s[1], s[3][:80]))
        #t = " ? " + " ? ".join(traceback.format_list(
        record.traceback =  " #? " + "\n #? ".join(t)

        record.msg = " ".join(record.msg.split(" "))
        #check if we're on a tty, if not, reset colon/coloff
        if not sys.stdout.isatty():
            record.colon = ""
            record.coloff = ""
            
        return logging.Formatter.format(self, record)

l = logging.getLogger('moa')
handler = logging.StreamHandler()
logmark = chr(27) + '[0;44mU' + \
          chr(27) + '[0m ' 


normalFormatter = XTRFormatter('%(colon)s%(vis1)s%(coloff)s %(message)s')
debugFormatter =  XTRFormatter('%(colon)s%(vis1)s%(coloff)s %(asctime)s: %(message)s @ %(filename)s:%(lineno)d')
debugFormatterX = XTRFormatterD(
    '#' * 80 + '\n##%(colon)s%(vis1)s%(coloff)s %(asctime)s\n%(traceback)s\n #@ %(filepathname)s:%(lineno)d\n%(message)s')


handler.setFormatter(normalFormatter)
l.addHandler(handler)

l.setLevel(logging.INFO)

def exitError(message):
    l.fatal(message)
    sys.exit(-1)

def setVerbose():
    handler.setFormatter(debugFormatter)
    l.setLevel(logging.DEBUG)

def setSilent():
    handler.setFormatter(normalFormatter)
    l.setLevel(logging.CRITICAL)

def setInfo():
    handler.setFormatter(normalFormatter)
    l.setLevel(logging.INFO)
