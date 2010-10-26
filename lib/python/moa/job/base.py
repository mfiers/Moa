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
Job
"""

import os
import re
import sys
import tempfile

import moa.utils
import moa.logger as l
import moa.conf
import moa.template
import moa.utils

MOABASE = moa.utils.getMoaBase()
        
class BaseJob(object):
    """
    New MoaJob class - should combine a lot of functionality
    that is now spread around over multiple locations
    """
    def __init__(self, wd):
        self.wd = wd
        self.conf = moa.conf.Config(self)
        

    @moa.utils.deprecated
    def saveConfig(self):
        self.conf.save()

    @moa.utils.deprecated
    def loadConfig(self):
        self.conf.load()
        
    @moa.utils.deprecated
    def setConf(self, item):
        self.conf.add(item)

    @moa.utils.deprecated
    def setConfKV(self, key, value, operator='='):
        self.conf.add(key, operator, value)

    @moa.utils.deprecated
    def setConfFromString(self, s):
        self.conf.add(s)
        
    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        """
        pass
    
    def new(self, *args, **kwargs):
        """
        Create a new job

        needs to be overridden for now
        """
        pass

def check(what):
    """
    Check if a template exists

        >>> check('gather')
        True
        >>> check('nonexistingtemplate')
        False
        >>> check('emboss/revseq')
        True
        >>> check('moa/base')
        False
        
    """
    templatefile = os.path.join(TEMPLATEDIR, what + '.mk')
    if not os.path.exists(templatefile):
        return False
    return True

def list():
    """
    List all known templates

        >>> result = list()
        >>> len(result) > 0
        True
        >>> type(result) == type([])
        True
        >>> 'adhoc' in result
        True
        >>> '__moaBase' in result
        False
        >>> 'moa/base' in result
        False
        >>> 'emboss/revseq' in result
        True

    @returns: a list with all known templates
    @rtype: a list of strings
    
    """
    r = []
    for path, dirs, files in os.walk(TEMPLATEDIR):
        relPath = path.replace(TEMPLATEDIR, '')
        if relPath and relPath[0] == '/':
            relPath = relPath[1:]
        if relPath[:3] == 'moa' :
            continue
        if relPath[:4] == 'util' :
            continue
        if relPath and relPath[-1] != '/':
            relPath += '/'
        files.sort()
        for f in files:
            if f[0] == '.': continue
            if f[0] == '_': continue
            if f[0] == '#': continue
            if f[-1] == '~': continue
            if not '.mk' in f: continue
            r.append(relPath  + f.replace('.mk', ''))
    return r

def _getDescription(template):
    """
    Parse a template and extract the template_description

        >>> desc = _getDescription('adhoc')
        >>> type(desc) == type('hi')
        True
        >>> len(desc) > 0
        True
        >>> 'The' in desc
        True
        
    @param template: the name of the template to get the
      description from
    @type template: string
    @returns: template_description
    @rtype: string
    """
    desc = ''
    with open(os.path.join(TEMPLATEDIR, '%s.mk' % template), 'r') as F:
        inDesc = False
        while True:
            line = F.readline()
            if not line: break
            line = line.strip()

            if inDesc:
                desc += " " + line
            elif line.find('template_description') == 0:
                inDesc = True                
                desc = line.split('=', 1)[1].strip()
            if inDesc :
                if desc and desc[-1] == '\\':
                    desc = desc[:-1]
                else:
                    break
    return " ".join(desc.split())

def listLong():
    """
    Returns a generator yielding tuples of all templates and a
    corresponding description.

        >>> ll = listLong()
        >>> fi = ll.next()
        >>> type(fi) == type((1,2))
        True
        >>> type(fi[0]) == type('hi')
        True
        >>> type(fi[1]) == type('hi')
        True

    @returns: a generator yielding (name, description) tupels
    @rtype: generator
    """
    for template in list():
        yield template, _getDescription(template)


# @moa.utils.deprecated
# def newJob(template,
#            title = None,
#            wd = '.',
#            parameters = [],
#            force = False,
#            titleCheck = True,
#            noInit = False):
#     """
#     Create a new template based makefile in the current dir.

