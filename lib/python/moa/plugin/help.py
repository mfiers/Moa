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
Help
"""

import os
import sys
import time
import shutil
import pydoc
import pprint
import optparse
from subprocess import Popen, PIPE

#from jinja2 import Environment, FileSystemLoader
import jinja2

import moa.runMake
import moa.info
import moa.job
import moa.logger
import moa.plugin
l = moa.logger.l

#class Help(moa.plugin.BasePlugin):
#    pass

MOABASE=os.environ['MOABASE']
JENV = None

chapters = ['introduction', 'installation',
            'commands', 'templates', 'extending',
            'reference']

    
def defineCommands(data):
    data['commands']['help'] = {
        'desc' : 'Display help',
        'call' : showHelp
        }

    data['commands']['manual_html'] = {
        'desc' : 'Generate a HTML manual of Moa',
        'call' : createHtmlManual,
        'private' : True
        }

def showHelp(data):
    wd = data['cwd']
    optons = data['options']
    args = data['args']

    global JENV
    JENV = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(MOABASE, 'doc')))

    if not args:
        if moa.info.isMoaDir(wd):
            pageTemplateHelp(wd, options, args)
        else:
            printWelcome()
    else:
        if args[0] in chapters:
            pager(JENV.get_template('markdown/%s.md' % args[0]), getRenderData(wd))
        elif args[0] in moa.job.list():
            td = moa.job.newTestJob(template=args[0], title='help')
            pageTemplateHelp(td, options,args)
        else:
            l.error("Unknown help page, try: moa help")
            sys.exit()

def printWelcome():
    """
    print a chapter to screen
    """
    print """Welcome to MOA
--------------

More help:

Moa introduction    : moa intro
a list of templates : moa list
help on a template  : moa help TEMPLATE
website and manual  : http://mfiers.github.com/Moa/
"""

def pageTemplateHelp(data):
    """
    create the help document for a specific template / job 
    """
    wd = data['cwd']
    optons = data['options']
    args = data['args']

    jobData = moa.info.info(wd)
    moaId = jobData['moa_id']
    jobData['d'] = jobData
    #see if there is a manual in $MOABASE/doc/markdown/templates
    templateDoc = os.path.join(MOABASE, 'doc', 'markdown',
                               'templates', '%s.md' % moaId)

    if os.path.exists(templateDoc):
        templateDoc = open(templateDoc).read()
    else:
        templateDoc = ""
        
    jobData['template_manual'] = templateDoc   
    pager(JENV.get_template('jinja2/help/template.help.md'), jobData)


def pager(template, jobData):
    """
    render the template & send it to the pager
    """
    markdown = template.render(jobData)
    
    #convert jinja2 to 
    p = Popen("pandoc -s -f markdown -t man".split(),
              stdin=PIPE, stdout=PIPE)    
    p.stdin.write(markdown)
    man,err = p.communicate()
    
    p2 = Popen("nroff -c -mandoc".split(),
               stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p2.stdin.write(man)
    doc, err = p2.communicate()
  
    pydoc.pager(doc)

    
def markdown2html(md):
    """
    Convert markdown to html
    """
        
    p = Popen("pandoc -s -f markdown -t html".split(),
              stdin=PIPE, stdout=PIPE)    
    p.stdin.write(md)
    html = p.communicate()[0]    
    return html

def getRenderData(data):
    """
    collect a lot of data on this specific job - this is meant to be
    dispatched of the jinja template
    """
    wd = data['cwd']
    commandOrder = data['commands'].keys()
    commandOrder.sort()
    
    jobData = {
        'chapters' : chapters,
        'moa_version' : moa.info.getVersion(),
        'date_generated' : time.ctime(),
        'git_version' : moa.info.getGitVersion(),
        'git_branch' : moa.info.getGitBranch(),
        'commands' : data['commands'],
        'templates' : moa.job.list(),
        'command_order' : commandOrder,
    }

    return jobData
    
def createHtmlManual(data):
    """
    Create an HTML manual
    """
    wd = data['cwd']
    options = data['options']
    commands = data['commands']
    args = data['args']

    global JENV
    JENV = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(MOABASE, 'doc')))

    if len(args) > 0:
        target = args[0]
    else:
        target = os.path.join(wd, 'moa_manual')
        
    if not os.path.exists(target):
        os.makedirs(target)

    imagesFrom = os.path.join(MOABASE, 'doc', 'images')
    images = os.path.join(target, 'images')
    if os.path.exists(images):
        shutil.rmtree(images)
    shutil.copytree(imagesFrom, images)
    shutil.copy(
        os.path.join(MOABASE, 'doc', 'jinja2', 'manual', 'html', 'moa.css'),
        os.path.join(target) )

    jobData = getRenderData(data)

    def render(outName, d={}, template=None):
        """
        Render the output file (possibly based on a differently named
        template
        """
        if template == None:
            template = outName
            
        t  = JENV.get_template('jinja2/manual/html/%s' % template)
        with open(os.path.join(target, outName), 'w') as F:
            F.write(t.render(d))

    #render the index
    render('index.html', jobData)
    
    for c in chapters:
        #get the markdown & convert it to html
        content = markdown2html(
            JENV.get_template('markdown/%s.md' % c).render(jobData))
        jobData['content'] = content
        render('%s.html' % c, jobData)
        
    for c in commands:
        #see if there is a markdown manual for this command
        try:
            commandTemplate = JENV.get_template('markdown/commands/%s.md' % c)
            content = markdown2html(commandTemplate.render(jobData))
        except jinja2.exceptions.TemplateNotFound:
            content = ""
            
        #render the command template 
        jobData['content'] = content
        jobData['command_name'] = c
        jobData['command_desc'] = commands[c].get('desc', "")
        render('command_%s.html' % c, jobData, template='command_template.html')

    for t in jobData['templates']:
        
        #get information on the template
        td = moa.job.newTestJob(template=t, title='help')
        inf = moa.info.info(td)
        jobData.update(inf)
        jobData['d'] = inf #don't know how else to dynamically access
                        #variables
        moaId = jobData['moa_id']

        #see if there is a manual in $MOABASE/doc/markdown/templates
        _td = os.path.join(MOABASE, 'doc', 'markdown',
                               'templates', '%s.md' % moaId)
        if os.path.exists(_td):
            templateManual = open(_td).read()
        else: templateManual = ""
        jobData['template_manual'] = markdown2html(templateManual)

        proper_name = t.replace('/', '__')
        render("template_%s.html" % proper_name, jobData,
               template='template_template.html')
        #render(JENV.get_template('jinja2/help/template.help.md'), jobData)
