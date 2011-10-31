#!/usr/bin/env python

import os
import sys
from pprint import pprint
import numpy as np
import subprocess as sp
import MySQLdb

import moa.script

args = moa.script.getArgs()

seqdir = args['input_dir']
outdir = 'tables'

CUTOFF = 50

if not os.path.isdir(outdir):
    os.makedirs(outdir)

print 'seq input dir', seqdir

#read seqdir
allTaxa = []
geneCounts = []
for f in os.listdir(seqdir):
    if f[-6:] != '.fasta':
        continue
    name = f[:-6]
    allTaxa.append(name)
    seqFile = os.path.abspath(os.path.join(seqdir, f))
    cl = "grep -c '^>' %s" % seqFile
    PR = sp.Popen(cl, stdout=sp.PIPE, shell=True)
    o, e = PR.communicate()
    count =  int(o.strip())
    print "found %d genes for %s" % (count, name)
    geneCounts.append((count, name))

allTaxa = [x[1] for x in geneCounts]

print '-- found %d taxa' % len(allTaxa)
print ", ".join(allTaxa)

#read incoming taxa seqids
def readSeqIds(taxon):
    seqids = []
    with open(os.path.join(seqdir, '%s.fasta' % taxon)) as F:
        for line in F:
            if line[0] != ">": continue
            sid = line[1:].split()[0]
            seqids.append(sid)
    seqids.sort()
    print "-- found %d seqids for taxon %s" % (len(seqids), taxon)
    return seqids

#read orthomcl configuration
conf = {}
conf['dbHost'] = 'localhost'
with open('orthomcl.config') as F:
    for line in F:
        line = line.strip()
        if not line: continue
        k, v = [x.strip() for x in line.split('=',1)]
        print k, v
        if k == 'dbVendor' and v != 'mysql':
            print 'invalid db', v
            sys.exit(1)
        if k == 'dbConnectString':
            conf['db'] = v.replace('dbi:mysql:', '').split(':')[0]
        conf[k] = v

dbconn = MySQLdb.connect(
    host = conf['dbHost'],
    user = conf['dbLogin'],
    passwd = conf['dbPassword'],
    db = conf['db'])

c = dbconn.cursor()
ot = conf['orthologTable']

def saveTaxonArray(taxon, seqids, matrix):
    #save array
    print "--saving array for taxon %s" % taxon
    base = os.path.join(outdir, taxon)
    with open(base + '.tsv', 'w') as F:
        F.write("\t")
        F.write("\t".join(allTaxa))
        F.write("\n")
        for g in range(len(seqids)):
            F.write(seqids[g])
            F.write("\t")
            for t in range(len(allTaxa)):
                F.write(str(matrix[g,t]))
                F.write("\t")
            F.write("\n")


def saveTaxonUnique(taxon, seqids, matrix):
    #save array
    print "-- saving a list of unique genes for taxon %s" % taxon
    base = os.path.join(outdir, taxon)
    i = 0
    with open(base + '.unique.list', 'w') as F:
        for g in range(len(seqids)):
            noAboveCutoff = len(np.nonzero(matrix[g] >= CUTOFF)[0])
            if noAboveCutoff > 1: 
                #`self` is always above CUTOFF!
                continue

            F.write("%s\n" % seqids[g])
    #run fastaExtract
    cl = (('fastaExtract -l %s.unique.list -t %s.unique.fasta ' + 
          '-f %s/%s.fasta ') % (base, base, seqdir, taxon)).split()
    sp.call(cl)

                
def getHitsForTaxon(taxon):
    Q = """
       SELECT QUERY_ID, SUBJECT_TAXON_ID, max(PERCENT_IDENTITY)
         FROM %s
        WHERE (QUERY_TAXON_ID = "%s")
          AND SUBJECT_TAXON_ID != "%s"
     GROUP BY QUERY_ID, SUBJECT_TAXON_ID
    """ % (  conf['similarSequencesTable'],
             taxon, taxon )
    c.execute(Q)
    i = 0
    while True:
        row = c.fetchone()
        if not row: break
        yield row

