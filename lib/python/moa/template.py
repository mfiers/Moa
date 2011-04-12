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
import glob
import shutil
import datetime

import yaml

import Yaco

import moa.ui
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

    >>> x = getTemplateFile('adhoc')
    >>> assert(x == os.path.join(moa.utils.getMoaBase(), 'template2', 'adhoc.moa'))
    >>> x= getTemplateFile('not.existing')
    Traceback (most recent call last):
      ...
    InvalidTemplate

    
    """
    if name[-4:] == '.moa' and os.path.isfile(name):
        return os.path.abspath(os.path.expanduser(name))
    
    if os.path.isfile('%s.moa' % name):        
        return os.path.abspath(os.path.expanduser(name + '.moa'))

    for templatePath in [
        os.path.join( os.path.expanduser('~'), '.config', 'moa', 'template'),
        TEMPLATEDIR]:

        templateFile = os.path.join(templatePath, '%s.moa' % name)
        if os.path.exists(templateFile):

            return templateFile

    raise InvalidTemplate()
    
def refresh(wd, default=None):
    """
    Refresh the template - try to find out what the template is from 
    {{wd}}/.moa/template.d/source. If that doesn't work, revert to the 
    default template. If default is not specified - exit with an error

    >>> import tempfile
    >>> wd = tempfile.mkdtemp()
    >>> initTemplate(wd, 'adhoc')
    >>> templateFile = os.path.join(wd, '.moa', 'template')
    >>> adhocFile = os.path.join(wd, '.moa', 'template.d', 'adhoc.mk')
    >>> os.unlink(adhocFile)    
    >>> os.unlink(templateFile)
    >>> assert(not os.path.exists(templateFile))
    >>> assert(not os.path.exists(adhocFile))
    >>> refresh(wd)
    >>> assert(os.path.exists(templateFile))
    >>> assert(os.path.exists(adhocFile))
    
    """
    source = default
    meta = Yaco.Yaco()
    try:
        meta.load(os.path.join(wd, '.moa', 'template.d', 'source'))
        source = meta.source
    except (IOError):
        pass

    if not source:
        moa.ui.exitError("Cannot refresh this job")    
        
    initTemplate(wd, source)
    
def initTemplate(wd, name):
    """
    Initialize the template - this means - try to figure out where the
    template came from & copy the template files into
    `job/.moa/template` & `job/.moa/template.d/extra`.

    Currently all templates come from the moa repository. In the
    future, multiple sources must be possible

    >>> import tempfile
    >>> wd = tempfile.mkdtemp()
    >>> initTemplate(wd, 'adhoc')
    >>> templateFile = os.path.join(wd, '.moa', 'template')
    >>> adhocFile = os.path.join(wd, '.moa', 'template.d', 'adhoc.mk')
    >>> assert(os.path.exists(templateFile))
    >>> assert(os.path.exists(adhocFile))
    
    """
    #try to find the related template file
    templateFile = getTemplateFile(name)
    
    l.debug('Trying to find template %s' % name)
    l.debug("found template file: %s" % templateFile)

    extraFileDir = os.path.join(wd, '.moa', 'template.d')

    if not os.path.isdir(extraFileDir):
        os.makedirs(extraFileDir)

    shutil.copyfile(templateFile,
                    os.path.join(wd, '.moa', 'template'))
                
    #copy additional files
    templateGlob = templateFile[:-3] + '*'
    for fl in glob.glob(templateGlob):
        if fl == templateFile: continue
        shutil.copyfile(fl,  os.path.join(extraFileDir, os.path.basename(fl)))
        
    meta = Yaco.Yaco()
    meta.source = name
    meta.loaded_on = datetime.datetime.now().isoformat()
    meta.save(os.path.join(wd, '.moa', 'template.d', 'source'))
    
class Template(Yaco.Yaco):
    """
    Template extends Yaco    
    
    """
    
    def __init__(self, templateFile):
        """
        Initialze the template object, which means:
        
        * Check if the template exists, if not raise an Exception
        * Load template info

        >>> import moa.job
        >>> job = moa.job.newTestJob(template='adhoc')
        >>> tfile = os.path.join(job.confDir, 'template')
        >>> t = Template(tfile)
        >>> assert(isinstance(t, Yaco.Yaco))
        >>> assert(len(t.parameters) > 0)
        >>> assert(isinstance(t.name, str))
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
            if len(_tempTemplate) < 50 and \
                   not "\n" in _tempTemplate:
                #this must be an old style template name- try to load the template
                initTemplate(os.path.dirname(os.path.dirname(templateFile)),
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
        """
        Return a Yaco representation of the yaml-template, without any
        of this Template processing. This is really useful when
        processing a template that needs to be written back to disk
        
        >>> import moa.job
        >>> job = moa.job.newTestJob(template='adhoc')
        >>> raw = job.template.getRaw()
        >>> assert(isinstance(raw, Yaco.Yaco))
        >>> assert(raw.has_key('parameters'))
        """
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
