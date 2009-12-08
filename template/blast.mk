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
		$(call errr, Biopython is not installed) ;\
		exit -1 ;\
	fi


moa_must_define += blast_input_dir
blast_input_dir_help = directory containing the input sequences
blast_input_dir_type = dir

moa_must_define += blast_db
blast_db_help = Location of the blast database. This parameter can	\
	point to one of the files of the blastdb
blast_db_type = file

moa_must_define +=  blast_gff_source
blast_gff_source_help = source field to use in the gff
blast_db_type = string

moa_may_define += input_extension
input_extension_help = Input file extension
input_extension_type = string
input_extension_default = fasta

moa_may_define += blast_program
blast_program_help = blast program to use (default: blastn)
blast_program_type = set
blast_program_allowed = blastx blastn blastp tblastx tblastn
blast_program_default = blastn

moa_may_define += blast_eval
blast_eval_help = e value cutoff
blast_eval_type = float
blast_eval_default = 1e-10

moa_may_define += blast_nohits
blast_nohits_help = number of hits to report
blast_nohits_type = integer
blast_nohits_default = 50

moa_may_define += blast_nothreads
blast_nothreads_help = threads to run blast with (note the overlap				\
	with the Make -j parameter)
blast_nothreads_type = integer
blast_nothreads_default = 2
blast_nothreads_category = advanced

moa_may_define += blast_gff_blasthit
blast_gff_blasthit_help = (T,**F**) - export an extra blasthit feature			\
  to the created gff, grouping all hsp (match) features.
blast_gff_blasthit_type = set
blast_gff_blasthit_allowed = T F
blast_gff_blasthit_default = F
blast_gff_blasthit_category = advanced

#preparing for gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)
#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

blast_eval ?= $(blast_eval_default)
blast_program ?= $(blast_program_default)
blast_input_extension ?= $(blast_input_extension_default)
blast_nohits ?= $(blast_nohits_default)
blast_nothreads ?= $(blast_nothreads_default)
blast_gff_blasthit ?= $(blast_gff_blasthit_default)

ifdef blast_main_phase
  blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

  blast_output_files = $(addprefix out/, \
	  $(notdir $(patsubst %.$(blast_input_extension), %.xml, $(blast_input_files))))

  blast_gff_files = $(addprefix gff/, \
	  $(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))
endif

# determine the name of a single blast db file.. to get the 
# dependencies correct...

ifdef blast_main_phase
ifdef blast_db
single_blast_db_file=$(shell ls $(blast_db)*.[pn]hr)
endif 
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

#prepare for blast - i.e. create directories
.PHONY: blast_prepare
blast_prepare:	
	-mkdir out 
	-mkdir gff  	

.PHONY: blast_post
blast_post: blast_report

# Convert to GFF
gff/%.gff: out/%.xml
	@echo "Create gff $@ from $<"
	cat $< | blast2gff -b $(blast_gff_blasthit) -s $(blast_gff_source) -d query > $@

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
	$(call echo,Creating blast reprt);
	blastReport out/ -o $@

blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm blast_report