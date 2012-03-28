# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**remoteLogger** - Remotely log Moa activity
--------------------------------------------

requires the standard moa logger to be active
"""

import os
import sys
import MySQLdb
import socket
import getpass

from datetime import datetime

import moa.job
import moa.utils
import moa.logger as l
from moa.sysConf import sysConf

SQL = """
INSERT INTO log (status, start, stop, level, command, full_command, wd, server, template, user, title)
VALUES (%(status)s, %(start)s, %(stop)s, %(level)s, 
        %(command)s, %(full_command)s, %(wd)s, %(server)s,
        %(template)s, %(user)s, %(title)s
        )
"""

def hook_logMessage():
    """
    Restore the log message -  this time in a remote mysql database
    """
    db=MySQLdb.connect(host = sysConf.plugins.remoteLogger.host, 
                       user = sysConf.plugins.remoteLogger.user, 
                       passwd = sysConf.plugins.remoteLogger.passwd, 
                       db = sysConf.plugins.remoteLogger.db)
    c = db.cursor()
    template = sysConf.job.template.get('name', "")
    title = sysConf.job.conf.getRendered('title')

    d = { 'status' : sysConf.logger.status ,
          'level' :  sysConf.logger.logLevel,
          'command' :  sysConf.logger.moa_command,
          'full_command' :  sysConf.logger.full_command,
          'start' : sysConf.logger.start_time.strftime("%Y-%m-%d %H:%M:%S"),
          'stop' : sysConf.logger.end_time.strftime("%Y-%m-%d %H:%M:%S"),
          'wd' : os.path.abspath(sysConf.job.wd),
          'server' : socket.gethostname(),
          'template' : template,
          'user' : getpass.getuser(),
          'title' : title
          }

    #l.critical('sql %s' % (SQL % d))
    c.execute(SQL, d)
    db.commit()
    l.debug("wrote log to remote server (%d)" % c.rowcount)
