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
import glob
import optparse

import moa.ui
import moa.utils
import moa.actor
import moa.template
from moa.sysConf import sysConf

def hook_defineCommands():
    """
    Set the moa commands for this plugin
    """

    sysConf['commands']['raw_commands'] = {
        'private' : True,
        'log' : False,
        'needsJob' : True,
        'call' : rawCommands,
        'unittest' : TESTRAWCOMMANDS
        }
    
    sysConf['commands']['raw_parameters'] = {
        'private' : True,
        'log' : False,
        'needsJob' : True,
        'call' : rawParameters,
        }
    sysConf['commands']['version'] = {
        'desc' : 'Print the moa version',
        'call' : version,
        'log' : False,
        'needsJob' : False,
        'unittest' : TESTVERSION
        }
    sysConf['commands']['out'] = {
        'desc' : 'Returns stdout of the last moa run',
        'call' : getOut,
        'needsJob' : True,
        'log' : False,
        'unittest' : TESTOUT
        }
    sysConf['commands']['err'] = {
        'desc' : 'Returns stderr of the last moa run',
        'call' : getErr,
        'needsJob' : True,
        'log' : False,
        'unittest' : TESTERR
        }
    sysConf['commands']['tree'] = {
        'desc' : 'display a directory tree',
        'call' : tree,
        'needsJob' : False,
        'log' : False
        }


def hook_defineOptions():
    parserG = optparse.OptionGroup(
        sysConf.parser, 'moa tree')
    parserG.add_option('--ts', action='store_true',
                       dest='sparseTree', 
                       help = 'Hide all non moa jobs directories')
    
    sysConf.parser.add_option_group(parserG)


def tree(job):
    wd = job.wd
    filt = sysConf.args[1:]
    findMoaId = re.compile("^name: (\S*)$", re.M)

    output = []

    for path, dirs, files in os.walk(job.wd):
        rpath = path.replace(wd, '')[1:]

        remove = set(dirs) - set(filt)
        if not rpath and filt:
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
            if not sysConf.options.sparseTree:
                output.append(( '.', thisPath, ''))
            continue
        
        tag = '.'
        
        templateFile = os.path.join(path, '.moa', 'template')
        templateName = ""
        if os.path.exists(templateFile):
            templ = open(templateFile).read()
            findmid = findMoaId.search(templ)
            if findmid: 
                templateName = "{{blue}}%s{{reset}}" % findmid.groups()[0]
                
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
        
                      


def getOut(job):
    out = moa.actor.getLastStdout(job)
    if out == None:
        moa.ui.exitError("No stdout found")
    else:
        print out

def getErr(job):
    err = moa.actor.getLastStderr(job)
    if err == None:
        moa.ui.exitError("No stderr found")
    else:
        print err

def version(job):
    """
    **moa version** - Print the moa version number
    """
    print sysConf.getVersion()

def status(job):
    """
    **moa status** - print out a short status status message

    Usage::

       moa status
       
    """
    if job.template.name == 'nojob':
        moa.ui.fprint("%(bold)s%(red)sNot a Moa job%(reset)s")
        return
    moa.ui.fprint("%(bold)s%(green)sThis is a Moa job%(reset)s")
    moa.ui.fprint("%%(blue)s%%(bold)sTemplate name: %%(reset)s%s" %
                  job.template.name)
   
def rawCommands(job):
    """
    *(private)* **moa raw_commands** - Print a list of all known commands
    
    Usage::

        moa raw_commands

    Print a list of known Moa commands, both global, plugin defined
    commands as template specified ones. This command is mainly used
    by software interacting with Moa.
    """
    commands = sysConf.commands
    c = commands.keys()
    if job.template.name != 'nojob':
        c.extend(job.template.commands)
    print ' '.join(c)


def rawParameters(job):
    """
    *(private)* **moa raw_parameters** - Print out a list of all known parameters

    Usage::

        moa raw_parameters
        
    print a list of all defined or known parameters
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
