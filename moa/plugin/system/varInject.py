# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**varInject** - Inject variables into this job
----------------------------------------------

"""
import os
import sys
import subprocess as sp

from moa.sysConf import sysConf
import moa.logger as l
import moa.ui

def hook_prepare_3():
    job = sysConf.job
    job.template.parameters.var_inject = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'The output of this command is parsed and injected into the config',
        'recursive' : False,
        'type' : 'string'


        }
    
    renderedConf = job.conf.render() 
    injectcommand = renderedConf.get('var_inject', '')
    
    if not injectcommand:
        return
    
    P = sp.Popen(injectcommand, shell=True, stdout=sp.PIPE)
    out, err = P.communicate()
    if err or P.returncode != 0:
        moa.ui.exitError("var_inject returned an error")
    for line in out.split("\n"):
        ls = line.strip().split(None, 1)
        if not ls: continue        
        if len(ls) != 2:
            moa.ui.exitError("var_inject invalid return: %s" % line)
        k,v = ls
        job.conf[k] = v

