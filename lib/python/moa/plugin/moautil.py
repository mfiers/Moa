# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**moautil** - Some extra utilities - copy/move jobs
---------------------------------------------------
"""

import os
import re
import sys
import glob
import shutil

import moa.logger as l
import moa.ui
from moa.sysConf import sysConf

def defineCommands(data):
    data['commands']['cp'] = {
        'desc' : 'Copy a moa job',
        'call' : moacp,
        'needsJob' : False,
        'recursive' : 'local',
        'unittest' : COPYTEST}

#    data['commands']['mv'] = {
#        'desc' : 'Move a moa job, ',
#        'call' : moamv }
#        


def moamv(data):
    
    args = data['newargs']

    fr = args[0]
    if fr[-1] == '/':
        fr = fr[:-1]
        
    if len(args) > 1: to = args[1]
    else: to = '.'

    #see if fr is a number
    if re.match('\d+', fr):
        newfr = glob.glob('%s*' % fr)
        if len(newfr) != 1:
            l.critical("Cannot resolve %s (%s)" % (fr, newfr))
            sys.exit(1)
        fr = newfr[0]
        
    if re.match('\d+', to):
        if re.search('^\d+', fr):
            to = re.sub('^\d+', to, fr)
        else:
            to = '%s.%s' % (to, fr)
    shutil.move(fr, to)
            
    
def moacp(job):
    """
    Copy a moa job, or a tree with jobs.

    moa cp copies only those files defining a job: the template files
    and the job configuration. Additionaly, all files in the moa
    directory that start with `moa.` (for example `moa.description`
    are copied as well. Data and log files are not copied!

    The command has two modes of operation. The first is::

        moa cp 10.from 20.to

    copies the moa job in 10.from to a newly created 20.to
    directory. If the `20.to` directory already exists, a new
    directory is created in `20.to/10.from`. As an shortcut one can
    use::

        moa cp 10.from 20

    in which case the job will be copied to the `20.from` directory.

    If the source (`10.from`) directory is not a Moa job, the command
    exits with an error.

    The second mode of operation is recursive copying::

       moa cp -r 10.from 20.to

    in which case all subdirectories under 10.from are traversed and
    copied - if a directory contains a Moa job. 

    ::TODO..  Warn for changing file & dir links
    """
    
    options = sysConf.options
    args = sysConf.newargs
    
    if len(args) > 1: dirTo = args[1]
    else: dirTo = '.'

    dirFrom = args[0]
    if dirFrom[-1] == '/': dirFrom = dirFrom[:-1]
    fromBase = os.path.basename(dirFrom)

    if dirTo[-1] == '/': dirTo = dirTo[:-1]
    toBase = os.path.basename(dirTo)

    # trick - the second argument is a number
    # renumber the target directory
    if re.match("^[0-9]+$", toBase):
        toBase = re.sub("^[0-9]*\.", toBase + '.', fromBase)
        dirTo = os.path.join(os.path.dirname(dirTo), toBase)
        
    elif os.path.exists(dirTo):
        #if the 'to' directory exists - create a new sub directory 
        dirTo = os.path.join(dirTo, fromBase)     
    
    l.info("Copying from %s to %s" % (dirFrom, dirTo))

    if  not options.recursive:
        if not os.path.isdir(dirFrom):
            moa.ui.exitError(
                "Need %s to be a directory" % dirFrom)
        fromJob = moa.job.Job(dirFrom)
        if not fromJob.isMoa():
            moa.ui.exitError(
                "Need %s to be a moa directory" % dirFrom)
        _copyMoaDir(fromJob, dirTo)
    else:
        #recursive: start traversing through dirFrom
        for path, dirs, files in os.walk(dirFrom):
            if '.moa' in dirs:
                fromJob = moa.job.Job(path)
                dirs.remove('.moa')
                thisToPath = path.replace(dirFrom, dirTo)
                _copyMoaDir(fromJob, thisToPath)

                            
def _copyMoaDir(job, toDir):
    for pattern in job.data.moaFiles:
        for fromFile in  glob.glob(os.path.join(job.wd, pattern)):
            toFile = fromFile.replace(job.wd, toDir)
            if os.path.exists(fromFile) and not os.path.isfile(fromFile):
                l.critical("Uncertain about copying %s" % fromFile)
                sys.exit()
            if os.path.exists(fromFile):
                thisToDir = os.path.dirname(toFile)
                if not os.path.exists(thisToDir):
                    os.makedirs(thisToDir)
                shutil.copyfile(fromFile, toFile)

#Unittest scripts

COPYTEST = '''
mkdir 10.test
cd 10.test
moa simple -t "test" -- echo "hello"
cd ..
moa cp 10.test 20 2>/dev/null
cd 20.test
output=`moa run`
[[ "$output" =~ "hello" ]] || (echo "invalid output"; false)
cd ..
moa cp 10.test 30.test2 2>/dev/null
cd 30.test2
output=`moa run`
[[ "$output" =~ "hello" ]] || (echo "invalid output"; false)
cd ../10.test
mkdir 05.subtest
cd 05.subtest
moa simple -t "test2" -- echo "subtest"
cd ../../
moa cp 10.test 40.test 2>/dev/null
[[ ! -d "40.test/05.subtest" ]] || (echo "subdirectory should not be there"; false)
moa cp -r 10.test 50.test 2>/dev/null
[[ -d "50.test/05.subtest" ]] || (echo "subdirectory is not there?"; false)
'''
