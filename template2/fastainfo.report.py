#!/usr/bin/env python

import os
import sys
import yaml

def errex(message):
    print message
    sys.exit(-1)

statfiles = os.environ.get('moa_stats_files').split()
#print statfiles
#sys.exit()

data = {}
for sf in statfiles:
    with open(sf) as F:
        d = yaml.load(F)
        bn = os.path.basename(d['fasta'])
        bn = bn.replace('.fasta', '')
        bn = bn.replace('.fa', '')
        bn = bn.replace('.fna', '')
        bn = bn.replace('.seq', '')
        data[bn] = d

kys = data.keys()
kys.sort()

with open('report.md', 'w') as F:
    F.write("#fasta stats\n\n")
    F.write("## Some basic length stats\n\n")
    F.write("!! Max contig length\n")
    F.write("%20s   max\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['len']['max']
        F.write("%-20s %10d\n" % (k, mx))
    F.write("!# chs=1000x200\n\n")

    F.write("!! N50\n")
    F.write("%20s   n50\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['len']['n50']
        F.write("%-20s %10d\n" % (k, mx))
    F.write("!# chs=1000x200\n\n")

