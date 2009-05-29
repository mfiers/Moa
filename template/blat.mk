# Run BLAT
#
# for info: type 
#    make help

##### Main target
maintarget: check blat blat_report

################################################################################
# Variable checks & definition & help
moa_ids += blat 
moa_title_blat =  BLAT-NT
moa_description_blat = Run BLAT with nucleotides
	
#outputs
moa_outputs += blat blat_report
moa_output_blat = ./out/*.out 
moa_output_blat_help = BLAT output file
moa_output_blat_report = ./report/NAME.report
moa_output_blat_report_help = Simple file showing all hits with a evalue better \
  then $(eval_cutoff)

#targets
moa_targets += blat clean blat_report
blat_help = run BLAT

#variables
moa_must_define += blat_db
blat_db_help = Blat db file (multifasta)

moa_must_define += input_dir
input_dir_help = input dir with the query files (in multifasta)

moa_must_define += input_extension
input_extension_help = extension of the input files

moa_may_define += eval_cutoff
eval_cutoff_help = evalue cutoff to select the reported hits on \
  (defaults to 1e-15)
 
moa_may_define += db_id_list
db_id_list_help = a sorted list of db ids and descriptions, enhances \
  the report generated
 
moa_may_define += db_type query_type
db_type_help = type of the database (dna, prot or dnax)
query_type_help = type of the query (dna, rna, prot, dnax or rnax)
  
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

eval_cutoff ?= 1e-15
db_type ?= dna
query_type ?= dna

output_files = $(addprefix ./out/, \
  $(patsubst %.$(input_extension), %.out, \
    $(notdir $(wildcard $(input_dir)/*.$(input_extension)))))
    
report_files =  $(addprefix ./report/, \
  $(patsubst %.$(input_extension), %.report, \
    $(notdir $(wildcard $(input_dir)/*.$(input_extension)))))
     
gff_files = $(addprefix ./gff/, \
  $(patsubst %.$(input_extension), %.gff, \
    $(notdir $(wildcard $(input_dir)/*.$(input_extension)))))
    
blat: blat_prep $(output_files) blat_report blat_gff 

blat_report: blat_report_prep $(report_files)
		
blat_gff: blat_gff_prep $(gff_files)

#prepare blat
blat_prep:
	-mkdir out
	@echo $(wildcard $(input_dir)/*.$(input_extension))

#Generate output - Run BLAT	
$(output_files): ./out/%.out : $(input_dir)/%.$(input_extension)
	@echo creating $@
	@echo from $<
	blat $(blat_db) $< -t=$(db_type) -q=$(query_type) $@ -out=blast9 ;\
	
	
blat_report_prep:
	-mkdir report

$(report_files): ./report/%.report: ./out/%.out
	-rm $@.stats
	grep ">" $(input_dir)/$*.$(input_extension) | cut -c2- | sed 's/ /\t/' | sort > ./report/$*.list
	i=`wc -l ./report/$*.list | cut -d' ' -f 1`; echo -e "$$i\tNo of query sequences"  >> $@.stats
	cat $< \
		| grep -v "^#" \
		| awk '{if ($$11<=$(eval_cutoff)) print $$2 "\t" $$1 "\t" $$11}' \
		| sort \
		| uniq \
		> $@
	cat $@ | cut -f 1 | sort | uniq > $@.db_ids
	cat $@ | cut -f 2 | sort | uniq > $@.query_ids
	lJoin ./report/$*.list difference $@.query_ids > $@.query_no_hit	
		
	i=`wc -l $@.query_ids | cut -d' ' -f 1`; echo -e "$$i\tNo of query sequences with a hit"  >> $@.stats
	i=`wc -l $@.query_no_hit | cut -d' ' -f 1`; echo -e "$$i\tNo of query sequences without a hit"  >> $@.stats
	i=`wc -l $@.db_ids | cut -d' ' -f 1`; echo -e "$$i\tNo of db sequences with a hit"  >> $@.stats	
	if [ "$(db_id_list)" ] ; then \
		ln -f $(realpath $(db_id_list)) ./report -s ;\
		cut -f 1 $(db_id_list) | sort | uniq > ./report/db_id_list ;\
		join -t "`printf '\t'`" -1 1 -2 1 $@ $(db_id_list) \
			-o 1.1,1.2,1.3,2.2 | sort > $@.detail; \
		lJoin ./report/db_id_list difference $@.db_ids > $@.db_no_hit ;\
		i=`wc -l $@.db_no_hit | cut -d' ' -f 1`; echo -e "$$i\tNo of db sequences without a hit"  >> $@.stats ;\
		i=`wc -l ./report/db_id_list | cut -d' ' -f 1`; echo -e "$$i\tNo of db sequences"  >> $@.stats ;\
	fi

blat_gff_prep:
	-mkdir gff
	
$(gff_files): ./gff/%.gff: ./out/%.out
	@echo Creating gff $@ from $<	
	
clean: blat_clean

blat_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	
