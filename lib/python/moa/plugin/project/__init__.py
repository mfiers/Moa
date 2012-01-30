# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**project** - Simple plugin to ease maintaining project data
------------------------------------------------------------

Have more plans for this plugin - but for now it defines the following
two variables to use in the job configuration

* _p : directory of the parent project
* project: the 'title' varialbe of the first parent project

"""
import re
import os
import sys
import Yaco
import subprocess as sp

from moa.sysConf import sysConf
import moa.logger as l
import moa.ui

def hook_prepare_3():

    #see if we can find a project directory - 
    job = sysConf.job
    lookat = os.path.abspath(sysConf.job.wd)
    while True:
        
        if lookat == '/': break
        
        templateFile = os.path.join(lookat, '.moa', 'template')
        if not os.path.exists(templateFile):
            lookat = os.path.dirname(lookat)
            continue
        
        td = Yaco.Yaco()
        td.load(templateFile)

        if td.moa_id != 'project':
            lookat = os.path.dirname(lookat)
            continue

        #found project!
        job.conf.setPrivateVar('__project', lookat)
        job.conf.setPrivateVar(
            '_project',
            re.sub("^[0-9]+\.+", "", os.path.basename(lookat)))
        
        #get this wd's job conf
        projectConf = os.path.join(lookat, '.moa', 'config')
        if os.path.exists(projectConf):
            pc = Yaco.Yaco()
            pc.load(projectConf)
            if pc.title:
                job.conf['project'] = pc.title
        break
