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
moa_id = vpcr_list
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

real_vpcr_list_db = $(if $(vpcr_list_db), $(shell echo "$(vpcr_list_db)" | sed "s/\.[pn]..$$//"))

ifdef real_vpcr_list_db
single_vpcr_list_db_file=$(shell ls $(real_vpcr_list_db)*.[pn]s[dq] 2>/dev/null || true)
endif

#echo Main target for vpcr_list
.PHONY: vpcr_list
vpcr_list: vpcr.out

a=2
b=2
test_2:
	echo 'x' $(if $(call seq,$(a),$(b)),Equal,Not so)

vpcr.out: vpcr.sam
	samtools view -S -f 67 vpcr.sam \
		| awk '{if ($$4 < $$8) print $$1,$$3,"+",$$4,$$9,$$8; else print $$1, $$3,"-",$$8,-1*$$9,$$4; }' \
		> vpcr.out

vpcr.sam: vpcr_input
	bowtie --all -f -S --chunkmbs 256 -y  -I 10 -X 1000 \
		-v 3 --fr -I $(vpcr_list_insert_min) -X $(vpcr_list_insert_max)		\
		 $(vpcr_list_bowtie_db) -1 forward.fasta -2 reverse.fasta			\
			> vpcr.sam

.PHONY: vpcr_input
vpcr_input: $(vpcr_list_primer_list)
	cat $< | grep -v '#' | awk '{print ">" $$1 "\n" $$2}' > forward.fasta
	cat $< | grep -v '#' | awk '{print ">" $$1 "\n" $$3}' > reverse.fasta

vpcr_list_clean:
	rm -f *.fasta vpcr.out vpcr.sam