# 
# Copyright 2009 Mark Fiers, Plant & Food Research
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

"""
**logo** - Print the moa logo
-----------------------------
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

    #adjust the logo for term width
    TERMHEIGHT, TERMWIDTH = map(int, os.popen('stty size', 'r').read().split())
    MOABASE = moa.utils.getMoaBase()
    version = data['sysConf'].getVersion()
    logoFile = os.path.join(MOABASE, 'share', 'logo', 'moa.logo.txt')
    logo = open(logoFile).read()
    logo = logo.replace('###', 't' * (TERMWIDTH - 64))
    logo = logo.replace('##', 't' * (TERMWIDTH - 58 - len(version)))
    logo = logo.replace('VERSION', version)
    print logo    
