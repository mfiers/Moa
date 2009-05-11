# Run BLAST
#
# for info: type 
#    make help

##### Main target
maintarget: check blast report

################################################################################
# Variable checks & definition & help

kea_title =  BLAST
kea_description = Run BLAST and convert the results to gff and a simple blast \
	report

#prerequisites
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
	
	
#outputs
kea_outputs += blastxml blastgff blastrep
kea_output_blastxml = ./out/*.xml 
kea_output_blastgff = ./gff/*.gff
kea_output_blastrep = ./blast.report
kea_output_blastxml_help = XML output of blastall
kea_output_blastgff_help = blast output converted to GFF
kea_output_blastrep_help = short report of the blast run

#targets
kea_targets += blast clean report
clean_help = remove all BLAST results
blast_help = run all BLASTs
report_help = Create a simple blast report

#variables
kea_must_define += blast_input_dir
blast_input_dir_help = directory with the input sequences

kea_must_define += blast_db
blast_db_help = Location of the blast database

kea_may_define += blast_input_ext
blast_input_ext_help = input file extension

kea_may_define += blast_program
blast_program_help = blast program to use (default: blastn)

kea_may_define += blast_eval
blast_eval_help = e value cutoff

kea_may_define += blast_nohits
blast_nohits_help = number of hits to report

kea_may_define += blast_nothreads
blast_nothreads_help = threads to run blast with (note the \
	overlap with the Make -j parameter)
	
kea_may_define +=  blast_gff_source
blast_gff_source_help = source field to use in the gff

kea_may_define += blast_reverse_gff
blast_reverse_gff_help = Create inverse gff

##### varchecks - commandline definitions
kea_may_define += blast_input_ext blast_program blast_eval blast_nohits blast_nothreads blast_gff_source						 
include $(shell echo $$KEA_BASE_DIR)/template/kea.base.mk

##### Derived variables for this run
blast_eval ?= 1e-10
blast_program ?= blastn
blast_input_ext ?= fasta
blast_nohits ?= 100
blast_nothreads ?= 1

ifeq ($(origin blast_db), undefined)
	blast_gff_source ?= $(blast_program)
else
	blast_gff_source ?= $(blast_program).$(shell basename $(blast_db))
endif

blast_reverse_gff ?= no

blast_gff_files = $(addprefix gff/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))

blast_input_files ?= $(wildcard $(blast_input_dir)/*.$(blast_input_ext))

blast_output_files = $(addprefix out/, \
	$(notdir $(patsubst %.$(blast_input_ext), %.xml, $(blast_input_files))))

	
ifeq ($(blast_reverse_gff), yes)
blast_gff_reverse_files = $(addprefix gff.reverse/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))	
else
blast_gff_reverse_files =
endif

################################################################################
# Main command definiton

blast: blast_prepare $(blast_gff_files) $(blast_gff_reverse_files)
	@echo "Done blasting!"
	
blast_prepare:	
	-mkdir out 
	-mkdir gff  	
	@if [ "$(blast_reverse_gff)" == "yes" ]; then \
		mkdir gff.reverse || true; \
		echo "Creating reverse gff" ; \
	fi
	
#from fasta to out/*.xml
out/%.xml: $(blast_input_dir)/%.$(blast_input_ext)
	@echo "Processing $(blast_program) $< $@ with db $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@

#Convert to GFF (forward)
gff/%.gff: out/%.xml
	blast2gff -s $(blast_gff_source) -d query < $< > $@

#Convert to GFF (backward)	
gff.reverse/%.gff: out/%.xml
	blast2gff -s $(blast_gff_source) -d subject < $< > $@

#creating the blastreport can only be executed when all blasts are done
report: $(blast_output_files)
	blastReport out/ -o $@
	
clean: blast_clean

blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm blast.report
	
