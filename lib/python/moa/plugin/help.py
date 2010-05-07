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
l = moa.logger.l

MOABASE=os.environ['MOABASE']
JENV = None

chapters = ['introduction', 'installation',
            'commands', 'templates', 'extending',
            'reference']

COMMANDS = None

def prepare(d):
    """
    initialize this plugin
    """
    global COMMANDS
    COMMANDS = d['moaCommands']
    
def defineCommands(commands):
    commands['help'] = {
        'desc' : 'Display help',
        'call' : showHelp
        }

    commands['manual_html'] = {
        'desc' : 'Generate a HTML manual of Moa',
        'call' : createHtmlManual,
        'private' : True
        }

def showHelp(wd, options, args):
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

def pageTemplateHelp(wd, options,args):
    """
    create the help document for a specific template / job 
    """

    data = moa.info.info(wd)
    moaId = data['moa_id']
    data['d'] = data
    #see if there is a manual in $MOABASE/doc/markdown/templates
    templateDoc = os.path.join(MOABASE, 'doc', 'markdown',
                               'templates', '%s.md' % moaId)

    if os.path.exists(templateDoc):
        templateDoc = open(templateDoc).read()
    else:
        templateDoc = ""
        
    data['template_manual'] = templateDoc   
    pager(JENV.get_template('jinja2/help/template.help.md'), data)


def pager(template, data):
    """
    render the template & send it to the pager
    """
    markdown = template.render(data)
    
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

def getRenderData(wd):
    
    global COMMANDS
    commandOrder = COMMANDS.keys()
    commandOrder.sort()
    
    data = {
        'chapters' : chapters,
        'moa_version' : moa.info.getVersion(),
        'date_generated' : time.ctime(),
        'git_version' : moa.info.getGitVersion(),
        'git_branch' : moa.info.getGitBranch(),
        'commands' : COMMANDS,
        'templates' : moa.job.list(),
        'command_order' : commandOrder,
    }

    return data
    
def createHtmlManual(wd, options, args):
    """
    Create an HTML manual
    """
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

    data = getRenderData(wd)

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
    render('index.html', data)
    
    for c in chapters:
        #get the markdown & convert it to html
        content = markdown2html(
            JENV.get_template('markdown/%s.md' % c).render(data))
        data['content'] = content
        render('%s.html' % c, data)
        
    for c in COMMANDS:
        #see if there is a markdown manual for this command
        try:
            commandTemplate = JENV.get_template('markdown/commands/%s.md' % c)
            content = markdown2html(commandTemplate.render(data))
        except jinja2.exceptions.TemplateNotFound:
            content = ""
            
        #render the command template 
        data['content'] = content
        data['command_name'] = c
        data['command_desc'] = COMMANDS[c].get('desc', "")
        render('command_%s.html' % c, data, template='command_template.html')

    for t in data['templates']:
        
        #get information on the template
        td = moa.job.newTestJob(template=t, title='help')
        inf = moa.info.info(td)
        data.update(inf)
        data['d'] = inf #don't know how else to dynamically access
                        #variables
        moaId = data['moa_id']

        #see if there is a manual in $MOABASE/doc/markdown/templates
        _td = os.path.join(MOABASE, 'doc', 'markdown',
                               'templates', '%s.md' % moaId)
        if os.path.exists(_td):
            templateManual = open(_td).read()
        else: templateManual = ""
        data['template_manual'] = markdown2html(templateManual)

        proper_name = t.replace('/', '__')
        render("template_%s.html" % proper_name, data, template='template_template.html')
        #render(JENV.get_template('jinja2/help/template.help.md'), data)
