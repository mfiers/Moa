# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**info** - Job information
---------------------------

Print info on Moa jobs and Moa
"""

import os
import re
import fnmatch

import moa.ui
import moa.utils
import moa.actor
import moa.template
import moa.args

from moa.sysConf import sysConf

@moa.args.argument('filter', nargs='?', help='show only directories that match this filter')
@moa.args.addFlag('-a', '--all')
@moa.args.command
def tree(job, args):
    """
    Show a directory tree and job status
    """
    wd = job.wd
    filt = args.filter
    findMoaId = re.compile("^name: (\S*)$", re.M)

    output = []

    for path, dirs, files in os.walk(job.wd):
        rpath = path.replace(wd, '')[1:]

        if not rpath and filt:
            remove = [d for d in dirs if not
                      fnmatch.fnmatch(d, filt)]
            while True:
                for r in remove:
                    if r in dirs:
                        dirs.remove(r)
                        break
                else:
                    break
        
        isMoa = '.moa' in dirs
        for d in dirs:
            if d[0] == '.': dirs.remove(d)
        dirs.sort()

        if not rpath: lev = 0
        else: lev = rpath.count('/') + 1

        thisPath = "%s./%s" %  (' |' * lev, rpath)

        if not isMoa:
            if args.all:
                output.append(( '.', thisPath, ''))
            continue
        
        tag = '.'
        
        templateFile = os.path.join(path, '.moa', 'template')
        templateName = ""
        if os.path.exists(templateFile):
            templ = open(templateFile).read()
            findmid = findMoaId.search(templ)
            if findmid: 
                templateName = "{{green}}%s{{reset}}" % findmid.groups()[0]
                
        lockFile = os.path.join(path, '.moa', 'lock')
        statusFile = os.path.join(path, '.moa', 'status')
        if os.path.exists(lockFile):
            tag = '{{bold}}{{cyan}}L{{reset}}'
        elif not os.path.exists(statusFile):
            tag = '{{bold}}{{black}}?{{reset}}'
        else:
            with open(statusFile) as F:
                message = F.read().strip()            
            tag = {
                'success' : '{{green}}o{{reset}}',
                'error' : '{{red}}e{{reset}}',
                'interrupted' : '{{blue}}i{{reset}}',
                'running' : '{{cyan}}r{{reset}}'
                }.get(message, '{{green}}?{{reset}}')
        output.append((tag, thisPath, templateName))


    remFor = re.compile('\{\{.*?\}\}')
    maxTemplateLen = max([len(remFor.sub("", x[2])) for x in output])
    for s,p,t in output:
        moa.ui.fprint("%s %s (%s)" % (s, p, t), f='jinja')
        #moa.ui.fprint(
        #    ("%%s %%-%ds | %%s"  % maxTemplateLen) % (s,t,p), f='jinja')

@moa.args.needsJob
@moa.args.command
def out(job, args):
    """
    Show the stdout of the most recently executed moa job
    """
    out = moa.actor.getLastStdout(job)
    if out == None:
        moa.ui.exitError("No stdout found")
    else:
        print out

@moa.args.needsJob
@moa.args.command
def err(job, args):
    """
    Show the stderr of the most recently executed moa job
    """
    err = moa.actor.getLastStderr(job)
    if err == None:
        moa.ui.exitError("No stderr found")
    else:
        print err

@moa.args.command
def version(job, args):
    """
    print moa version number
    """
    print sysConf.getVersion()

@moa.args.private
@moa.args.doNotLog
@moa.args.command
def rehash(job, args):
    """
    cache a list of variables for command line completion

    """
    print job
    print job.isMoa()
    globalCommandFile = os.path.join(
        os.path.expanduser('~'), '.config', 'moa', 'globalCommands')

    globalCommands = []
    for c in sysConf.commands.keys():
        
        if sysConf.commands[c].get('needsJob', False):
            continue
        globalCommands.append(c)
    
    with open(globalCommandFile, 'w') as F:
        F.write(" ".join(globalCommands))


@moa.args.private
@moa.args.doNotLog
@moa.args.command
def raw_commands(job, args):
    """
    return a list available commands

    Print a list of known Moa commands, both global, plugin defined
    commands as template specified ones. This command meant to be used
    by software interacting with Moa.
    """
    commands = sysConf.commands
    c = commands.keys()
    if job.template.name != 'nojob':
        c.extend(job.template.commands)
    print ' '.join(c)

@moa.args.private
@moa.args.doNotLog
@moa.args.command
def raw_parameters(job, args):
    """
    Print a list of all known parameters
    """
    if not job.isMoa():
        return
    print " ".join(job.conf.keys())

TESTRAWCOMMANDS = '''
out=`moa raw_commands`
[[ "$out" =~ "help" ]]
[[ "$out" =~ "list" ]]
[[ "$out" =~ "new" ]]
'''

TESTSCRIPT = """
moa new adhoc -t 'something'
moa set mode=simple
moa set process='echo "ERR" >&2; echo "OUT"'
moa run
moa out | grep OUT
moa err | grep ERR
moa version
"""

TESTOUT = '''
moa simple -t "test" -- echo "something"
moa run >/dev/null 2>/dev/null
out=`moa out`
[[ "$out" =~ "something" ]] || (echo "Moa out failed" ; false)
'''

TESTERR = '''
moa simple -t "test" --np
moa set process='echo "something" >&2'
moa run >/dev/null 2>/dev/null
err=`moa err`
[[ "$err" =~ "something" ]] || (echo "Moa err failed" ; false)
'''

TESTVERSION = '''
x=`moa version`
rv=`cat $MOABASE/VERSION`
[[ "$rv" == "$x" ]]
'''