def extendMatrix(taxon, seqids, taxaRead, matrix):
    print '-- extending matrix based on data from %s' % taxon
    print '-- already processed are %s' % " ".join(taxaRead)
    toAppend = []
    appendIds = []
    
    #to add a row to the SupaTable, it should be below cutoff for all 
    #taxa that are already processed
    belowCutofIndici = []
    for x in taxaRead:
        belowCutofIndici.append(allTaxa.index(x))
    print '-- taxa read indici %s'% " ".join(map(str, belowCutofIndici))

    i = 0
    for g in range(len(seqids)):
        x2 = np.take(matrix[g], belowCutofIndici)
        x3 = np.nonzero(x2 < CUTOFF)[0]
        x4 = len(x3)
        if x4 < len(taxaRead) -1: 
            #at least on of the taxa already processed
            #has a similarity to this gene > CUTOFF
            #so - this gene is already in the SUPATABLE
            continue
        toAppend.append(matrix[g])
        appendIds.append(seqids[g])
        
    return np.array(toAppend), appendIds
    
SUPMATRIX=None
GLOSEQIDS=[]
taxaRead = []

for taxid, taxon in enumerate(allTaxa):
    
    taxaRead.append(taxon)
    MATRIX=None

    print "## processing taxon %s" % taxon
    seqids = readSeqIds(taxon)    
    thisTaxId = allTaxa.index(taxon)

    outBase = os.path.join('tables', taxon)
    if os.path.exists(outBase + '.npz'):
        print "--loading %s.npz" % outBase
        with open(outBase + '.npz') as F:
            _raw = np.load(F)
            MATRIX = _raw['matrix']
    else:
        #build the matrix from the database
        MATRIX = np.zeros((len(seqids), len(allTaxa)), dtype='f8')

        #set this genes 'self' to 100
        MATRIX[:,thisTaxId] = 100

        print "-- created matrix with %d entries", \
            len(seqids) * len(allTaxa)
      
        for row in getHitsForTaxon(taxon):
            gene, tax, score = row        
            geneid = seqids.index(gene)

            try: 
                taxid = allTaxa.index(tax)
            except:
                print "cannot find taxon", tax
                sys.exit(-1)
            score = float(score)

            if MATRIX[geneid, taxid] < score:
                MATRIX[geneid, taxid] = score

    if taxid == 0:
        SUPMATRIX = MATRIX
        GLOSEQIDS = seqids
    else:
        toAppend, appendIds = extendMatrix(taxon, seqids, taxaRead, MATRIX)
        SUPMATRIX = np.vstack((SUPMATRIX, toAppend))
        GLOSEQIDS.extend(appendIds)
        print '-- Super matrix, appended %d - shape now %s' % (
            len(appendIds), np.shape(SUPMATRIX))

    saveTaxonArray(taxon, seqids, MATRIX)
    saveTaxonUnique(taxon, seqids, MATRIX)

    print "## finished processing taxon %s" % taxon

print "-- Saving super matrix"
with open('tables/super.tsv', 'w') as F:
    F.write("\t")
    F.write("\t".join(allTaxa))
    F.write("\n")
    for g in range(len(GLOSEQIDS)):
        F.write(GLOSEQIDS[g])
        F.write("\t")
        for t in range(len(allTaxa)):
            F.write(str(SUPMATRIX[g,t]))
            F.write("\t")
        F.write("\n")

print '-- Saving SuperSimpleTable'
coreGenome = []
with open('tables/super.simple.tsv', 'w') as F:
    F.write("\t")
    F.write("\t".join(allTaxa))
    F.write("\n")
    
    i = 0
    for g in range(len(GLOSEQIDS)):
        #MATRIX[:,thisTaxId] = 100
        i += 1
        if i < 5: 
            print ", ".join(map(str, SUPMATRIX[g,:]))

        if np.min(SUPMATRIX[g,:]) >= 80: 
            coreGenome.append(GLOSEQIDS[g])
            #this gene is present in all libraries - ignore
            continue

        F.write(GLOSEQIDS[g])
        F.write("\t")
        for t in range(len(allTaxa)):
            F.write(str(SUPMATRIX[g,t]))
            F.write("\t")
        F.write("\n")

print '-- Saving core genome'
with open('tables/core.list', 'w') as F:
    for gene in coreGenome:
        F.write("%s\n" % gene)

print "## DONE"



