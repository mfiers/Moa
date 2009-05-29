#@+leo-ver=4-thin
#@+node:mf.20090529111457.21:@thin template/blast.mk
#@@language makefile
# Moa definitions
#@<< header >>
#@+node:mf.20090529111457.24:<< header >>
# Main target: default operation - the first target in any makefile defines what
# is executed when make is executed without parameters.
#@<< main target >>
#@+node:mf.20090529111457.25:<< main target >>
##### Main target
maintarget: check blast report
#@-node:mf.20090529111457.25:<< main target >>
#@nl
#@+others
#@+node:mf.20090529111457.26:moa definitions
# Variable checks & definition & help
moa_ids += blast
moa_title_blast =  BLAST
moa_description_blast = Run BLAST and convert the results to gff and a simple blast \
	report
#@-node:mf.20090529111457.26:moa definitions
#@+node:mf.20090529111457.28:prerequisites
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
#@-node:mf.20090529111457.28:prerequisites
#@+node:mf.20090529111457.29:target definitions
moa_targets += blast clean report
clean_help = remove all BLAST results
blast_help = run all BLASTs
report_help = Create a simple blast report
#@-node:mf.20090529111457.29:target definitions
#@+node:mf.20090529111457.30:output definitions
#outputs
moa_outputs += blastxml blastgff blastrep
moa_output_blastxml = ./out/*.xml 
moa_output_blastgff = ./gff/*.gff
moa_output_blastrep = ./blast.report
moa_output_blastxml_help = XML output of blastall
moa_output_blastgff_help = blast output converted to GFF
moa_output_blastrep_help = short report of the blast run
#@nonl
#@-node:mf.20090529111457.30:output definitions
#@+node:mf.20090529111457.27:obligatory variables
moa_must_define += blast_input_dir
blast_input_dir_help = directory with the input sequences

moa_must_define += blast_db
blast_db_help = Location of the blast database
#@-node:mf.20090529111457.27:obligatory variables
#@+node:mf.20090529111457.31:optional variables
moa_may_define += blast_input_ext
blast_input_ext_help = input file extension

moa_may_define += blast_program
blast_program_help = blast program to use (default: blastn)

moa_may_define += blast_eval
blast_eval_help = e value cutoff

moa_may_define += blast_nohits
blast_nohits_help = number of hits to report

moa_may_define += blast_nothreads
blast_nothreads_help = threads to run blast with (note the \
	overlap with the Make -j parameter)

moa_may_define +=  blast_gff_source
blast_gff_source_help = source field to use in the gff

moa_may_define += blast_reverse_gff
blast_reverse_gff_help = Create inverse gff
#@-node:mf.20090529111457.31:optional variables
#@-others
#@nonl
#@-node:mf.20090529111457.24:<< header >>
#@nl
#@<< include >>
#@+node:mf.20090529111457.32:<< include >>
include $(shell echo $$MOABASE)/template/upload2gbrowse.mk

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif
#@nonl
#@-node:mf.20090529111457.32:<< include >>
#@nl
#@<< definitions >>
#@+node:mf.20090529111457.33:<< definitions >>
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
#@nonl
#@-node:mf.20090529111457.33:<< definitions >>
#@nl
#@<< targets >>
#@+node:mf.20090529111457.35:<< targets >>
#@+all
#@+node:mf.20090529111457.36:blast
blast: blast_prepare $(blast_gff_files) $(blast_gff_reverse_files)
	@echo "Done blasting!"
#@nonl
#@-node:mf.20090529111457.36:blast
#@+node:mf.20090529111457.37:blast_prepare
blast_prepare:	
	-mkdir out 
	-mkdir gff  	
	@if [ "$(blast_reverse_gff)" == "yes" ]; then \
		mkdir gff.reverse || true; \
		echo "Creating reverse gff" ; \
	fi
#@-node:mf.20090529111457.37:blast_prepare
#@+node:mf.20090529111457.38:out/%.xml
#from fasta to out/*.xml
out/%.xml: $(blast_input_dir)/%.$(blast_input_ext)
	@echo "Processing $(blast_program) $< $@ with db $(blast_db)"
	blastall -i $< -p $(blast_program) -e $(blast_eval) -m 7 \
		-a $(blast_nothreads) -d $(blast_db) \
		-b $(blast_nohits) -v $(blast_nohits) \
		-o $@
#@nonl
#@-node:mf.20090529111457.38:out/%.xml
#@+node:mf.20090529111457.39:gff/%.gff
#Convert to GFF (forward)
gff/%.gff: out/%.xml
	blast2gff -s $(blast_gff_source) -d query < $< > $@
#@nonl
#@-node:mf.20090529111457.39:gff/%.gff
#@+node:mf.20090529120721.1:gff.reverse/%.gff
#Convert to GFF (backward)	
gff.reverse/%.gff: out/%.xml
	blast2gff -s $(blast_gff_source) -d subject < $< > $@
#@-node:mf.20090529120721.1:gff.reverse/%.gff
#@+node:mf.20090529120721.2:report
#creating the blastreport can only be executed when all blasts are done
report: $(blast_output_files)
	blastReport out/ -o $@
#@nonl
#@-node:mf.20090529120721.2:report
#@+node:mf.20090529120721.3:clean
clean: blast_clean
#@-node:mf.20090529120721.3:clean
#@+node:mf.20090529120721.4:blast_clean
blast_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm blast.report
#@nonl
#@-node:mf.20090529120721.4:blast_clean
#@-all
#@nonl
#@-node:mf.20090529111457.35:<< targets >>
#@nl
#@nonl
#@-node:mf.20090529111457.21:@thin template/blast.mk
#@-leo
