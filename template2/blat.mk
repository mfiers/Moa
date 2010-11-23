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
moa_id = blat

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

ifdef blat_input_file
										| awk -F . '{print $$NF}')
else 
endif

blat_output_files = $(addprefix ./out/, \
  $(patsubst %.$(blat_input_extension), %.out, \
    $(notdir $(blat_input_files))))

blat_report_files =  $(addprefix ./report/, \
  $(patsubst %.$(blat_input_extension), %.report, \
    $(notdir $(blat_input_files))))

blat_gff_files = $(addprefix ./gff/, \
  $(patsubst %.$(blat_input_extension), %.gff, \
    $(notdir $(blat_input_files))))

test:
	@echo $(blat_output_files)
	@echo $(blat_report_files)
	@echo $(blat_gff_files)

.PHONY: blat_prepare
blat_prepare:
	-mkdir out
	-mkdir gff
	@echo $(wildcard $(blat_input_dir)/*.$(blat_input_extension))

.PHONY: blat_post
blat_post: blat_report

blat: $(blat_gff_files)

blat_report: blat_report_prep $(blat_report_files)

$(blat_gff_files): ./gff/%.gff : ./out/%.out
	@echo Creating gff $@ from $<	
	awk '/^[^#]/ {if ($$1 != $$2) print $$1 \
			"\t$(blat_gff_source)\tmatch\t" \
			$$7 "\t" $$8 "\t" $$12 "\t.\t.\tID=$(blat_gff_source)_" \
			$$1 "_" $$2 "_" $$7 "_" $$8 \
			";Target=Sequence:" $$2 " " $$9 " " $$10 \
			";Blat_expect=" $$11 \
			";Blat_percent_ident=" $$3 \
			";Blat_align_length=" $$4 \
			";Blat_mismatches=" $$5 \
			";Blat_gap_openings=" $$6 } '  $< > $@

#Generate output - Run BLAT	
$(blat_output_files): ./out/%.out : $(blat_input_dir)/%.$(blat_input_extension)
	@$(call echo,Creating $@ from $<)

	blat $(blat_db) $< -t=$(blat_db_type) -q=$(blat_query_type) $@ -out=blast9 ;\

blat_report_prep:
	-mkdir report

#generate a set of report files *per* blat output
$(blat_report_files): ./report/%.report: ./out/%.out
	-rm $@.stats
	grep ">" $(blat_input_dir)/$*.$(blat_input_extension) \
			| cut -c2- | sed 's/ /\t/' | sort > ./report/$*.list
	i=`wc -l ./report/$*.list | cut -d' ' -f 1`; \
		echo -e "$$i\tNo of query sequences"  >> $@.stats
	cat $< \
		| grep -v "^#" \
		| awk '{if ($$11<=$(blat_eval)) print $$2 "\t" $$1 "\t" $$11}' \
		| sort \
		| uniq \
		> $@
	cat $@ | cut -f 1 | sort | uniq > $@.db_ids
	cat $@ | cut -f 2 | sort | uniq > $@.query_ids
	lJoin ./report/$*.list difference $@.query_ids > $@.query_no_hit	
	i=`wc -l $@.query_ids | cut -d' ' -f 1`; \
			echo -e "$$i\tNo of query sequences with a hit"  >> $@.stats
	i=`wc -l $@.query_no_hit | cut -d' ' -f 1`; \
			echo -e "$$i\tNo of query sequences without a hit"  >> $@.stats
	i=`wc -l $@.db_ids | cut -d' ' -f 1`; \
			echo -e "$$i\tNo of db sequences with a hit"  >> $@.stats	
	if [ "$(blat_db_id_list)" ] ; then \
		ln -f $(realpath $(blat_db_id_list)) ./report -s ;\
		cut -f 1 $(blat_db_id_list) | sort | \
				uniq > ./report/blat_db_id_list ;\
		join -t "`printf '\t'`" -1 1 -2 1 $@ $(blat_db_id_list) \
				-o 1.1,1.2,1.3,2.2 | sort > $@.detail; \
		lJoin ./report/blat_db_id_list difference $@.db_ids > $@.db_no_hit ;\
		i=`wc -l $@.db_no_hit | cut -d' ' -f 1`; \
		echo -e "$$i\tNo of db sequences without a hit"  >> $@.stats ;\
		i=`wc -l ./report/blat_db_id_list | cut -d' ' -f 1`; \
		echo -e "$$i\tNo of db sequences"  >> $@.stats ;\
	fi

blat_clean:
	-rm -rf ./gff
	-rm -rf ./out
	-rm -rf ./report

