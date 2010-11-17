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

moa_id = blast

moa_additional_targets += blast_report

#########################################################################
# Prerequisite testing

prereqlist += prereq_biopython_installed

prereq_biopython_installed:
	@if ! python -c "import Bio.Blast"; then \
		$(call errr, Biopython is not installed) ;\
		exit -1 ;\
	fi

#moa_inputfile_vars += blast_input_files
moa_state_outsets  +=  blast_gff_files

#preparing for gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)

#include the moa core libraries
include $(MOABASE)/lib/gnumake/core.mk
real_blast_db = $(if $(blast_db), $(shell echo "$(blast_db)" | sed "s/\.[pn]..$$//"))

#  blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_extension))
#  $(warning XXX indir $(blast_input_dir) inext $(blast_input_extension)  inf $(blast_input_files))

ifdef blast_main_phase  
  blast_output_files = $(addprefix out/, \
	  $(notdir $(patsubst %.$(blast_input_extension), %.xml, $(blast_input_files))))

  blast_gff_files = $(addprefix gff/, \
	  $(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))
endif

# determine the name of a single blast db file.. to get the 
# dependencies correct...

ifdef real_blast_db
single_blast_db_file=$(shell ls $(real_blast_db)*.[pn]s[dq] 2>/dev/null || true)
endif

blasttest:
	$(e)echo $(blast_input_dir)
	$(e)echo $(blast_input_extension)
	$(e)echo $(blast_input_dir)/*.$(blast_input_extension)
	$(e)echo $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

#echo Main target for blast
.PHONY: blast
blast: blast_report

#prepare for blast - i.e. create directories
.PHONY: blast_prepare
blast_prepare:	
	-mkdir out 2>/dev/null
	-mkdir gff 2>/dev/null

.PHONY: blast_post
blast_post:

# Convert to GFF
gff/%.gff: out/%.xml
	$(e)echo "Create gff $@ from $<"
	cat $< | blast2gff -b $(blast_gff_blasthit) -s $(blast_gff_source) -d query > $@

# create out/*xml - run BLAST 
out/%.xml: $(blast_input_dir)/%.$(blast_input_extension) $(single_blast_db_file)
	$(e) $(call echo,Running BLAST on $<)
	$(e)echo "Processing blast $*"
	$(e)echo "Creating out.xml $@ from $<"
	$(e)echo "Params $(blast_program) $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(real_blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@

# creating the blastreport can only be executed when 
# all blasts are done
blast_report: $(blast_gff_files)
	$(call echo,Creating blast reprt);
	blastReport out/ -o $@

blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm -rf error.log
	-rm blast_report

blast_unittest:	
	moa new -d 10.blastdb -t 'test blast db' blastdb \
			bdb_fasta_file=$$MOADATA/dna/test01.fasta bdb_name=test
	cd 10.blastdb; moa 
	moa new -d 20.blast -t 'test blast' blast \
			blast_db=../10.blastdb/test blast_input_dir=$$MOADATA/dna
	cd 20.blast; moa 
	cd 20.blast; ls
	[[ -f 20.blast/blast_report ]] || false
