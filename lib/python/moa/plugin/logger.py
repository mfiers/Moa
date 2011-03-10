"""
**logger** - Log Moa activity



"""

import os
import re
import sys
from datetime import datetime

import moa.job
import moa.logger as l
import moa.plugin

def defineCommands(data):
    data['commands']['log'] = { 
        'desc' : 'Show the logs for this job',
        'call' : showLog
        }

def prepare(data):
    data.logger.start_time = datetime.today()


def finish(data):

    data.logger.end_time = datetime.today()
    data.logger.run_time = data.logger.end_time - data.logger.start_time
    runtime = data.logger.end_time - data.logger.start_time
    logFile = os.path.join(data.job.confDir, 'log')
    
    with open(logFile, 'a') as F:
        F.write("%s\n" % "\t".join([
            ",".join(data.executeCommand),
            data.logger.start_time.strftime("%Y-%m-%dT%H:%M:%S:%f"),
            data.logger.end_time.strftime("%Y-%m-%dT%H:%M:%S:%f"),
            str(runtime)
            ]))
        
def showLog(data):
    logFile = os.path.join(data.job.confDir, 'log')
    with open(logFile) as F:
        for line in F:
            print line
