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

include $(MOABASE)/lib/gnumake/prepare.mk
moa_id = gsMapper

#variables
gsMapper_sfffile_cardinality = many

################################################################################
## Include MOABASE
include $(MOABASE)/lib/gnumake/core.mk################################################################################

.PHONY: gsMapper_prepare
gsMapper_prepare:

.PHONY: gsMapper_post
gsMapper_post:

.PHONY: gsMapper
gsMapper: out.gff

out.gff: out/454HCDiffs.txt 
	$e awk '/>/ {print $$1"\tgsMapperper\tPolymorphism\t"$$2"\t"$$3"\t.\t.\t.\tName SNP_$(gsMapper_name)_"$$5" ; Reference "$$4" ; variant "$$5}' $< |  tail -n +3  | cut -c 2- > out.gff
	$e awk '/>/ {print $$1"\tgsMapperper\tSNP_$(gsMapper_name)\t"$$2"\t"$$3"\t.\t.\t.\tName SNP_$(gsMapper_name)_"$$5" ; Reference "$$4" ; variant "$$5}' $< |  tail -n +3  | cut -c 2- > out2.gff

################################################################################
## A python scriptlet that adapts the HCDIF FILE
define PYTHON_ADAPT_HCDIF

index = dict([x.split() for x in open('reads.index').readlines()])
libs = set(index.values())
mll = max([len(x) for x in libs])
mllr = '%%-%ds %%s' % mll
mlls = ' ' * (mll+1)
F = open('improved.HCDiffs', 'w')
i = 0

for line in open('out/454HCDiffs.txt', 'r').readlines():
	i += 1
	if i % 1000 == 0: print '%s lines processed' % i
	if not line.strip(): 
		F.write("\n")
		continue
	if line[0] in ['>', '_', '-']: 
		F.write(line)
		continue
	ls = line.split()
	if ls[0] in ["Reads", "Other"]:
		F.write(line)
		continue
	if ls and ls[0] in index.keys():
		F.write(mllr % (index[ls[0]], line))
	else:
		F.write(line.replace(ls[0], ls[0] + mlls))
F.close()

endef
################################################################################

improved.HCDiffs: reads.index
	$(call exec_python, PYTHON_ADAPT_HCDIF)

reads.index: $(gsMapper_sfffile)
	$e for x in $(gsMapper_sfffile); do				\
		bn=`basename $$x .sff`;					\
		sffinfo -a $$x | sed "s/$$/ $$bn/";		\
	done > reads.index

ifdef gsMapper_annotation
	$(warning HHIHIH)
  annotCL= -annot $(gsMapper_annotation)
else
  annotCl=
endif

out/454HCDiffs.txt: $(gsMapper_reference_fasta) $(gsMapper_sfffile)
	$e runMapping \
		-o out -ace -fd $(annotCL) \
		-mi $(gsMapper_min_overlap_ident) \
		-ml $(gsMapper_min_overlap_len) \
		$(gsMapper_reference_fasta) \
		$(gsMapper_sfffile)

gsMapper_clean:
	$e -rm -rf out
	$e -rm -f reads.index
	$e -rm -f improved.HCDiffs
	$e -rm -f out.gff

#      #   mid = "MID1", "ACGAGTGCGT", 2;
#         mid = "MID2", "ACGCTCGACA", 2;
#         mid = "MID3", "AGACGCACTC", 2;
#         mid = "MID4", "AGCACTGTAG", 2;
#         mid = "MID5", "ATCAGACACG", 2;
#         mid = "MID6", "ATATCGCGAG", 2;
#         mid = "MID7", "CGTGTCTCTA", 2;
#         mid = "MID8", "CTCGCGTGTC", 2;
#         mid = "MID9", "TAGTATCAGC", 2;
#         mid = "MID10", "TCTCTATGCG", 2;
#         mid = "MID11", "TGATACGTCT", 2;
#         mid = "MID12", "TACTGAGCTA", 2;
#         mid = "MID13", "CATAGTAGTG", 2;
#         mid = "MID14", "CGAGAGATAC", 2;
