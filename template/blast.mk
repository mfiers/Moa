
#main: moa_default_target

# Variable checks & definition & help
moa_ids += blast
moa_title_blast =  BLAST
moa_description_blast = Run BLAST and convert the results to gff \
  and a simple blast report

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

moa_targets += blast report
clean_help = remove all BLAST results
blast_help = run all BLASTs
report_help = Create a simple blast report
#outputs
moa_outputs += blastxml blastgff blastrep
moa_output_blastxml = ./out/*.xml 
moa_output_blastgff = ./gff/*.gff
moa_output_blastrep = ./blast.report
moa_output_blastxml_help = XML output of blastall
moa_output_blastgff_help = blast output converted to GFF
moa_output_blastrep_help = short report of the blast run

moa_may_define += blast_input_dir
blast_input_dir_help = directory with the input sequences

moa_must_define += blast_db
blast_db_help = Location of the blast database

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

#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

blast_eval ?= 1e-10
blast_program ?= blastn
blast_input_extension ?= fasta
blast_nohits ?= 100
blast_nothreads ?= 1

blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

blast_output_files = $(addprefix out/, \
	$(notdir $(patsubst %.$(blast_input_extension), %.xml, $(blast_input_files))))

blast_gff_files = $(addprefix gff/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))

# determine the name of a single blast db file.. to get the 
# dependencies correct...
ifeq ($(blast_program), blastn)
 single_blast_db_file = $(blast_db).nhr
endif 

ifeq ($(blast_program), tblastn)
 single_blast_db_file = $(blast_db).nhr
endif

ifeq ($(blast_program), tblastx)
 single_blast_db_file = $(blast_db).nhr
endif

ifeq ($(blast_program), blastp)
 single_blast_db_file = $(blast_db).phr
endif

ifeq ($(blast_program), blastx)
 single_blast_db_file = $(blast_db).phr
endif

test:
	@echo $(blast_input_dir)
	@echo $(blast_input_extension)
	@echo $(blast_input_dir)/*.$(blast_input_extension)
	@echo $(wildcard $(blast_input_dir)/*.$(blast_input_extension))

blast_test:
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
out/%.xml: $(blast_input_dir)/%.$(blast_input_extension) $(one_blast_db_file)
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
	-rm report