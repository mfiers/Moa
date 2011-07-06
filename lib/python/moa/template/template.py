# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.template.template
---------------------

Store information on a template. This module is also responsible for
retrieving template information.

"""

import os

import Yaco

import moa.logger as l
import moa.template

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
        
        self.parameters.jobid = {
            'help' : 'Identifier for this job - Should unique in the' +
               'context of this workflow',
            'optional' : True,
            'recursive' : False,
            'type' : 'string',
            'default' : 'unset'
            }
        
        self.filesets = {}

        #try to load the template!!
        noTemplate = False
        if not os.path.isfile(self.templateFile):
            noTemplate = True
        elif not os.access(self.templateFile, os.R_OK):
            noTemplate = True
        else:
            _tempTemplate = open(self.templateFile).read().strip()
            if len(_tempTemplate) < 50 and \
                   not "\n" in _tempTemplate:
                if os.access(self.templateFile, os.W_OK):
                    #this must be an old style template name- try to load the template
                    moa.template.installTemplate(
                        os.path.dirname(os.path.dirname(templateFile)),
                        _tempTemplate)
                else:
                    noTemplate = True



        if noTemplate:
            self.name = 'nojob'
            self.backend = 'nojob'
            self.parameters = {}
        else:
            self.load(self.templateFile)

            
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
        
