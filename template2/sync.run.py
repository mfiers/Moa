#!/usr/bin/env python

import os
import sys
import yaml

#walk through the input directories
dirlist = []
templateId = ""

def errex(message):
    print message
    sys.exit(-1)

source = os.environ.get('moa_source').strip()
original = os.environ.get('moa_original', "")
ignore = os.environ.get('moa_ignore').strip().split()

print "source based on %s" % source
print "ignoring", ignore

if not source:
    errex("source directory is not defined")

if not os.path.isdir(source):
    errex("Source is not a directory")

print "Source directory: %s" % source

lastAccessTime = 0
lastAccessDir = None

for indir in os.listdir('.'):
    if indir[0] == '.': continue
    if not os.path.isdir(indir):
        print "Ignoring %s (not a dir)" % indir
        continue
    
    if indir in ignore:
        print "Ignoring %s (in ignore list)" % indir
        continue
        
    templateFile = os.path.join(indir, '.moa', 'template')
    if not os.path.isfile(templateFile):
        errex("Invalid moa directory %s" % indir)

    confFile = os.path.join(indir, '.moa', 'config')

    #read timestamp
    tist = os.path.getmtime(confFile)
    #print tist, lastAccessTime, tist > lastAccessTime
    if tist > lastAccessTime:
        lastAccessTime = tist
        lastAccessDir = indir

    with open(templateFile) as F:
        template = yaml.load(F)
        if not templateId:
            templateId = template['moa_id']
        else:
            if not templateId == template['moa_id']:
                print "multiple templates (%s, %s)" % (
                    templateId, template['moa_id'])
                sys.exit(-1)

    dirlist.append(indir)

print "Found %d directories" % len(dirlist),
print "With the '%s' template" % templateId
print "Last accessed is '%s'" % lastAccessDir

if not original: 
    original = lastAccessDir

print "Using '%s' as original" % original

if not os.path.exists(original):
    print "No original found - cannot sync"
    print "set up at least one moa directory to work from"
    print "or correct original"
    sys.exit(-1)


print "start parsing the source directory"
originalConf = os.path.join(original, '.moa', 'config')

for indir in os.listdir(source):
    sourceDir = os.path.join(source, indir)
    basename = os.path.basename(indir)

    if basename in ignore:
        print "ignoring %s (in ignore list)" % basename
        continue

    if basename[0] == '.': continue
    #if not os.path.isdir(sourceDir):
    #    print "ignoring source %s (not a directory)" % indir
    #    continue
    if not basename in dirlist:
        cl = 'moa cp %s %s' % (original, basename)
        print 'Executing %s' % cl
        os.system(cl)
    else:
        targetConf = os.path.join(basename, '.moa', 'config')
        cl = 'cp %s %s' % (originalConf, targetConf)
        print "Copying configuration from %s to %s" % (original, basename)
        os.system(cl)
        cl = '(git rev-parse --git-dir 2>/dev/null) && cd %s && moa gitadd' % basename
        os.system(cl)
        continue

