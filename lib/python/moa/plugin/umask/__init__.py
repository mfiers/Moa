# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 

"""
**umaks** - Sets umaks for the moa process
--------------------------------------------
"""
import os

from moa.sysConf import sysConf

def hook_prepare_1():
    mask = int(sysConf.plugins.umask.get('umask', '0o777'), 8)
    os.umask(mask)

    
