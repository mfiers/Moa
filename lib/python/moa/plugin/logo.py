# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**logo** - Print a big, in your face, moa logo
----------------------------------------------
"""
import os

import moa.utils    

order = 10

def preRun(data):
    """
    Print the logo just before a moa run
    """
    
    job = data['job']
    #don't print a logo during a no-job run
    if job.template.name == 'nojob':
        return
    if 'MOA_NOLOGO' in os.environ.keys():
        return
    #adjust the logo for term width
    TERMHEIGHT, TERMWIDTH = map(int, os.popen('stty size', 'r').read().split())
    MOABASE = moa.utils.getMoaBase()
    version = data['sysConf'].getVersion()
    logoFile = os.path.join(MOABASE, 'share', 'logo', 'moa.logo.txt')
    logo = open(logoFile).read()
    logo = logo.replace('###', 't' * (TERMWIDTH - 64))
    logo = logo.replace('##', 't' * (TERMWIDTH - 59 - len(version)))
    logo = logo.replace('VERSION', version)
    print logo    
