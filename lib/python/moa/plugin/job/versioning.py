# Copyright 2009-2012 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**versioning** - track versioning of tools
------------------------------------------

Track what versions are used by a job

"""
import os
import moa.ui
import moa.utils
import moa.args
import subprocess as sp
import moa.logger
from moa.sysConf import sysConf

l = moa.logger.getLogger(__name__)
l.setLevel(moa.logger.DEBUG)


def _run_cl(cl):
    """helper routine meant to run a line of code and return the first
    line of the output
    """

    P = sp.Popen(cl, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    o, e = P.communicate()
    if e:
        moa.ui.warn("error tracking version information")
        moa.ui.warn("'%s' gave an error" % cl)
        moa.ui.warn("%s" % e)
    return o.strip().split("\n")[0]


def _get_specific_versioninfo(run_id):
    """
    Get the version info from a specific run_id

    :param run_id: the run id to get the version info from
    """
    version_file = os.path.join('.moa', 'version',
                                "%04d.version" % run_id)
    if not os.path.exists(version_file):
        return {}

    vd = {}
    with open(version_file) as F:
        for line in F:
            ls = line.split("\t", 1)
            if len(ls) != 2:
                l.warning("Invalid line in version file %s" % version_file)
                l.warning(line.strip())
                continue
            vd[ls[0]] = ls[1].strip()
    return vd


def _get_last_versioninfo(no=10):
    """
    determine what the last run id was, and based on that return
    the last version

    :param no: no of recent versions to retrieve
    """
    avd = {}
    run_id_file = '.moa/last_run_id'
    if not os.path.exists(run_id_file):
        return 0, {}

    try:
        last_run_id = int(open(run_id_file).read())
    except:
        #not worth crashing
        l.warning("Could not retrieve last run id")
        return 0, {}

    l.debug("last_run_id: %d" % last_run_id)

    for i in range(no):
        avd[last_run_id - i] = _get_specific_versioninfo(last_run_id - i)

    return last_run_id, avd


def hook_pelican(job):
    l.debug("pelican versioning output")
    nov = 10
    last_run_id, vinfo = _get_last_versioninfo(nov)
    vrange = list(reversed(sorted(range(last_run_id, last_run_id - nov, -1))))
    if last_run_id == 0 or vinfo == {}:
        l.warning("cannot create version info page")
        return

    allkeys = set()
    for rid in vinfo:
        allkeys.update(set(vinfo[rid]))
    allkeys = sorted(list(allkeys))

    jenv = sysConf.plugins.pelican.jenv
    jtemplate = jenv.select_template(['versioning.page.jinja2'])
    with open('./doc/pages/version.md', 'w') as F:
        F.write(jtemplate.render({
            'last_run_id': last_run_id,
            'vrange': vrange,
            'allkeys': allkeys,
            'vinfo': vinfo}))


def hook_pre_run(job):
    version_data = {'moa': sysConf.getVersion()}

    #check versioning - first generate versioning document
    versionDir = os.path.join(job.confDir, 'version')
    if not os.path.exists(versionDir):
        try:
            os.makedirs(versionDir)
        except:
            moa.ui.warn("cannot create %s" % versionDir)
            return

    #several sources of versioning information
    #first, run the core set of checks
    core_set = sysConf.plugins.job.versioning.core_set
    core_keys = sorted(core_set.keys())
    for k in core_keys:
        v = core_set[k]
        version_data[k] = _run_cl(v)

    #template set:
    template_set = job.template.prerequisites
    template_keys = template_set.keys()
    for k in template_keys:
        v = template_set[k]
        val = _run_cl(v)
        version_data[k] = val

    vfile = os.path.join(versionDir, "%04d.version" % (sysConf.runId))
    lfile = os.path.join(versionDir, "%04d.version" % (sysConf.runId - 1))
    with open(vfile, 'w') as F:
        for k in sorted(version_data.keys()):
            F.write("%s\t%s\n" % (k, version_data[k].strip()))
    if not os.path.exists(lfile):
        moa.ui.warn("No previous version information found")
        return

    lastv = {}
    with open(lfile) as F:
        for line in F:
            try:
                k, v = line.strip().split("\t", 1)
            except:
                moa.ui.warn("Invalid version line:")
                moa.ui.warn("%s" % line)
            lastv[k] = v

    #compare this & last version
    allkeys = set(version_data.keys() + lastv.keys())

    diffset = {}
    for a in allkeys:
        vn = version_data.get(a, "")
        vl = lastv.get(a, "")
        if vn != vl:
            diffset[a] = (vl, vn)

    if len(diffset) > 0:
        #differences!!
        moa.ui.warn("Version differences found")
        for k in diffset:
            v = diffset[k]
            moa.ui.warn(' - %s is now "%s" (was "%s")' % (k, v[1], v[0]))
