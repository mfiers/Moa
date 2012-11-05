#!/usr/bin/env python

import os
import pkg_resources
import subprocess as sp


def moainit():

    #get the moa.sh script
    moash = pkg_resources.resource_filename(
        'moa', 'data/etc/profile.d/moa.sh')
    print moash

if __name__ == '__main__':
    moainit()
