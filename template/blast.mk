
moa_default: moa_welcome $(addprefix prep_, $(moa_ids)) moa_check $(moa_ids) $(addprefix post_, $(moa_ids))

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
moa_targets += blast clean report
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

moa_may_define += input_dir
input_dir_help = directory with the input sequences

moa_must_define += blast_db
blast_db_help = Location of the blast database

moa_must_define +=  gff_source
gff_source_help = source field to use in the gff

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

moa_may_define +=  gff_source
gff_source_help = source field to use in the gff

moa_may_define += blast_reverse_gff
blast_reverse_gff_help = Create inverse gff
#preparing for gbrowse upload:
gup_input_dir = ./gff
gup_input_extension = gff

#function to delete the resutls from one single file:
gup_delete_single = bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -n $(gff_source)_`basename $< .gff`

#function to delete all results from this analysis
gup_delete_single = bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -t $(gff_source)

#include the code to upload stuff to gbrowse
include $(shell echo $$MOABASE)/template/upload2gbrowseInclude.mk

#include mobase, if it isn't already done yet..
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

blast_eval ?= 1e-10
blast_program ?= blastn
input_extension ?= fasta
blast_nohits ?= 100
blast_nothreads ?= 1
blast_reverse_gff ?= no

blast_input_files ?= $(wildcard $(input_dir)/*.$(input_extension))

blast_output_files = $(addprefix out/, \
	$(notdir $(patsubst %.$(input_extension), %.xml, $(blast_input_files))))

blast_gff_files = $(addprefix gff/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))

ifeq ($(blast_reverse_gff), yes)
  blast_gff_reverse_files = $(addprefix gff.reverse/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))	
else
  blast_gff_reverse_files =
endif

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
blast: blast_prepare $(blast_gff_files) $(blast_gff_reverse_files)
	@echo "Done blasting!"
blast_prepare:	
	-mkdir out 
	-mkdir gff  	
	@if [ "$(blast_reverse_gff)" == "yes" ]; then \
		mkdir gff.reverse || true; \
		echo "Creating reverse gff" ; \
	fi
status_blast:
	echo "Input files: $(words $(blast_input_files))"
	echo "blast output files: $(words $(blast_output_files))"
#from fasta to out/*.xml

out/%.xml: $(input_dir)/%.$(input_extension) $(single_blast_db_file)
	@echo "Processing $(blast_program) $< $@ with db $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@

#Convert to GFF (forward)
gff/%.gff: out/%.xml
	blast2gff -s $(gff_source) -d query < $< > $@

gff.reverse/%.gff: out/%.xml
	blast2gff -s $(blast_gff_source) -d subject < $< > $@
#creating the blastreport can only be executed when all blasts are done
report: $(blast_output_files)
	blastReport out/ -o $@
clean: blast_clean
blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm report