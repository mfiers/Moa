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
moa_title = Blast
moa_description = Wraps BLAST [[Alt90]], the most popular	\
  similarity search tool in bioinformatics
moa_prerequisites += The [BLAST](http://www.ncib.nlm.nih.gov/blast)	\
  [[Alt90]] suite of tools
moa_ids += blast
blast_help = Running BLAST takes an input directory					\
  (*blast_input_dir*), determines what sequence files are present		\
  (with the parameter *blast_input_extension*) and executes BLAST on	\
  each of these. Moa BLAST is configured to create XML output (as		\
  opposed ot the standard text based output) in the *./out*				\
  directory. The output XML is subsequently converted to GFF3			\
  [[gff]] by the custom *blast2gff* script (build around biopython		\
  [[biopython]]). Additionally, a simple text report is created.		\

moa_additional_targets += blast_report
moa_blast_report_help = Generate a text BLAST report.


#########################################################################
# Prerequisite testing

prereqlist += prereq_blast_installed prereq_blast_report_installed \
  prereq_biopython_installed

prereq_blast_installed:
	@if ! which blastall >/dev/null; then \
		echo "Blast is either not installed or not in \$$PATH" ;\
		false ;\
	fi

prereq_blast_report_installed:
	@if ! which blastReport >/dev/null; then \
		echo "blastReport is either not installed or not in \$$PATH" ;\
		false ;\
	fi

prereq_biopython_installed:
	@if ! python -c "import Bio.Blast"; then \
		echo "biopython appears not to be installed" ;\
		false ;\
	fi


moa_may_define += blast_input_dir
blast_input_dir_help = directory containing the input sequences

moa_must_define += blast_db
blast_db_help = Location of the blast database
blast_db_cdbattr = blastdb
moa_must_define +=  blast_gff_source
blast_gff_source_help = source field to use in the gff

moa_may_define += input_extension
input_extension_help = input file extension

moa_may_define += blast_program
blast_program_help = blast program to use (default: blastn)

moa_may_define += blast_eval
blast_eval_help = e value cutoff

moa_may_define += blast_nohits
blast_nohits_help = number of hits to report

moa_may_define += blast_nothreads
blast_nothreads_help = threads to run blast with (note the \
	overlap with the Make -j parameter)

#preparing for gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)
#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

blast_eval ?= 1e-10
blast_program ?= blastn
blast_input_extension ?= fasta
blast_nohits ?= 100
blast_nothreads ?= 1

ifdef blast_main_phase
  blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

  blast_output_files = $(addprefix out/, \
	  $(notdir $(patsubst %.$(blast_input_extension), %.xml, $(blast_input_files))))

  blast_gff_files = $(addprefix gff/, \
	  $(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))
endif

# determine the name of a single blast db file.. to get the 
# dependencies correct...

ifdef blast_db
single_blast_db_file=$(shell ls $(blast_db)*.[pn]hr)
endif 

test:
	@echo $(blast_input_dir)
	@echo $(blast_input_extension)
	@echo $(blast_input_dir)/*.$(blast_input_extension)
	@echo $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

blast_test:
	@echo "Input extension: '$(blast_input_extension)'"
	@echo "a blastdb file: '$(single_blast_db_file)'"
	@echo "No inp files $(words $(blast_input_files))"
	@echo "No xml files $(words $(blast_output_files))"
	@echo "No gff files $(words $(blast_gff_files))"

#echo Main target for blast
.PHONY: blast
blast: $(blast_gff_files)
	@echo "Done blasting!"

#prepare for blast - i.e. create directories
.PHONY: blast_prepare
blast_prepare:	
	-mkdir out 
	-mkdir gff  	

.PHONY: blast_post
blast_post: blast_report

# Convert to GFF (forward)
gff/%.gff: out/%.xml
	@echo "Create gff $@ from $<"
	cat $< | blast2gff -s $(blast_gff_source) -d query > $@

# create out/*xml - run BLAST 
out/%.xml: $(blast_input_dir)/%.$(blast_input_extension) $(single_blast_db_file)
	@echo "Processing blast $*"
	@echo "Creating out.xml $@ from $<"
	@echo "Params $(blast_program) $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@

# creating the blastreport can only be executed when 
# all blasts are done
blast_report: $(blast_output_files)
	blastReport out/ -o $@

blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm blast_report