#         >>> d = tempfile.mkdtemp()
#         >>> newJob(template = 'adhoc',
#         ...        title = 'test job creation',
#         ...        wd=d, parameters=['moa_precommand="ls"'])
#         >>> os.path.exists(os.path.join(d, 'Makefile'))
#         True
#         >>> os.path.exists(os.path.join(d, 'moa.mk'))
#         True
#         >>> moa.conf.getVar(d, 'title')
#         'test job creation'
#         >>> moa.conf.getVar(d, 'moa_precommand')
#         '"ls"'

#     @param template: The template to use for the new job
#     @param wd: Where to create the new job
#     @param title: Title of the newly created job
#     @type title: String
#     @param wd: Directory to create the new job
#     @type wd: String
#     @param parameters: A list of parameters for initialization
#     @type parameters: List of strings. Each of the strings should
#        have the following form: 'key=some value'
#     @param force: Force job creation - this overwrites older jobs
#        in the same directory
#     @type force: boolean
#     @param noInit: Skip initialization. Normally moa calls
#        `make init`. If this flag is set, this step is skipped
#     @type noInit: boolean
#     @returns: Nothing

#     """
#     l.debug("Creating template '%s'" % template)
#     l.debug("- in wd %s" % wd)

#     #is this a valid template??

#     #TODO: do something with the results of this check
#     check(template)
            
#     if not wd: wd = os.getcwd()
#     if not os.path.isdir(wd):
#         l.info("Creating wd %s" % wd)
#         os.makedirs(wd)

#     # check if a title is defined as 'title=something' on the
#     # commandline, as opposed to using the -t option
#     if not title:
#         for p in parameters:
#             if p.find('title=') == 0:
#                 title = p.split('=',1)[1].strip()
#                 parameters.remove(p)
#                 break
        
#     if (not title) and titleCheck and (not template == 'traverse'):
#         l.warning("You *must* specify a job title")
#         l.warning("You can still do so by running: ")
#         l.warning("   moa set title='something descriptive'")
#         title = ""
#     if title:
#         l.debug('creating a new moa makefile with title "%s" in %s' % (
#             title, wd))
#     else:
#         l.debug('creating a new moa makefile in %s' % ( wd))

#     makefile = os.path.join(wd, 'Makefile')
#     moamk = os.path.join(wd, 'moa.mk')
#     moamklock = os.path.join(wd, 'moa.mk.lock')
    
#     if os.path.exists(makefile):
#         l.debug("Makefile exists!")
#         if not force:
#             l.critical("makefile exists, use -f (--force) to overwrite")
#             sys.exit(1)

#     l.debug("Start writing %s" % makefile)
#     F = open(makefile, 'w')
#     F.write(NEW_MAKEFILE_HEADER)
#     F.write("$(call moa_load,%s)\n" % template)

#     #include moabase
#     F.close()

#     if title:
#         with moa.utils.flock(moamklock):    
#             moamkdata = []

#             #open & rewrite an older moa.mk
#             if os.path.exists(moamk):
#                 moamkdata = open(moamk).readlines()
                    
#             F = open(moamk, 'w')
#             for line in moamkdata:
#                 if re.match("^title *=", line) and title:
#                     continue
#                 F.write(line)
                
#             if title:
#                 F.write("title=%s\n" % title)
#                 l.debug("writing title=%s to moa.mk" % title)

#             F.close()       
#             l.debug('Written moa.mk')

#     params = []
#     for p in parameters:
#         if not '=' in p: continue
#         params.append(p)
#         moa.conf.writeToConf(wd, moa.conf.parseClArgs(params))
        
#     if noInit: return

#     l.debug("Running moa initialization")
#     job = moa.runMake.MOAMAKE(wd = wd,
#                               target='initialize',
#                               captureOut = False,
#                               captureErr = False,
#                               stealth = True,
#                               verbose=False)
#     job.run()
#     job.finish()
#     l.debug("Written %s, try: moa help" % makefile)

