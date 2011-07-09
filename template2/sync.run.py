#!/usr/bin/env python

import os
import yaml

#walk through the input directories
dirlist = []
templateId = ""

source = os.environ.get('moa_source')
if not source:
    print "source directory is not defined"
    sys.exit(-1)
if not os.path.isdir(source):
    print "Source is not a directory" 
    sys.exit(-1)

print "Source directory: %s" % source

for indir in os.listdir('.'):
    if indir[0] == '.': continue
    if not os.path.isdir(indir):
        print "Ignoring %s (not a dir)" % indir
        continue
    templateFile = os.path.join(indir, '.moa', 'template')
    if not os.path.isfile(templateFile):
        print "Invalid moa directory %s" % indir
        sys.exit(-1)
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

if len(dirlist) == 0:
    print "Zero directories found - cannot sync"
    print "set up at least one moa directory to work from"
    sys.exit(-1)

copySource = dirlist[0]

print "start parsing the source directory"
for indir in os.listdir(source):
    sourceDir = os.path.join(source, indir)
    basename = os.path.basename(indir)
    if basename[0] == '.': continue
    if not os.path.isdir(sourceDir):
        print "ignoring source %s (not a directory)" % indir
        continue
    if basename in dirlist:
        print "ignoring source %s (already present)" % basename
        continue

    cl = 'moa cp %s %s' % (copySource, basename)
    print 'Executing %s' % cl
    os.system(cl)
