# export data from an assembly using gap4!

# Main target - should be first in the file
moa_main_target: check gap4export


################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += gap4export clean
gap4export_help = Export data from an assembly using gap4
clean_help = Clean up. 

# Help
moa_ids += gap4export
moa_title_gap4export = Assembly export using gap4
moa_description_gap4export = Export data from an assembly using gap4

# Output definition
moa_outputs += g4ephase
moa_output_g4ephase = ./BACID.phase
moa_output_g4ephase_help = phase of the BAC (1-3)

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data

moa_must_define += input_pattern
input_pattern_help = file name pattern

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################


infiles = $(notdir $(shell find $(input_dir) -maxdepth 1 -name "$(input_pattern)" -type d))
gap4export_phase = $(addsuffix .phase, $(infiles))
gap4export_cons = $(addsuffix .contig.fasta, $(infiles))
gap4export_gbfas = $(addsuffix .fasta, $(infiles))

.PHONY: gap4export
gap4export: gap4export_run
	
.PHONY: gap4export_run 
gap4export_run: $(gap4export_phase) $(gap4export_cons) $(gap4export_gbfas)

$(gap4export_phase): %.phase : $(input_dir)/%
	bacId=`basename $@ .phase` ;\
		bac1phase=$</$$bacId.1.phase ;\
		bacAphase=$</$$bacId.a.phase ;\
		echo "looking at $$bac1phase $$bacAphase" ;\
		if [ -f $$bac1phase ]; then \
			cp $$bac1phase $@ ;\
		elif [ -f $$bacAphase ]; then \
			cp $$bacAphase $@ ;\
		else \
			echo "1" > $@ ;\
		fi	

$(gap4export_cons): %.contig.fasta : $(input_dir)/%
	@echo creating cons $@ from $<
	export bacId=`basename $@ .contig.fasta` ;\
		if [ -f $</$$bacId.1.aux ]; then \
			export bestversion=1 ;\
			echo "Found v1 for $@" ;\
		else \
			export bestversion=a ;\
			echo "Using vA for $@" ;\
		fi ;\
		gap4ExportContig $</$$bacId $$bestversion $$bacId


$(gap4export_gbfas): %.fasta : %.contig.fasta %.contig.order
	@echo "hi $@ $<"
	seqId=`basename $@ .fasta` ;\
		cat $(word 2, $^) \
		| sort -k 3n \
		| awk '{printf "fasta::$<:" $$1; if ($$2 == "+" ) print "[1:-1]"; else print "[1:-1:r]"; printf "asis:"; for (i=1; i<=10; i+=1) printf "NNNNNNNNNN"; print ""}'  \
		| head -n -1 \
		| union -sequence @stdin -outseq stdout \
		| sed "s/>.*$$/>$$seqId/" \
		> $@
	
%.contig.order:
	@echo "looking at $@"
	bacId=`basename $@ .contig.order` ;\
		echo "bacId is $$bacId" ;\
		phasefile=$$bacId.phase ;\
		phase=`cat $$phasefile` ;\
		catfile=$(input_dir)/$${bacId}/$${bacId}cat ;\
		echo "CATFILE $$catfile" ;\
		count=1 ;\
		if [ -f $$catfile ]; then \
			echo "CATFILE EXISTS!!!!! 0-------------------------------------" ;\
			for x in `grep ">" $$catfile | cut -f 1 -d" " `; do \
         		contig=`echo "$$x" | sed "s/>//"` ;\
         		if [ $phase == "1" ]; then \
            		echo -e "$$contig\t+\t$$count\t\t" >> $$bacId.contig.order ;\
         		else \
            		echo -e "$$contig\t+\t1\t\t" >> $$bacId.contig.order ;\
         		fi ;\
    	     	let count=count+1 ;\
	       done ;\
		else \
    		if [ "$$phase" == "1" ] ; then \
    			cp $$bacId.contig.phase1.default.order $$bacId.contig.order ;\
    		elif [ "$$phase" == "2" ] ; then \
    			cp $$bacId.contig.phase2.default.order $$bacId.contig.order ;\
    		else \
    			echo "not phase 1 or 2, make your own contig order (should be simple enough, I just cannot be bothered right now" ;\
    		fi ;\
    	fi
	
#CLEAN	    
.PHONY: clean    
clean: pregap_clean

.PHONY: pregap_clean
pregap_clean:
	@echo "TODO: Run clean"
		