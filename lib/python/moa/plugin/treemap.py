# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**treemap** - draw maps of jobs
-------------------------------

Control job configuration
"""
import os
import sys
import moa.ui
import moa.utils
import moa.args
import textwrap
import optparse
import moa.logger
import collections
from moa.sysConf import sysConf

l = moa.logger.getLogger(__name__)
l.setLevel(moa.logger.DEBUG)

NODES = {}
PATHS = collections.defaultdict(list)
NODECOUNT = 0

GV_HEADER = """

digraph treemap {
    node [ shape=Mrecord];
    
"""


def _graphvizHeader():
    """
    Return the Graphviz header
    """
    return GV_HEADER

def _graphvizFooter():
    """
    Return the Graphviz footer code
    """
    return '}\n\n'


def _getOrAddNode(job):
    
    fullpath = os.path.abspath(job.wd)
    if fullpath in NODES:
        return NODES[fullpath]

    l.debug("Registering job at %s" % fullpath)

    global NODECOUNT
    NODECOUNT += 1
    job.nodecount =  NODECOUNT
    NODES[fullpath] = job
    job.connected = False
    return job


def _addPath(fromNode, fromFs, toNode, toFs, nof):
    fromNode.connected = True
    PATHS[fromNode].append(
        {'fromNode' : fromNode,
         'fromFs' : fromFs,
         'toNode' : toNode,
         'toFs'   : toFs,
         'noFiles' : nof})
    
def _processJob(job):

    node = _getOrAddNode(job)

    node_wd = os.path.basename(node.wd)
    for fs in job.template.filesets:
        fsfiles = set(job.data.filesets[fs].files.absolute())
        l.debug("checking fileset %s (%d files)" %
                (fs, len(fsfiles)))
        l.debug(" -- first file: %s" % list(fsfiles)[0])
        fsinfo = job.template.filesets[fs]
        
        if fsinfo.category == 'output':
            continue
        
        fspath = os.path.abspath(job.conf[fs])
        l.debug(" -- with path %s" % fspath)

        fsbase = os.path.dirname(fspath)
        l.debug(" -- and base %s" % fsbase)
    
        #ignore fsets pointing to ourselves
        if fsbase == node_wd: continue 

        #instantiate remote job
        remoteJob = moa.job.Job(fsbase)
        remoteNode = _getOrAddNode(remoteJob)
        l.debug(" -- remote job: %s" % remoteNode.isMoa())

        undef_files = set(fsfiles)
        

        for rfs in remoteJob.template.filesets:
            rfsfiles = set(remoteJob.data.filesets[rfs].files.absolute())
            rfsinfo = remoteJob.template.filesets[rfs]
            if rfsinfo.category != 'output': continue
            rfsconf = remoteJob.conf[rfs]
            l.debug("    -- remote fileset: %s (%d files)" % (rfs, len(rfsfiles)))
            l.debug("    -- remote job wd: %s" % (remoteJob.wd))
            l.debug("    -- config: %s" % (rfsconf))
            l.debug("    -- first file: %s" % list(rfsfiles)[:1])
            uu = fsfiles & rfsfiles
            sd = fsfiles ^ rfsfiles
            l.debug("    -- union: %d -- symmetric difference %d" % (len(uu), len(sd)))
            if len(uu) > 0:
                _addPath(remoteNode, rfs, node, fs, len(uu))
    

def _nodeToDot(node):
    label=['{ <core> %s ' % node.wd]
    label.append(
        ' | %s / %s ' % (
            node.template.name, node.conf.title))
    

    ins = []
    ous = []
    
    for fs in node.template.filesets:
        fsi = node.template.filesets[fs]
        if fsi.category == 'input': ins.append(fs)
        elif fsi.category == 'output': ous.append(fs)

    if len(ins) + len(ous) > 0:
        label.append(' |{{ ')
        ins.sort()
        label.append('|'.join(["<%s> %s" % (x,x) for x in ins]))
        label.append('}|{')
        ous.sort()
        label.append('|'.join(["<%s> %s" % (x,x) for x in ous]))
        label.append('}}')
    label.append('}')
    return '    node_%s [label="%s"];' % (
        node.nodecount, "".join(label))

def _pathToDot(path):
    return "   node_%s:%s -> node_%s:%s [label=%s];" % (
        path['fromNode'].nodecount, path['fromFs'],
        path['toNode'].nodecount, path['toFs'],
        path['noFiles'])
        
        

    
    
##
## graph command
##
@moa.args.localRecursive
@moa.args.needsJob
@moa.args.command
def treemap(job, args):
    """
    Draw a tree of the job and its relations
    """

    _processJob(job)
    
    F = open('tmp.dot', 'w')
    F.write(_graphvizHeader())
    for node_path in NODES:
        node = NODES[node_path]
        F.write(_nodeToDot(node))
        F.write("\n")
    for pathKey in PATHS:
        for path in PATHS[pathKey]:
            F.write(_pathToDot(path))
            F.write("\n")
    F.write(_graphvizFooter())
    F.close()


    os.system( 'dot -Tpng -otest.png tmp.dot')
