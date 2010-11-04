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
Functions to retrieve information from Moa directories
"""

import os
import re
import sys
import time
import commands
import subprocess

import moa.logger as l
from moa.exceptions import *
import moa.utils
import moa.runMake
import moa.lock

MOABASE = moa.utils.getMoaBase()

def getPlugins(wd = None):
    """
    Get the plugins for a certain directory
    """
    if not wd:
        wd = os.getcwd()
        
    if isMoaDir(wd):
        #inside a moa job: executed a regular moa call
        result = moa.runMake.runMakeGetOutput(
            wd, target='moa_list_plugins', verbose=False,
            stealth=True ).strip().split()
    else:
        # If executed outside of a moa job we'll use a specific
        # Makefile that loads the configuration and prints out the
        # plugins globally configured
        result = moa.runMake.runMakeGetOutput(
            wd, target='get_moa_plugins', stealth=True,
            makefile = "%s/template/moa/getPluginList.mk" % MOABASE
            ).strip().split()
                
    l.debug("Plugins for '%s' are '%s'" % (wd, str(result)))
    return result


def getMoaBase():
    """
    Return the MOABASE
    
        >>> mb = getMoaBase()
        >>> type(mb) == type('string')
        True
        >>> os.path.exists(mb)
        True
        >>> os.path.exists(os.path.join(mb, 'bin', 'moa'))
        True
        
    """
    return MOABASE

def isMoaDir(d):
    """
    Is directory d a 'moa' directory?

        >>> isMoaDir('/')
        False
        >>> import moa.job
        >>> jobdir = moa.job.newTestJob('traverse')
        >>> isMoaDir(jobdir)
        True
        
    """
    makefile = os.path.join(d, 'Makefile')
    if not os.access(makefile, os.R_OK):
        #ok, this might be a moa directory, but
        #you do not have sufficient permissions
        return False
    
    l.debug('isMoaDir: checking %s' % makefile)
    if not os.path.exists(makefile):
        return False
    
    #we could run make, but that is rather slow just to check if a Makefile
    #is a proper Makefile - so, we' quickly reading the Makefile to see if
    #it imports __moaBase.mk. If it does - it's probably a Moa Makefile
    isMoa = False
    
    F = open(os.path.join(d, 'Makefile'))
    for line in F.readlines():
        if 'MOABASE' in line:
            isMoa = True
            break
        if '$(call moa_load' in line:
            isMoa = True
            break
    F.close()        
    return isMoa

def getVersion():
    """
    Get the current MOA version
    """
    version = open(os.path.join(MOABASE, 'VERSION')).read().strip()
    return version

def _simpleExec(cl, cwd=None):
    rv = subprocess.Popen(
        cl.split(), cwd = cwd, stdout=subprocess.PIPE).communicate()[0]
    return rv

def getGitVersion():
    """
    Return the git version for Moa
    """
    r =  _simpleExec("git show", MOABASE)
    return r.strip().split()[1]

def getGitBranch():
    """
    Return the current git branch
    """
    r =  _simpleExec("git branch", MOABASE)
    return r.strip().split()[1]
    
def _checkRunlock(d):
    """
    Check if the runlock file actually points to a proper process

    @returns: If the runlock is valid
    @rtype: boolean
    """
    runlockfile = os.path.join(d, 'moa.runlock')

    #does the file exist?
    if not os.path.exists(runlockfile):
        return False, None
    
    try:
        with open(runlockfile, 'r') as F:    
            pid = F.read().strip()
            pid = int(pid)
    except IOError, e:
        if e.errno == 2: #file does not exist (anymore?)
            return False, None
        #other error - raise
        raise
    except ValueError, e:
        #the file does not seem be a proper runlock
        if "invalid literal for int()" in e.message:
            #runlock should contain a PID, i.e. an integer
            l.warning("Erroneous lock file (or so it seems) - removing")
            os.unlink(runlockfile)
            return False, None
        raise
    
    if not pid:
        os.unlink(runlockfile)
        return False, None

    l.debug("Checking pid %d" % pid)

    procInfo = commands.getoutput("ps -p %d -o 'state= comm='" % pid)
    try:
        state, processName = procInfo.strip().split(' ', 1)
    except:
        state, processName = "", ""
    l.debug("pid: %d; state: %s; process: %s" % (
            pid, state, processName))
    if processName != 'make':
        l.warning("Stale lock file (or so it seems) - removing")
        try:
            os.unlink(runlockfile)
        except OSError:
            #Probably do not have the rights to remove the runlock file
            #so, ignore it
            l.warning("Failed attempt to remove the runlock file")
            pass
        return False, None

    return True, state



def status(d):
    """
    Returns the status of a directory. It will return a one of the
    following status messages:

       - notmoa - this is not a moa directory
       - waiting - a moa job, not doing anything
       - success - a moa job, not doing anything, but the last (background) run
          was successfull
       - failed - A moa job, not doing anything, but the last (background) run
          failed
       - running - this is a moa job & currently executing (runlock exists)       
       - paused - this is an executing moa job, but currently paused (runlock exists) 
       - running - this is a moa job & currently executing (runlock exists)       
       - locked - this job is locked (i.e. a lock file exists)

           >>> import moa.job
           >>> jobdir = moa.job.newTestJob('traverse')
           >>> status(jobdir)
           'waiting'
           >>> import moa.lock
           >>> moa.lock.lockJob(jobdir)
           >>> status(jobdir)
           'locked'
           >>> import tempfile
           >>> emptyDir = tempfile.mkdtemp()
           >>> moa.utils.removeMoaFiles(emptyDir)
           >>> status(emptyDir)
           'notmoa'

       
    """
    if not isMoaDir(d):
        return "notmoa"
    lockfile = os.path.join(d, 'lock')
    successfile = os.path.join(d, 'moa.success')
    failedfile = os.path.join(d, 'moa.failed')
    lockfile = os.path.join(d, 'lock')
    runlockfile = os.path.join(d, 'moa.runlock')
    isRunning, state = _checkRunlock(d)
    if isRunning and state == 'T':
        return 'paused'
    elif isRunning:
        return "running"
    elif os.path.exists(lockfile):
        return "locked"
    elif os.path.exists(successfile):
        return "success"
    elif os.path.exists(failedfile):
        return "failed"

    return "waiting"

def getTemplateFile(name):
    """
    Return the file corresponding to the template name
    """
    
    try1 = os.path.join(
        os.path.expanduser('~'), 'moa', 'template',
        '%s.mk' % name)
    if os.path.exists(try1):
        return try1
    
    try2 = os.path.join(MOABASE, 'template', '%s.mk' % name)
    if os.path.exists(try2):
        return try2

    raise Exception("Cannot find template file")
    
def getTemplateName(wd):
    """
    A better name for L{template}
    """    
    return template(wd)

def template(wd):
    """
    Return the template name of this wd
    """
    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    with open(os.path.join(wd, 'Makefile')) as F:
        for line in F.readlines():
            if 'include' in line \
                    and 'MOABASE' in line \
                    and '/template/' in line \
                    and (not '/template/moa/' in line):
                template = line.strip().split('/')[-1].replace('.mk', '')
                return template
            if '$(call moa_load,' in line:
                template = line.split(',')[1][:-2]
                return template

reFindTitle=re.compile(r'title\+?= *(.*?) *$')
def getTitle(wd):
    """
    Return the title of a moa job

    @param wd: directory to get the title of
    @type wd: String
    @returns: The title of the project
    @rtype: String
    @raises NotAMoaDirectory
    """
    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)
    moamk = os.path.join(wd, 'moa.mk')
    if not os.path.exists(moamk):
        return "(title not specified)"
    with open(moamk) as F:
        for line in F.readlines():
            m = reFindTitle.match(line)
            if not m: continue
            return  m.groups()[0]

    
def info(wd):
    """
    Retrieve a lot of information on a template

    >>> d =  moa.job.newTestJob(template='adhoc')
    >>> result = info(d)
    >>> type(result) == type({})
    True
    >>> result.has_key('moa_targets')
    True
    >>> 'clean' in result['moa_targets']
    True
    >>> result.has_key('template_description')
    True
    >>> len(result['template_description']) > 0
    True
    >>> try: result2 = info('/NOTMOA')
    ... except NotAMoaDirectory: 'ok!'
    'ok!'

    @param wd: Moa directory to retrieve info from
    @type wd: String
    
    @raises NotAMoaDirectory: when wd is not a Moa directory or does
       not exists
    
    """

    if not isMoaDir(wd):
        raise NotAMoaDirectory(wd)

    #prepare the output data structure
    rv = { 'parameters' : {} }

    outBaseName = '.moa.%d' % os.getpid()
    l.debug("using %s" % outBaseName)
    #get the information from Moa
    job = moa.runMake.MOAMAKE( wd,
                               background=False,
                               stealth = True,
                               target='info',
                               verbose=False,
                               captureOut=True,
                               captureName = 'tempfile')
    job.run()
    out = job.getOutput()
    job.finish()
    
    for line in out.split("\n"):
        line = line.strip()
        if not line: continue

        ls = line.split("\t")
        what = ls[0]
        if len(ls) > 1:
            val = " ".join(ls[1:])
        else: val = ""
        
        if what == 'moa_targets':
            rv[what] = val.split()
                  
        elif what == 'parameter':
            parname = None            
            pob = {}
            for v in ls[1:]:
                try:
                    k,v = v.split('=', 1)
                except:
                    l.critical("error parsing parameter %s" % v)
                    raise
                if k == 'mandatory':
                    if v == 'yes': pob[k] = True
                    else: pob[k] = False
                elif k == 'name':
                    parname=v
                elif k in ['value', 'help', 'default', 'type',
                           'category', 'cardinality']:
                    pob[k] = v
                elif k == 'allowed':
                    pob[k] = v.split()
                else:
                    raise ("invalid key in %s" %line)
            if pob.get('cardinality') == 'many':
                pob['value'] = pob.get('value').split()
            rv['parameters'][parname] = pob
            
        else:
            rv[what] = val

    #add some extra information - template name &  creation time
    templateName = getTemplateName(wd)
    templateFile = getTemplateFile(templateName)
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(templateFile)
    rv['template_name'] = templateName
    rv['template_file'] = templateFile
    rv['template_creation_date'] = time.ctime(ctime)
    rv['template_modification_date'] = time.ctime(mtime)

    #prepare a category ordering
    cats = {}
    for pk in rv['parameters'].keys():
        cat = rv['parameters'][pk].get('category', '')
        if not cats.has_key(cat): cats[cat] = []
        cats[cat].append(pk)
    catorder = cats.keys()
    catorder.sort()
    if "''" in catorder:
        catorder.remove('')
        catorder.insert(0, '')
    if 'advanced' in catorder:
        catorder.remove('advanced')
        catorder.append('advanced')
    for c in cats.keys():
        cats[c].sort()
        #make sure the mandatory parameters come first in the
        #ordering
        parMan = []; parOpt = []
        for p in cats[c]:
            if rv['parameters'][p]['mandatory']:
                parMan.append(p)
            else:
                parOpt.append(p)
        cats[c] = parMan + parOpt

    rv['parameter_category_order'] = catorder
    rv['parameter_categories'] = cats

    return rv

def getErr(wd):
    """
    Return the error output of a job

        >>> d =  moa.job.newTestJob(template='adhoc', title='test')
        >>> #we'r not setting adhoc_input_dir: Should result in an error
        >>> job = moa.runMake.MOAMAKE(wd=d, verbose=False, captureErr=True)
        >>> rc = job.run()
        >>> #check if there really was an error
        >>> rc > 0
        True
        >>> err = getErr(d)
        >>> len(err) > 0
        True
        >>> 'adhoc_input_dir' in err
        True

    @param wd: Directory (containing a moa job) from which
      we want to retrieve the moa stderr output
    @type wd: string
    @returns: the stderr output of the last Moa run
    @rtype: string
    
    """
    errFile = os.path.join(wd, 'moa.err')
    if not os.path.exists(errFile):
        return ""

    if not os.access(errFile, os.R_OK):
        raise MoaPermissionDenied(errFile)

    l.debug("reading error from %s" % errFile)
    return open(errFile).read()

def getOut(wd):
    """
    Return the job output

        >>> job =  moa.job.newTestJob(template='adhoc',
        ...                         title='test job')
        >>> job.conf.set('adhoc_process', 'simple')
        >>> job.captureOut = True
        >>> job.captureErr = True
        >>> rc = job.execute()
        >>> rc = job.run()
        >>> rc ==  0
        True
        >>> out = getOut(d)
        >>> len(out) > 0
        True
        >>> 'konijn' in out
        True

    @param wd: Directory (containing a moa job) from which
      we want to retrieve the moa sdtout output
    @type wd: string
    @returns: the stdout output of the last Moa run
    @rtype: string
    

    """
    outFile = os.path.join(wd, 'moa.out')

    if not os.path.exists(outFile):
        return ""

    if not os.access(outFile, os.R_OK):
        raise MoaPermissionDenied(outFile)

    l.debug("reading out from %s" % outFile)
    return open(outFile).read()
    
    



