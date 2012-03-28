# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**twit** - Tweet results
------------------------

Use twitter to send a message upon job completion
"""

import os
import sys
import time
import smtplib
import jinja2
from email.mime.text import MIMEText

import Yaco

import moa.logger as l
from moa.sysConf import sysConf
import moa.plugin.logger

def hook_postError():
    postRun(data)
def hook_postInterrupt():
    postRun(data)

MESSAGE = """
Your job, named '{{ job.conf.title }}' has finished with state '{{ job.status }}'

location : {{ job.absPath }}
start    : {{ logger.start_time }}
stop     : {{ logger.end_time }}
run time : {{ logger.run_time }} ({{logger.niceRunTime}})

Parameters:
===========

{% for param in job.conf.keys() %}
{{- "%20s : "|format(param) -}}
{{ job.conf[param] }}
{% endfor %}

"""

def postRun(job):
    """
    Send a mail out upon completion of this job
    """
    l.info('sending mail')
    server = sysConf.plugins.mail.server

    frm = sysConf.plugins.mail['from']
    tom = sysConf.plugins.mail['to']
    
    job = sysConf.job
    data = Yaco.Yaco()

    sysConf.job.absPath = os.path.abspath(sysConf.job.wd)

    status = sysConf.job.get('status', 'unknown')
    subject = "Moa job '%s' finished (%s) in '%s'" % (
        sysConf.job.conf.title, status,
        sysConf.job.absPath)



    template = jinja2.Template(MESSAGE)
    message = template.render(sysConf)

    smtp = smtplib.SMTP(server)
    smtp.helo()

    msg = MIMEText(message)

    msg['Subject'] = 'Moa job finished in %s (%s)' % (
        os.path.basename(sysConf.job.wd),
        sysConf.job.status)
    msg['From'] = frm
    msg['To'] = tom

    smtp.sendmail(frm, [tom], msg.as_string())

