#!/usr/bin/env python

import os
import sys
import yaml

def errex(message):
    print message
    sys.exit(-1)


source = os.environ.get('moa_source')
original = os.environ.get('moa_original', "")

infile = os.environ.get("moa_input", None)
outfile = os.environ.get("moa_output", None)
statfile = os.environ.get("moa_stats", None)

statdir = os.path.dirname(statfile)
if not os.path.isdir(statdir):
    os.makedirs(statdir)
outdir = os.path.dirname(outfile)
if not os.path.isdir(outdir):
    os.makedirs(outdir)

if not infile:
    errex("no input file found")

def fastareader(fn):
    with open(fn) as F:
        name, seq = "", []
        for l in F:
            l = l.strip()
            if not l: continue

            if l[0] == '>':
                if name and seq:
                    yield name, "".join(seq)
                seq = []
                name = l[1:]
            else:
                seq.append("".join(l.split()).lower())
                
        if name and seq:
            yield name, "".join(seq)

def getNX(d, N):
    cutoff = np.sum(d) * N
    summ = 0
    for i in range(len(d)):
        x = d[i]
        result = x
        summ += x
        if summ > cutoff: break
    return result, i

data = {
    'len' : [],
    'gcfrac' : [],
    'non' : [],
    'nfrac'  : [],
}

with open(outfile, 'w') as G:
    G.write("#id\tlen\tgcfrac\tnoN\tnfrac\n")
    for name, seq in fastareader(infile):
        g = seq.count('g')
        c = seq.count('c')
        a = seq.count('a')
        t = seq.count('t')
        n = seq.count('n')

        ln = len(seq)
        gcfrac = float(g+c) / (g + c + a + t)
        non = n
        nfrac = float(n) / len(seq)

        data['len'].append(ln)
        data['gcfrac'].append(gcfrac)
        data['non'].append(non)
        data['nfrac'].append(nfrac)
        
        G.write("%s\t%s\t%s\t%s\t%s\n" % (name, ln, gcfrac, non, nfrac))


def getNX(d, N):
    cutoff = sum(d) * N
    summ = 0
    for i in range(len(d)):
        x = d[i]
        result = x
        summ += x
        if summ > cutoff: break
    return result, i

stts = {}
stts['data'] = {}
stts['fasta'] = infile

for k in 'len gcfrac non nfrac'.split():
    ts = {}
    d = data[k]

    if len(d) == 0: continue

    d.sort()
    ts['max'] = max(d)
    ts['sum'] = sum(d)
    ts['min'] = min(d)
    ts['median'] = d[int(len(d)/2)]
    ts['n'] = len(d)
    ts['mean'] = float(sum(d)) / len(d)
    ts['n50'] = getNX(d, 0.5)[0]
    ts['n90'] = getNX(d, 0.9)[0]
    stts['data'][k] = ts

with open(statfile, 'w') as G:
    G.write(yaml.dump(stts, default_flow_style=False))
    
