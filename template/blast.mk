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
include $(MOABASE)/template/moa/prepare.mk

moa_title = Blast
moa_description = Wraps BLAST [[Alt90]], the most popular similarity	\
  search tool in bioinformatics
moa_prerequisites += The [BLAST](http://www.ncib.nlm.nih.gov/blast)	\
  [[Alt90]] suite of tools

moa_id = blast

blast_help = Running BLAST takes an input directory			\
  (*blast_input_dir*), determines what sequence files are present	\
  (with the parameter *blast_input_extension*) and executes BLAST on	\
  each of these. Moa BLAST is configured to create XML output (as	\
  opposed ot the standard text based output) in the *./out*		\
  directory. The output XML is subsequently converted to GFF3 [[gff]]	\
  by the custom *blast2gff* script (build around biopython		\
  [[biopython]]). Additionally, a simple text report is created.  \
moa_additional_targets += blast_report
moa_blast_report_help = Generate a text BLAST report.

#########################################################################
# Prerequisite testing

prereqlist += prereq_biopython_installed
moa_prereq_simple += blastall blastReport

prereq_biopython_installed:
	@if ! python -c "import Bio.Blast"; then \
		$(call errr, Biopython is not installed) ;\
		exit -1 ;\
	fi

$(call moa_fileset_define,blast_input,fasta,Directory with the BLAST input files)

#moa_inputfile_vars += blast_input_files
moa_state_outsets  +=  blast_gff_files

moa_must_define += blast_db
blast_db_help = Location of the blast database. You can either define the \
  blast db parameter as used by blast, or any of the blast database files, \
  in which case the extension will be removed before use
blast_db_type = file

moa_may_define += blast_gff_source
blast_gff_source_default = BLAST
blast_gff_source_help = source field to use in the gff
blast_gff_source_type = string

moa_may_define += blast_program
blast_program_default = blastn
blast_program_help = blast program to use (default: blastn)
blast_program_type = set
blast_program_allowed = blastx blastn blastp tblastn tblastx

moa_may_define += blast_eval
blast_eval_default = 1e-10
blast_eval_help = e value cutoff
blast_eval_type = float

moa_may_define += blast_nohits
blast_nohits_default = 50
blast_nohits_help = number of hits to report
blast_nohits_type = integer

moa_may_define += blast_nothreads
blast_nothreads_default = 2
blast_nothreads_help = threads to run blast with (note the overlap with the Make -j parameter)
blast_nothreads_type = integer

moa_may_define += blast_gff_blasthit
blast_gff_blasthit_default = F
blast_gff_blasthit_help = (T,**F**) - export an extra blasthit feature to the created gff, grouping all hsp (match) features.
blast_gff_blasthit_type = set

blast_gff_blasthit_allowed = T                               F

#preparing for gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)

#include the moa core libraries
include $(shell echo $$MOABASE)/template/moa/core.mk

real_blast_db = $(if $(blast_db), $(shell echo "$(blast_db)" | sed "s/\.[pn]..$$//"))

#  blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_extension))
#  $(warning XXX indir $(blast_input_dir) inext $(blast_input_extension)  inf $(blast_input_files))


ifdef blast_main_phase  
  blast_output_files = $(addprefix out/, \
	  $(notdir $(patsubst %.$(blast_input_extension), %.xml, $(blast_input_files))))

  blast_gff_files = $(addprefix gff/, \
	  $(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))
endif

$(warning blast input files $(blast_input_files))
$(warning blast output files $(blast_output_files))

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
blast_report: $(blast_output_files)
	$(call echo,Creating blast reprt);
	blastReport out/ -o $@

blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm -rf error.log
	-rm blast_report

blast_unittest:	
	moa new -d 10.blastdb -t 'test blast db' blastdb							\
			bdb_fasta_file=$$MOADATA/dna/test01.fasta bdb_name=test
	cd 10.blastdb; moa 
	moa new -d 20.blast -t 'test blast' blast									\
			blast_db=../10.blastdb/test blast_input_dir=$$MOADATA/dna
	cd 20.blast; moa 
	cd 20.blast; ls
	[[ -f 20.blast/blast_report ]] || false
