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

* `__tmp`: `/tmp`
* `__this`: `/tmp/this`
* `__is`: `/tmp/this/is`
* `__a`: `/tmp/this/is/a`
* `__test`: `/tmp/this/is/a/test`

Note that numerical prefixes are stripped from directoy names. So, for
example: `/tmp/this/10.is/444.a/test` would result in the same
variables names as mentioned above (but with different
directories). Also, [^A-Za-z0-9_] in variable names are converted to
underscores to become valid python variable names.

(for backwards compatibility - _tmp versions are also defined with the
same value)

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

`_f`: `10.suba`
`_p`: `10.suba`
`_n`: `30.subc`
`_l`: `40.subd`

`__f`: `/tmp/test/20.dirc/10.suba`
`__p`: `/tmp/test/20.dirc/10.suba`
`__n`: `/tmp/test/20.dirc/30.subc`
`__l`: `/tmp/test/20.dirc/40.subd`

`_ff`: `00.dira`
`_pp`: `10.dirb`
`_nn`: `30.dird`
`_ll`: `30.dird`

`__ff`: `/tmp/test/00.dira`
`__pp`: `/tmp/test/10.dirb`
`__nn`: `/tmp/test/30.dird`
`__ll`: `/tmp/test/30.dird`


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

import frappant

import jinja2
from jinja2.ext import Extension
from jinja2 import nodes

from moa.sysConf import sysConf
import moa.logger as l
import moa.ui

class MoaPathParser(Extension):
    tags = set(['mp'])

    def processDirString(self, s):
        cwd = os.getcwd()
        return frappant.frp(cwd, s)
        # l.critical(cwd)

        # l.critical("parsing %s" % s)
        # sp = s.split(os.path.sep)
        # return '_'.join(sp)
        
    def parse(self, parser):
        node = nodes.Scope(lineno=next(parser.stream).lineno)
        lineno = parser.stream.current.lineno
        #get first argument
        expr = parser.parse_expression()
        
        while parser.stream.current.type != 'block_end':
            #flush superfluous arguments
            parser.stream.expect('comma')
            parser.parse_expression()

        #process the string!
        return nodes.Const(self.processDirString(expr.value))


def hook_prepare_1():

    if not sysConf.jinja2.extensions:
        sysConf.jinja2.extensions = []
    print sysConf.jinja2.pretty()
    sysConf.jinja2.extensions += [MoaPathParser]

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
        #job.conf.setPrivateVar('dir%d' % i, p)
        job.conf.setPrivateVar('_%d' % i, p)
        job.conf.setPrivateVar('_%s' % clean_p, cp)
        job.conf.setPrivateVar('__%s' % clean_p, cp)

        if i <= 3:
            job.conf.setPrivateVar('_' * i, p)

        if i > 1 and  i <= 3:
            thisdirlist = [x for x in os.listdir(cp) if not x[0] == '.']
            thisdirlist.sort()
            
            iofp = thisdirlist.index(lastp)

            job.conf.setPrivateVar('_' + ('f' * (i-1)), thisdirlist[0])
            job.conf.setPrivateVar('__' + ('f' * (i-1)),
                                   os.path.join(cp, thisdirlist[0]))
            
            job.conf.setPrivateVar('_' +('l' * (i-1)), thisdirlist[-1])
            job.conf.setPrivateVar('__' +('l' * (i-1)),
                                   os.path.join(cp, thisdirlist[-1]))

            if iofp > 0:
                job.conf.setPrivateVar('_' +('p' * (i-1)), thisdirlist[iofp-1])
                job.conf.setPrivateVar('__' +('p' * (i-1)),
                                       os.path.join(cp, thisdirlist[iofp-1]))


            if iofp < (len(thisdirlist)-1):
                job.conf.setPrivateVar('_' +('n' * (i-1)), thisdirlist[iofp+1])
                job.conf.setPrivateVar('__' +('n' * (i-1)),
                                       os.path.join(cp, thisdirlist[iofp+1]))


        lastp = p
        i += 1

    
