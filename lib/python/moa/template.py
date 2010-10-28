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
Template
"""

import os
import yaml
import moa.utils
import moa.logger as l

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template')

class Template(object):
    
    def __init__(self, templateName=None):
        """

        """
        self.name = 'nojob'
        self.backend = 'nojob'
        if templateName:
            self.name = templateName
                    
        #later we can do more magic here for now we assume it is a Makefile template
        
        self.templateFile = os.path.join(TEMPLATEDIR, '%s.mk' % templateName)
        self.valid = True
        
        if os.path.exists(self.templateFile):
            self.backend = 'gnumake'              
        
        l.debug("set template to %s, backend %s" % (self.name, self.backend))
                    
    def save(self, wd):
        """
        Save the template name to disk 
        """
        confDir = os.path.join(wd, '.moa')
        if not os.path.exists(confDir):
            os.mkdir(confDir)
        templateFile = os.path.join(confDir, 'template')
        with open(templateFile, 'w') as F:
            F.write(self.name)
        l.debug('wrote template name to disk')
    
    def __str__(self):
        """
        String repr. of this object
        """
        return self.name
            
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
