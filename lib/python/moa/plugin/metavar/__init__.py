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

`_`
    name of the current directory. In the example, `_`
    renders to `test`
    
`__`
    name of the parent directory - (example: `a`)

`___`
    name of the parent directory - (example: `is`)

`dir1`
    same as `_`
    
`dir2`
    same as `__`
    
`dir3`
    same as `___`
    
`dir4`
    parent directory of dir3

Also a number of contextual variables are defined. In the same
example as above, based on the directory name, the following variables
are defined:

* `_tmp`: `/tmp`
* `_this`: `/tmp/this`
* `_is`: `/tmp/this/is`
* `_a`: `/tmp/this/is/a`
* `_test`: `/tmp/this/is/a/test`

Note that numerical prefixes are stripped from directoy names. So, for
example: `/tmp/this/10.is/444.a/test` would result in the same
variables names as mentioned above (but with different directories).

Additional contextual variables are, based on the following example
directory structure (with cwd being `/tmp/test/20.dirc/20.subb/`::

    /tmp/test/00.dira/
    /tmp/test/10.dirb/
    /tmp/test/20.dirc/
    /tmp/test/20.dirc/10.suba/
    /tmp/test/20.dirc/20.subb/
    /tmp/test/20.dirc/30.subc/
    /tmp/test/20.dirc/40.subd/
    /tmp/test/30.dird/

`_first`: `/tmp/test/20.dirc/10.suba`
`_prev`: `/tmp/test/20.dirc/10.suba`
`_next`: `/tmp/test/20.dirc/30.subc`
`_last`: `/tmp/test/20.dirc/40.subd`

`__first`: `/tmp/test/00.dira`
`__prev`: `/tmp/test/10.dirb`
`__next`: `/tmp/test/30.dird`
`__last`: `/tmp/test/30.dird`

Equivalently, `___first`, `___prev`, `___next` and `___last` are also
defined.

Note that all directory orders are based on an alphanumerical sort of
directory names. `9.dir` comes after `10.dir`. (so use `09.dir`).

The latter definitions override the earlier ones.
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
    lastp = None

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

        if i > 1 and  i <= 3:
            thisdirlist = os.listdir(cp)
            thisdirlist.sort()
            
            iofp = thisdirlist.index(lastp)

            job.conf.setPrivateVar(('_' * (i-1)) + 'first',
                                   os.path.join(cp, thisdirlist[0]))
            job.conf.setPrivateVar(('_' * (i-1)) + 'last',
                                   os.path.join(cp, thisdirlist[-1]))

            if iofp > 0:
                job.conf.setPrivateVar(('_' * (i-1)) + 'prev',
                                       os.path.join(cp, thisdirlist[iofp-1]))

            if iofp < (len(thisdirlist)-1):
                job.conf.setPrivateVar(('_' * (i-1)) + 'next',
                                       os.path.join(cp, thisdirlist[iofp+1]))


        lastp = p
        i += 1

    
