# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**metavar** - Create a number of meta variables
-----------------------------------------------

Set a number of meta variables to be used in job
configuration. Variable that are currently created are:

(Assuming we're in the directory: `/tmp/this/is/a/test`)

_
    name of the current directory. In the example, `_`
    renders to `test`
    
__
    name of the parent directory - (example: `a`)

___
    name of the parent directory - (example: `is`)

dir1
    same as _
    
dir2
    same as __
    
dir3
    same as ___
    
dir4
    parent directory of dir3

Als - a number of contextual variables are defined. In the same
example as above, based on the directory name, the following variables
are defined:

_tmp: /tmp
_this: /tmp/this
_is: /tmp/this/is
_a: /tmp/this/is/a
_test: /tmp/this/is/a/test
     
    

"""
import re
import os
import sys
import subprocess as sp

from moa.sysConf import sysConf
import moa.logger as l
import moa.ui

def hook_prepare_3():
    job = sysConf.job
    renderedConf = job.conf.render() 

    job.conf.setPrivateVar('wd', job.wd)

    dirparts = job.wd.split(os.path.sep)
    job.conf.setPrivateVar('_', dirparts[-1])
    i = 1                
    while dirparts:
        cp = os.path.sep.join(dirparts)
        p = dirparts.pop()
        clean_p = re.sub("^[0-9]+\.+", "", p).replace('.', '_')

        #print i, clean_p, p, cp
        if not p: break
        job.conf.setPrivateVar('dir%d' % i, p)
        job.conf.setPrivateVar('_%d' % i, p)
        job.conf.setPrivateVar('_%s' % clean_p, cp)

        if i <= 3:
            job.conf.setPrivateVar('_' * i, p)

        i += 1
 
