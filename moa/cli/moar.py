#!/usr/bin/env python

import os
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(description='run recursively')
parser.add_argument('--bg', dest='background', action='store_true',
                    default=False,
                    help='run each job in the background')
parser.add_argument('-d', dest='depth', default=0, type=int,
                    help='depth: 1 means run only in first ' +
                    'level subdirs, 2 only in second level, and so on')
parser.add_argument('-t', dest='test', default=False,
                    help='test run', action='store_true')
parser.add_argument('command', nargs='+')
args = parser.parse_args()


def moar():
    cl = " ".join(args.command).strip()
    if args.background and cl[-1] != '&':
        cl = '( ' + cl + ' )& '

    print 'executing:', cl

    base = os.path.abspath(os.getcwd())

    if base[-1] == '/':
        base = base[:-1]

    for path, dirs, files in os.walk(base):
        toRemove = [x for x in dirs if x[0] in ['.', '_']]
        [dirs.remove(x) for x in toRemove]
        localpath = path.replace(base, '')
        level = len(localpath.split('/')) - 1

        dirs.sort()

        if args.depth and args.depth != level:
            continue

        if args.test:
            print 'would executed in', localpath
            print '   ', cl
        else:
            print 'executing in %s' % localpath
            P = sp.Popen(cl, cwd=path, shell=True)
            P.wait()

if __name__ == '__main__':
    moar()
