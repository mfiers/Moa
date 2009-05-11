# Run BLAST
#
# for info: type 
#    make help

##### Main target
maintarget: check blast
	

################################################################################
# Variable checks & definition & help

help_intro:
	@echo "Run Blast!"
	@echo 
	@echo "Possible targets:"
	@echo "  - check: checks if all variables are in order"

help_output:
	@echo " ./out/*.xml: raw blast output (in XML format!)"
	@echo " ./gff/*.gff: gff representation"
	@echo " ./blast.report: short output"	

blast_input_dir_help = directory with the input sequences
blast_db_help = Location of the blast database
blast_input_ext ?= fasta
blast_input_ext_help = input file extension
blast_program ?= blastn
blast_program_help = blast program to use
blast_eval ?= 1e-10
blast_eval_help = e value cutoff
blast_nohits ?= 100
blast_nohits_help = number of hits to report
blast_nothreads ?= 1
blast_nothreads_help = threads to run blast with (mark the possible \
	overlap with the Make -j parameter) 
blast_gff_source ?= $(blast_program).$(shell basename $(blast_db))
blast_gff_source_help = source field to use in the gff
blast_reverse_gff ?= no

##### varchecks - commandline definitions
## using += allows combination of multiple makefiles
kea_must_define += blast_input_dir blast_db
kea_may_define += blast_input_ext blast_program blast_eval blast_nohits blast_nothreads blast_gff_source						 
include $(shell echo $$KEA_TEMPLATE_DIR)/kea.varcheck.mk

##### Derived variables for this run
blast_gff_files = $(addprefix gff/, \
	$(patsubst %.xml, %.gff, $(notdir $(blast_output_files))))

blast_input_files = $(wildcard $(blast_input_dir)/*.$(blast_input_ext))

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
	-mkdir out || true
	-mkdir gff || true	
	if [ "$(blast_reverse_gff)" == "yes" ]; then \
		mkdir gff.reverse || true; \
		echo "Creating reverse gff" ; \
	fi
	@echo "### Found $(words $(blast_input_files)) input files!"
	
#from fasta to out/*.xml
out/%.xml: $(blast_input_dir)/%.$(blast_input_ext)
	@echo "Processing $(blast_program) $< $@ with db $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@

#Convert to GFF (forward)
gff/%.gff: out/%.xml
	betterBlast2gff -s $(blast_gff_source) -d query < $< > $@

#Convert to GFF (backward)	
gff.reverse/%.gff: out/%.xml
	betterBlast2gff -s $(blast_gff_source) -d subject < $< > $@

#creating the blastreport can only be executed when all blasts are done
blast.report: $(blast_output_files)
	quickBlastReport.py out/ -o $@
