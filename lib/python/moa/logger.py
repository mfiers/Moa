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
import sys
import logging

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
            record.vis1 = "D"
        elif record.levelno <= logging.INFO:
            record.colon = chr(27) + "[30m" + chr(27) + "[42m"
            record.visual = "#INFO "
            record.vis1 = "I"
        elif record.levelno <= logging.WARNING:
            record.visual = "#WARN "
            record.colon = chr(27) + "[30m" + chr(27) + "[46m"
            record.vis1 = "W"
        elif record.levelno <= logging.ERROR:
            record.visual = "#ERRR "
            record.vis1 = "E"
            record.colon = chr(27) + "[30m" + chr(27) + "[43m"
        else:
            record.colon = chr(27) + "[30m" + chr(27) + "[41m"
            record.visual = "#CRIT "
            record.vis1 = "C"


        record.msg = " ".join(record.msg.split())
        #check if we're on a tty, if not, reset colon/coloff
        if not sys.stdout.isatty():
            record.colon = ""
            record.coloff = ""
            
        return logging.Formatter.format(self, record)


l = logging.getLogger('moa')
handler = logging.StreamHandler()
logmark = chr(27) + '[0;44mU' + \
          chr(27) + '[0m ' 


formatter = XTRFormatter('%(colon)s%(vis1)s%(coloff)s %(message)s')

handler.setFormatter(formatter)
l.addHandler(handler)

l.setLevel(logging.INFO)

def exitError(message):
    l.fatal(message)
    sys.exit(-1)

def setVerbose():
    l.setLevel(logging.DEBUG)

def setSilent():
    l.setLevel(logging.WARNING)

def setInfo():
    l.setLevel(logging.INFO)
