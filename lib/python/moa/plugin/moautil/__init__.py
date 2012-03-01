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
import tarfile
import optparse

import moa.logger as l
import moa.ui
from moa.sysConf import sysConf

def hook_defineCommands():
    sysConf['commands']['cp'] = {
        'desc' : 'Copy a moa job',
        'call' : moacp,
        'needsJob' : False,
        'recursive' : 'local',
        'unittest' : COPYTEST}

    sysConf['commands']['mv'] = {
        'desc' : 'Rename/renumber/move a job',
        'call' : moamv,
        'needsJob' : False,
        'recursive' : 'none',
        'unittest' : RENTEST}

    sysConf['commands']['archive'] = {
        'desc' : 'Archive a job, ',
        'needsJob' : True,
        'recursive' : 'local',
        'call' : archive }

    sysConf['commands']['archive_exclude'] = {
        'desc' : 'marks a directory to not be archived',
        'needsJob' : False,
        'call' : archive_exclude }
    
    sysConf['commands']['archive_include'] = {
        'desc' : 'marks a directory to be archived',
        'needsJob' : False,
        'call' : archive_include }



def hook_defineOptions():
    parserG = optparse.OptionGroup(sysConf.parser, 'moa archive')
    parserG.add_option("--template", dest="archive_template",
                              action='store_true', default=False,
                              help='store this archive as a template')
    sysConf.parser.add_option_group(parserG)

def archive_include(job):
    """
    Toggle a directory to be included in an moa archive.
    
    """
    moa.ui.message("%s {{green}}will{{reset}} be included in an archive" % job.wd)


    moaConfDir = os.path.join(job.wd, '.moa')
    if not os.path.exists(moaConfDir):
        return #default is to include
    moaNoArchiveFile = os.path.join(moaConfDir, 'noarchive')
    if os.path.exists(moaNoArchiveFile):
        os.unlink(moaNoArchiveFile)

def archive_exclude(job):
    """
    Toggle a directory to be included in an moa archive.
    
    """
    moa.ui.message("%s will {{bold}}NOT{{reset}} be included in an archive" % job.wd)
    moaConfDir = os.path.join(job.wd, '.moa')
    if not os.path.exists(moaConfDir):
        os.makedirs(moaConfDir)
    moaNoArchiveFile = os.path.join(moaConfDir, 'noarchive')
    if not os.path.exists(moaNoArchiveFile):
        with open(moaNoArchiveFile, 'w') as F:
            F.write("")



