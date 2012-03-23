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
import moa.args
from moa.sysConf import sysConf

@moa.args.command
def archive_incl(job, args):
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

@moa.args.command
def archive_excl(job, args):
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


@moa.args.argument('name', nargs='?', help='archive name')
@moa.args.addFlag('-t', '--template', help='Store this archive as a template')
@moa.args.addFlag('-s', '--sync', help='Alternative approach to deal with sync type jobs - only include _ref directories')
@moa.args.forceable
@moa.args.localRecursive
@moa.args.command
def archive(job, args):
    """
    Archive a job, or tree with jobs for later reuse.
    
    This command stores only those files that are necessary for
    execution of this job, that is: templates & configuration. In &
    output files, and any other file are ignored. An exception to this
    are all files that start with 'moa. If the `name` is omitted, it
    is derived from the `jobid` parameter.

    It is possible to run this command recursively with the `-r`
    parameter - in which case all (moa job containing) subdirectories
    are included in the archive.
    """
    

    if args.name:
        archiveName = args.name
    else:
        archiveName = job.conf.get('jobid', None)
        if archiveName == None:
            moa.ui.exitError('When not in a moa job, you must define an ' +
                             'archive name')

    if args.template:
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
        if not args.force:
            moa.ui.exitError("%s exists - use -f to overwrite" %
                             archiveFile)

    if not args.recursive and not sysConf.job.isMoa():
        moa.ui.exitError('Nothing to archive')
        
    l.info("archiving %s" % archiveFile)
    
    TF = tarfile.open(
        name = archiveFile,
        mode = 'w:gz')

    def _addFiles(tf, path, job):
        moa.ui.message("Archiving %s" % path)
        for pattern in job.data.moaFiles:
            for fl in glob.glob(os.path.join(path, pattern)):
                if fl[-1] == '~': continue
                tf.add(fl)
                
    if args.recursive:
        for path, dirs, files in os.walk('.'):
            if os.path.exists(os.path.join(path, '.moa', 'noarchive')):
                continue
            sjob = moa.job.Job(path)
            _addFiles(TF, path, sjob)
            if args.sync and '_ref' in dirs:
                toRemove = [x for x in dirs if x != '_ref']
            else:
                toRemove = [x for x in dirs if x[0] == '.']
            [dirs.remove(x) for x in toRemove]
    else:
        _addFiles(TF, '.', job)

@moa.args.argument('todir', metavar='to', nargs='?', help='copy to this path')
@moa.args.argument('fromdir', metavar='from', nargs=1, help='copy from this path')
@moa.args.localRecursive
@moa.args.command
def cp(job, args):
    """
    Copy a moa job, or a tree with jobs (with -r).

    moa cp copies only those files defining a job: the template files
    and the job configuration. Additionaly, all files in the moa
    directory that start with `moa.` (for example `moa.description`
    are copied as well. Data and log files are not copied!. If used in
    conjunction with the -r (recursive) flag the complete tree is
    copied.
    """
    
    #remember the files copied
    sysConf.moautil.filesCopied = []

    if args.todir:
        dirTo = args.todir
    else: dirTo = '.'

    dirFrom = args.fromdir[0]
        
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

    if  not args.recursive:
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

@moa.args.argument('todir', metavar='to', nargs='?', help='copy to this path')
@moa.args.argument('fromdir', metavar='from', nargs=1, help='copy from this path')
@moa.args.localRecursive
@moa.args.command
def mv(job, args):
    """
    Move, rename or renumber a moa job.
    """

    #remember the files moved
    sysConf.moautil.filesMoved = []

    fr = args.fromdir
    
    if fr[-1] == '/':
        fr = fr[:-1]
        
    if args.todir:
        to = args.todir
    else:
        to = '.'

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
