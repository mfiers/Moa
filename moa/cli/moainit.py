#!/usr/bin/env python
"""Return the path to the moa environment initializiation
script. Should be called as:

. `moainit`

"""

import pkg_resources


def moainit():

    #get the moa.sh script
    moash = pkg_resources.resource_filename(
        'moa', 'data/etc/profile.d/moa.sh')
    print moash


if __name__ == '__main__':
    moainit()