def archive(job):
    """
    Archive a job, or tree with jobs for later execution.
    
    This command stores only those files that are necessary for
    execution of this job, that is: templates & configuration. In &
    output files, and any other file are ignored. An exception to this
    are all files that start with 'moa.'

    Usage::

        moa archive

    or::

        moa archive [NAME]

    an archive name can be omitted when the command is issued in a
    directory with a moa job, in which case the name is derived from
    the `jobid` parameter

    It is possible to run this command recursively with the `-r`
    parameter - in which case all (moa job containing) subdirectories
    are included in the archive.

    As an alternative application you can specify the
    `--template`. 
    
    """

    if len(sysConf.newargs) > 0:
        archiveName = sysConf.newargs[0]
    else:
        archiveName = job.conf.get('jobid', None)
        if archiveName == None:
            moa.ui.exitError('When not in a moa job, you must define an archive name')

    if sysConf.options.archive_template:    
        if ('/' in archiveName):
            moa.ui.exitError("You can not specify a path when using --template")
            
        archivePath = os.path.abspath(os.path.expanduser(
            sysConf.plugins.moautil.get('dir', '~/.config/moa/archive')))
        if not os.path.exists(archivePath):
            os.makedirs(archivePath)
    else:
        if ('/' in archiveName):
            archivePath, archiveName = os.path.split(archiveName)
        else:
            archivePath = '.'
            
    if archiveName[-2:] == 'gz':
        moa.ui.exitError("Do not specify an extension for the archive")

    archiveName += '.tar.gz'
    archiveFile = os.path.join(archivePath, archiveName)

    if os.path.exists(archiveFile):
        if not sysConf.options.force:
            moa.ui.exitError("%s exists - use -f to overwrite" %
                             archiveFile)

    if not sysConf.options.recursive and not sysConf.job.isMoa():
        moa.ui.exitError('Nothing to archive')
        
    l.info("archiving %s" % archiveFile)
    
    TF = tarfile.open(
        name = archiveFile,
        mode = 'w:gz')

    def _addFiles(tf, path, job):
        for pattern in job.data.moaFiles:
            for fl in glob.glob(os.path.join(path, pattern)):
                if fl[-1] == '~': continue
                tf.add(fl)
                
    if sysConf.options.recursive:
        for path, dirs, files in os.walk('.'):
            if os.path.exists(os.path.join(path, '.moa', 'noarchive')):
                continue
            sjob = moa.job.Job(path)
            _addFiles(TF, path, sjob) 
            toRemove = [x for x in dirs if x[0] == '.']
            [dirs.remove(x) for x in toRemove]
    else:
        _addFiles(TF, '.', job)

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

    #remember the files copied
    sysConf.moautil.filesCopied = []
    
    if len(args) > 1: dirTo = args[1]
    else: dirTo = '.'

    dirFrom = args[0]
    if dirFrom[-1] == '/': dirFrom = dirFrom[:-1]
    fromBase = os.path.basename(dirFrom)

    if dirTo[-1] == '/': dirTo = dirTo[:-1]
    toBase = os.path.basename(dirTo)

    #print fromBase, toBase
    # trick - the second argument is a number
    # renumber the target directory
    if re.match("^[0-9]+$", toBase) and re.match("^[0-9]+\..+$", toBase):
        print toBase, fromBase
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
    #l.info("Copying from %s to %s" % (job.wd, toDir))
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
            sysConf.moautil.filesCopied.append(toFile)

def hook_git_finish_cp():
    files = sysConf.moautil.get('filesCopied', [])
    repo = sysConf.git.getRepo(sysConf.job)
    repo.index.add(map(os.path.abspath, files))
    repo.index.commit("moa cp %s" % " ".join(sysConf.newargs))
    
def moamv(job):
    """
    Renumber or rename a moa job..
    """

    #remember the files moved
    sysConf.moautil.filesMoved = []

    args = sysConf.newargs

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
        
    if re.match('^\d+$', to):
        if re.search('^\d+', fr):
            to = re.sub('^\d+', to, fr)
        else:
            to = '%s.%s' % (to, fr)
            
    moa.ui.message("Moving %s to %s" % (fr, to))
    if sysConf.git.active and sysConf.git.repo:
        l.debug('git is active - deferring move to later')        
        sysConf.moautil.mv.fr = fr
        sysConf.moautil.mv.to = to
    else:
        shutil.move(fr, to)
        
def hook_git_finish_mv():
    #make sure the 'from' directory is under git control
    sysConf.git.commitDir(sysConf.moautil.mv.fr, 'Preparing for git mv')
    #seems that we need to call git directly gitpython does not work
    os.system('git mv %s %s' % (sysConf.moautil.mv.fr, sysConf.moautil.mv.to))
    os.system('git commit %s %s -m "moa mv %s %s"' % (sysConf.moautil.mv.fr, sysConf.moautil.mv.to,
                                                      sysConf.moautil.mv.fr, sysConf.moautil.mv.to))
    #repo.index.add(map(os.path.abspath, files))
    #repo.index.commit("moa cp %s" % " ".join(sysConf.newargs))
            

#Unittest scripts
RENTEST = '''
mkdir 10.test
moa ren 10.test 20.test
[[ ! -d 10.test ]]
[[ -d 20.test ]]
moa ren 20.test 30
[[ ! -d 20.test ]]
[[ -d 30.test ]]
moa ren 30 40
[[ ! -d 30.test ]]
[[ -d 40.test ]]
'''

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
