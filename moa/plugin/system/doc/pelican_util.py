"""
Functions to support pelican
"""
import datetime
import collections
import os
import glob

import moa.logger
from Yaco import Yaco

import jinja2


jenv = jinja2.Environment(loader=jinja2.PackageLoader('moa.plugin.system.doc'))

l = moa.logger.getLogger(__name__)


def _getpagename(name):
    """
    Create a filename for a pelican page with this name

    :param name: Name of the page
    :type name: String
    """
    pagedir = os.path.join('.moa', 'doc', 'pages')
    if not os.path.exists(pagedir):
        os.makedirs(pagedir)

    return os.path.join(pagedir, name)


def _getpostname(category):
    """
    Return a file name for a (blog) "post" -

    :param category: post category
    :type category: string
    """

    pagedir = os.path.join('.moa', 'doc', category)
    if not os.path.exists(pagedir):
        os.makedirs(pagedir)

    flist = glob.glob(os.path.join(pagedir, '*.md'))
    if len(flist) == 0:
        latest = None
    else:
        latest = max(flist, key=lambda x: os.stat(x).st_mtime)

    now = datetime.datetime.now()
    filename = os.path.join(pagedir, '%s_%d%d%d_%d%d%d.md' % (
        category, now.year, now.month, now.day,
        now.hour, now.minute, now.second))
    return filename, latest


def generate_redirect(job):
    """
    Create a redirect page

    :param job: job for the HTML redirect
    :type job: moa.job.Job object
    """
    jtemplate = jenv.select_template(['redirect.jinja2'])
    if os.path.exists('index.html'):
        os.unlink('index.html')
    with open('index.html', 'w') as F:
        F.write(jtemplate.render({
            'job': job}))


def generate_template_page(job):
    """
    create a page with template parameters

    :type job: moa.job.Job object
    """
    jtemplate = jenv.select_template(['template.page.jinja2'])
    pagename = _getpagename('template.md')

    l.debug("generate template page")
    newpage = jtemplate.render({
        't': job.template})

    with open(pagename, 'w') as F:
        F.write(newpage)


def generate_readme_page(job):
    """
    Create a parameter page for pelican
    """
    if not os.path.exists('README.md'):
        return

    targetdir = os.path.join('.moa', 'doc', 'pages')
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    targetfile = os.path.join(targetdir, 'readme.md')

    with open(targetfile, 'w') as F:
        F.write("Title: readme\n\n")
        with open('README.md') as G:
            F.write(G.read())


def generate_parameter_page(job):
    """
    Create a parameter page for pelican
    """

    jtemplate = jenv.select_template(['parameter.page.jinja2'])
    pagename = _getpagename('parameters.md')

    #max paramater key length
    mkl = max([len(x) for x in job.conf.keys()]) + 4
    mvl = max([len(str(x)) for x in dict(job.conf).values()])
    fsk = '%-' + str(mkl) + 's'
    fsv = '%-' + str(mvl) + 's'
    head1 = ('%-' + str(mkl) + 's | FLAG  | %-' + str(mvl) + 's') % \
            ('key', 'value')
    head2 = ('%-' + str(mkl) + 's | ----- | %-' + str(mvl) + 's') % \
            ('-' * mkl, '-' * mvl)

    with open(pagename, 'w') as F:
        F.write(jtemplate.render({
            'keys': sorted(job.conf.keys()),
            'conf': job.conf,
            'rendered': job.conf.render(),
            'job': job,
            'fsk': fsk,
            'fsv': fsv,
            'head1': head1,
            'head2': head2,
        }))


def generate_file_page(job):
    """
    Prepare a list of files for display
    """
    ## perform some file magic

    jtemplate = jenv.select_template(['file.page.jinja2'])
    pagename = _getpagename('files.md')

    filesets = job.template.filesets.keys()
    if len(filesets) == 0:
        #no filesets - nothing to display
        return

    filesets.sort()

    fsets = []
    fmaps = []

    data = Yaco()

    for fsid in filesets:
        templateInfo = job.template.filesets[fsid]
        files = job.data.filesets[fsid].files

        if templateInfo.type == 'set':
            fsets.append(fsid)
            continue
        elif templateInfo.type == 'map':
            fmaps.append(fsid)
            continue
        else:
            data.single['fsid'].files = files

    #rearrange the files into logical sets
    nofiles = len(job.data.filesets[(fsets + fmaps)[0]].files)

    data.sets = []
    all_categories = ['input', 'output']
    for i in range(nofiles):
        thisFiles = collections.defaultdict(list)
        max_in_category = 0
        for j, fsid in enumerate((fsets + fmaps)):
            files = job.data.filesets[fsid].files
            templateInfo = job.template.filesets[fsid]
            cat = templateInfo.category

            if not cat in all_categories:
                all_categories.append(cat)

            thisFiles[cat].append(
                [templateInfo.type,
                 fsid,
                 files[i],
                 os.path.dirname(files[i]),
                 os.path.basename(files[i])])
        max_in_category = max([len(x) for x in thisFiles.values()])
        data.sets.append((max_in_category, thisFiles))

    with open(pagename, 'w') as F:
        F.write(jtemplate.render(data))

    return
