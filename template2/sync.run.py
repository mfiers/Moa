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

if ignore:
    print "ignoring", ignore

if not source:
    print "source directory is not defined"
    SOURCE=False
elif os.path.isdir(source):
    SOURCE=True
    print "Source directory: %s" % source
else:
    SOURCE=False
    print "No source - just syncing"

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
print "Using '%s' as original (last accessed)" % lastAccessDir

if not original: 
    original = lastAccessDir

if not os.path.exists(original):
    print "No original found - cannot sync"
    print "set up at least one moa directory to work from"
    print "or correct original"
    sys.exit(-1)


    
originalConf = os.path.join(original, '.moa', 'config')

if SOURCE:
    print "start parsing the source directory"
    sourcelist = [x for x in os.listdir(source) if os.path.isdir(os.path.join(source, x))]
    if os.path.exists('_ref'):
        sourcelist.append('_ref')

    #make sure we're not copying the file to itself
    sourcelist.remove(original)

else:
    #no sourcelist - just get a list of local directories
    sourcelist = [x for x in os.listdir('.') if os.path.isdir(x)]

print "Syncing %s to %d target(s)" % (original, len(sourcelist))
for indir in sourcelist:
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
        if basename == '_ref':
            print "Automatically locking _ref"
            os.system('cd _ref; moa lock; cd ..')
    else:
        targetConf = os.path.join(basename, '.moa', 'config')
        cl = 'cp %s %s' % (originalConf, targetConf)
        print "Copying configuration from %s to %s" % (original, basename)
        os.system(cl)
        cl = '(git rev-parse --git-dir >/dev/null 2>/dev/null) && (moa raw_commands | grep "gitadd") && cd %s && moa gitadd' % basename
        os.system(cl)
        continue

