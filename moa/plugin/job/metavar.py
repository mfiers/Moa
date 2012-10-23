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

Another feature that metavar does it try to parse out variables from
the directory name. So if a directory name is:
./test__qual_13__cutoff_0.12

Note that
* variables are delimited by a double underscore
* Key/values are separate by a single underscore
* the item before the first __ is not interpreted
* items without a '_' are ignored

Then this plugin will filter set the variable qual to 13 and cutoff to 0.12.

"""
import os
import re

import moa.logger

l = moa.logger.getLogger(__name__)


def _varparser(conf, name):
    """
    Filter out variables from the variable name
    """
    l.debug('parsing parameters from directory name %s', name)
    for item in name.split('__')[1:]:
        if not '_' in item:
            continue
        k, v = item.split('_', 1)
        l.debug('setting %s to %s' % (k, v))
        conf[k] = v


def hook_pre_filesets(job):

    wd = job.wd
    awd = os.path.abspath(wd)

    job.conf.setPrivateVar('wd', awd)

    dirparts = awd.split(os.path.sep)
    job.conf.setPrivateVar('_', dirparts[-1])
    i = 1

    while dirparts:
        cp = os.path.sep.join(dirparts)
        p = dirparts.pop()
        if i == 1:
            #top level - parse parameters from the dirname
            _varparser(job.conf, p)

        clean_p = re.sub("^[0-9]+\.+", "", p).replace('.', '_')

        if not p:
            break

        if i <= 3:
            job.conf.setPrivateVar('_' * i, p)

        i += 1
