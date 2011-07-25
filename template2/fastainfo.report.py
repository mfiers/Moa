#!/usr/bin/env python

import os
import sys
import yaml

def errex(message):
    print message
    sys.exit(-1)

statfiles = os.environ.get('moa_stats_files').split()

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
    F.write("!! Max sequence (contig) length\n")
    F.write("%20s   max\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['len']['max']
        F.write("%-20s %10d\n" % (k, mx))
    F.write("!# chs=1000x200\n\n")

    F.write("!! No sequences (contigs)\n")
    F.write("%20s   No\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['len']['n']
        F.write("%-20s %10d\n" % (k, mx))
    F.write("!# chs=1000x200\n\n")

    F.write("!! Total sequence length\n")
    F.write("%20s   Total\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['len']['sum']
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

    F.write("!! No N's\n")
    F.write("%20s   NoN\n" % "")
    for k in kys:
        if not data[k]['data']:
            mx = 0
        else:
            mx = data[k]['data']['non']['sum']
        F.write("%-20s %10d\n" % (k, mx))
    F.write("!# chs=1000x200\n\n")

    #write most important stats to a table
    F.write('| %15s | Tot.Seq.len | Contigs | Longest.Cnt | N50       |\n' % 'Id')
    F.write('|%s|-------------|---------|-------------|-----------|\n' % ('-' * 17))

            
    for k in kys:
        F.write("| %15s |%12.3g |%8g |%12.3g |%10.3g |\n" % (
            k[:15],
            data[k]['data']['len']['sum'],
            data[k]['data']['len']['n'],
            data[k]['data']['len']['max'],
            data[k]['data']['len']['n50'],
            ))
        
