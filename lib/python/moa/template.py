# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.template
------------

Store information on a template. This module is also responsible for
retrieving template information.

"""

import os
import shutil
import glob

import Yaco
import yaml

import moa.utils
import moa.logger as l

MOABASE = moa.utils.getMoaBase()
TEMPLATEDIR = os.path.join(MOABASE, 'template2')

class InvalidTemplate(Exception):
    """ Invalid Template """
    pass

def getTemplateFile(name):
    """
    Return a base filename for a template
    """

    templateFile = os.path.join(
        TEMPLATEDIR, '%s.moa' % name)
    
    if not os.path.exists(templateFile):
        raise InvalidTemplate()

    return templateFile
    
def initTemplate(target, name):
    #try to find the related template file

    templateFile = getTemplateFile(name)
    
    l.debug('Trying to find template %s' % name)
    l.debug("found template file: %s" % templateFile)

    extraFileDir = os.path.join(target, 'template.d')
    if not os.path.isdir(extraFileDir):
        os.makedirs(extraFileDir)

    shutil.copy(templateFile,
                os.path.join(target, 'template'))
                
    #copy additional files
    templateGlob = templateFile[:-3] + '*'
    for fl in glob.glob(templateGlob):
        if fl == templateFile: continue
        shutil.copy(fl, extraFileDir)
    
class Template(Yaco.Yaco):
    """
    Template extends Yaco

    
    
    """
    
    def __init__(self, templateFile):
        """
        Initialze the template object, which means:
        
        * Check if the template exists, if not raise an Exception
        * Load template info
        """

        super(Template, self).__init__(self)

        self.templateFile = templateFile

        #set a few defaults to be used by each template
        self.parameters = {}
        self.parameters.default_command = {
            'default' : 'run',
            'help' : 'command to run for this template',
            'optional' : True,
            'private' : True,
            }

        #try to load the template!!
        
        if os.path.exists(self.templateFile):
            _tempTemplate = open(self.templateFile).read().strip()
            if len(_tempTemplate) < 20 and \
                   not "\n" in _tempTemplate:
                #this must be an old style template name- try to load the template
                initTemplate(os.path.dirname(templateFile),
                             name = _tempTemplate)
                
            self.load(self.templateFile)
        else:
            self.name = 'nojob'
            self.backend = 'nojob'
            self.parameters = {}
            
        l.debug("set template to %s, backend %s" % (self.name, self.backend))
        if not self.name == 'nojob' and not self.modification_date:
            self.modification_date = os.path.getmtime(self.templateFile)

    def getRaw(self):
        y = Yaco.Yaco()
        y.load(self.templateFile)
        return y
    
    def saveRaw(self, raw):
        raw.save(self.templateFile)
    
    def save(self):
        raise Exception("direct saving of template files is disabled")
        
def check(what):
    """    def _getParameterCategories(self):
        order = self.parameter_category_order
        for pn in self.parameters,keys():
            p = self.parameters[pn]
            if not p.category in order:
                order.append(p.category)
        l.critical("%s" % order)
        return order
    
    parameterCategories = property(_getParameterCategories)
    

    Check if a template exists

        >>> check('adhoc')
        True
        >>> check('nonexistingtemplate')
        False
    """
    try:
        template = getTemplateFile(what)
        return True
    except:
        return False


def listAll():
    """
    List all known templates, returns a tuple of:
    (templatename, templatefile)

        >>> result = listAll()
        >>> len(result) > 0
        True
        >>> type(result) == type([])
        True

    @returns: a list with all known templates
    @rtype: a list of strings
    
    """
    r = []
    for path, dirs, files in os.walk(TEMPLATEDIR):
        relPath = path.replace(TEMPLATEDIR, '')
        if relPath and relPath[0] == '/':
            relPath = relPath[1:]
        if relPath and relPath[-1] != '/':
            relPath += '/'
        files.sort()
        for f in files:
            if f[0] == '.' or \
               f[0] == '_' or \
               f[0] == '#' or \
               f[-1] == '~'or \
               (not '.moa' in f):
                continue
            name = f.replace(".moa", "")
            r.append((os.path.join(path, f), name))
    return r

def listAllLong():
    """
    Returns a generator yielding tuples of all templates and a
    corresponding description.

        >>> ll = listAllLong()
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
    for tFile, tName in listAll():
        f = Yaco.Yaco()
        f.load(tFile)
        yield tName, f.description
