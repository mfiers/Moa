#!/usr/bin/env python
"""Returns the path to the bash environment initializiation
script. Should be called as:

. $(moainit)

Note - this works for Bash.
"""

import pkg_resources


def moainit():

    #get the moa.sh script
    moash = pkg_resources.resource_filename(
        'moa', 'data/etc/profile.d/moa.sh')
    print '%s' % (moash)


if __name__ == '__main__':
    moainit()
