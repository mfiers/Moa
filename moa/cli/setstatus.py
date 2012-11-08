#!/usr/bin/env python

import os
import sys
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(description='set moa status, needs to ' + 
                                 'be executed in a moa job directory')

parser.add_argument('status', help='status to set')
args = parser.parse_args()


def setstatus():

    if not os.path.exists('.moa') and os.path.isdir('.moa'):
        sys.stderr.write("must be executed in a moa job directory\n")
        sys.exit(-1)

    statusFile = os.path.join('.moa', 'status')
    pidFile = os.path.join('.moa', 'pid')

    status = args.status.lower()

    if not status in 'waiting running success error interrupted'.split():
        sys.stderr.write('invalid status: %s\n' % status)
        sys.exit(-1)

    if status != 'run':
        if os.path.exists(pidFile):
            os.unlink(pidFile)

    with open(statusFile, 'w') as F:
        F.write(status)


if __name__ == '__main__':
    setstatus()
