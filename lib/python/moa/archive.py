#!/usr/bin/env python
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
Moa script - template related code
"""

import os
import re
import sys
import tarfile

import moa.logger
l = moa.logger.l

MOABASE = os.environ["MOABASE"]
TEMPLATEDIR = os.path.join(MOABASE, 'template')

def archiveError(message):
    """ 
    Generate an error & exit
    """
    if message:
        l.error(message)
    else:
        l.error('Invalid invocation of "moa archive"')

    sys.exit(-1)
    
def handler(options, args):
    l.debug("archive handler with args %s" % args)

    if len(args) == 0:
        archiveError()
        
    command = args[0]
    
    if command == 'create':
        archive_create(options, args[1:])
    elif command == 'open':
        archive_open(options, args[1:])

def archive_create(options, args):

    """ Create a archive file - nothing more than a tar.gz """

    l.debug("Start create archive")

    if len(args) != 2:
        archiveError("Usage: moa archive create NAME DIR") 

    archivefile = args[0]
    target = args[1]

    if not ".tar.bz2" in archivefile:
        archivefile += ".tar.bz2"
    
    l.debug("creating archive %s" % archivefile)
    if os.path.exists(archivefile):
        if options.force:
            os.remove(archivefile)
        else:
            archiveError("%s exists. Use -f to override" % archivefile)
            
    ball = tarfile.open(archivefile, 'w:bz2')
    targetpath = os.path.abspath(target)
    l.debug("target path %s" % targetpath)
    for root, dirs, files in os.walk(target):
        #add the dir
        fullpath = os.path.abspath(root)
        relpath = '.' + fullpath.replace(targetpath, '')
        ball.add(fullpath, relpath, recursive=False)
        l.debug("adding %s" % relpath)
        for f in files:
            if f in ['moa.mk', 'Makefile', 'moa.archive']:
                fullpath = os.path.abspath(os.path.join(root,f))
                relpath = '.' + fullpath.replace(targetpath, '')
                ball.add(fullpath, relpath)
                l.debug("adding %s" % relpath)

        #add anything that is in moa.archive
        if 'moa.archive' in files:
            xtrafile = os.path.join(root, 'moa.archive')
            for extraFile in open(xtrafile).readlines():
                extraFile = extraFile.strip()
                if not extraFile: 
                    continue
                print files
                print extraFile
                if extraFile in files:
                    fullpath = os.path.abspath(os.path.join(root,extraFile))
                    relpath = '.' + fullpath.replace(targetpath, '')
                    ball.add(fullpath, relpath)
                    l.debug("adding %s" % relpath)
    ball.close()
    l.debug("closing archive")
        

    #if "/" in target[:-1]:
    #    archiveError('Not implemented yet - cd first to %s' %
    #               target.rsplit('/',1)[0])

    #if not os.path.exists(target):
    #    archiveError("%s does not exist" % target)
        
    #l.debug('create archive "%s" from "%s"' % (name, target))
    
    #os.system(('cd %s; find . -type d  -o -name "moa.mk" -o   ' + 
    #          '-name "Makefile" -o -name ".*.moarch" > ../moa.files') % target)
    #os.system('cd %s; tar czhf ../%s.tar.gz -T ../moa.files --no-recursion' % 
    #          (target, name))
    #os.system('rm moa.files')

def archive_open(options, args):
    
    if len(args) != 2:
        archiveError("Usage: moa archive open archiveFile targetDir")

    archivefile = args[0]
    target = args[1]

    #first find the archivefile
    if not os.path.exists(archivefile):
        #see if it needs an extension
        if not '.tar.gz' == archivefile[-6:]:
            archivefile += '.tar.gz'
    if not os.path.exists(archivefile):        
        #try the archive dir in moabase
        archivefile = os.path.join(MOABASE, archives, archivefile)
    
    if not os.path.exists(archivefile):
        archiveError("Cannot find your archive")

    archivefile = os.path.abspath(archivefile)
    l.debug("discovered archivefile at %s" % archivefile)

    if not os.path.exists(target):
        os.mkdir(target)

    if not options.force:
        indir = os.listdir(target)
        if os.path.basename(archivefile) in indir:
            indir.remove( os.path.basename(archivefile))
        if len( indir) > 0:
            archiveError("Target dir is not empty, use -f to force")

    #open the tarfile & dump it
    tar = tarfile.open(archivefile)
    tar.extractall(target)
