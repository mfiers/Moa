# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 

"""
Moa utilities
"""

import os
import re
import sys
import shutil
import optparse
import moa.logger as l
import moa.info

def defineCommands(data):
    data['commands']['cp'] = {
        'desc' : 'Copy a moa job (only the configuration, not the data), '+
        'use moa cp DIR_FROM DIR_TO',
        'call' : moacp }
        
    data['commands']['kill'] = {
        'desc' : 'Kill a running moa job',
        'call' : moakill }

    data['commands']['pause'] = {
        'desc' : 'Pause a running moa job',
        'call' : moapause }

    data['commands']['resume'] = {
        'desc' : 'Resume a paused moa job',
        'call' : moaresume }

    data['commands']['tree'] = {
        'desc' : 'return a tree structure with extra moa information',
        'call' : moaTree }


def moaTree(data):
    """
    Print a tree with Moa info
    """
    cwd = data['cwd']
    for root, dirs, files in os.walk(cwd):
        state = moa.info.status(root)
        print "%-10s %s" % (state, os.path.relpath(root, cwd))

def moakill(data):
    """
    kill a running job
    """
    cwd = data['cwd']

    if not moa.info.status(cwd) == 'running': 
        l.warning("Moa does not seem to be running!")
        sys.exit(-1)

    pid = int(open(os.path.join(cwd, 'moa.runlock')).read())
    l.critical("killing job %d" % pid)
    os.kill(pid, 9)

def moapause(data):
    """
    pause a running job
    """
    cwd = data['cwd']

    if not moa.info.status(cwd) == 'running': 
        l.warning("Moa process does not seem to be active!")
        sys.exit(-1)

    pid = int(open(os.path.join(cwd, 'moa.runlock')).read())
    l.warning("Pausing job %d" % pid)
    os.kill(pid, 19)

def moaresume(data):
    """
    resume a paused job - 

    """
    cwd = data['cwd']
    if not moa.info.status(cwd) == 'paused': 
        l.warning("Moa process does not seem to be paused!")
        sys.exit(-1)

    pid = int(open(os.path.join(cwd, 'moa.runlock')).read())
    l.warning("Resming job %d" % pid)
    os.kill(pid, 18)

        
def moacp(data):
    """
    Copy a moa job - 
      0 create a new directory
      1 copy the configuration

    TODO: adapt file & dir links
    """
    wd = data['cwd']
    options = data['options']
    args = data['newargs']

    if len(args) > 1: dirto = args[1]
    else: dirto = '.'

    dirfrom = args[0]

    #remove trailing slash & determine basename
    if dirfrom[-1] == '/': dirfrom = dirfrom[:-1]
    fromBase = os.path.basename(dirfrom)

    # trick - the second argument is a number
    # renumber the target directory
    if re.match("^[0-9]+$", dirto):
        dirto = re.sub("^[0-9]*\.", dirto + '.', fromBase)
    
    if not os.path.exists(dirto):
        l.info("creating directory %s" % dirto)
        os.makedirs(dirto)
    else:
        dirto = os.path.join(dirto, fromBase)
        os.makedirs(dirto)

        
    l.info("Copying from %s to %s" % (dirfrom, dirto))

    for f in ['Makefile', 'moa.mk']:
        cfr = os.path.join(dirfrom, f)
        cto = os.path.join(dirto, f)

        l.info("copy %s to %s" % (cfr, cto))

        shutil.copyfile(cfr, cto)
