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
moa_id = h_blast

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
		echo "biopython appears not to be installed" ;\
		false ;\
	fi

#include moabase, if it isn't already done yet..
include $(MOABASE)/lib/gnumake/core.mk
comma=,
h_blast_db_files = \
	$(call merge,$(comma),\
		$(foreach v,\
			$(shell ls $(h_blast_db).[np]??),\
			$(hdfs_base)/user/mf/$(jid)/$(shell basename $(v))\
		)\
	)

#echo Main target for blast
.PHONY: blast
h_blast: h_upload_to_hdfs h_execute_blast h_download_from_hdfs

.PHONY: h_execute_blast
h_execute_blast:
	$(hadoop_base)/bin/hadoop jar \
		$(hadoop_base)/contrib/streaming/hadoop-*-streaming.jar \
		-D mapred.job.name="$(jid)"	\
		-D mapred.reduce.tasks=0 \
		-files $(h_blast_db_files) \
		-input $(jid)/input/*.$(h_blast_input_extension) \
		-mapper "`which blastall` -p blastn -d $(shell basename $(h_blast_db))" \
		-output $(jid)/out/

.PHONY: h_download_from_hdfs
h_download_from_hdfs:
	-rm -r output
	$(hadoop_base)/bin/hadoop dfs -get $(jid)/out out

.PHONY: h_upload_to_hdfs
h_upload_to_hdfs: h_blast_inputfiles h_blast_db
	$(hadoop_base)/bin/hadoop dfs -put prep $(jid)

.PHONY: h_blast_inputfiles
h_blast_inputfiles:
	@$(call echo, uploading input files)
	find $(h_blast_input_dir) -name "*.$(h_blast_input_extension)" | \
		xargs  -IXXX ln XXX prep/input

.PHONY: h_blast_db
h_blast_db:
	@$(call echo, preparing upload to hadoop)
	for x in $(h_blast_db).[np]??; do \
		ln $$x prep ;\
	done

#prepare for blast - i.e. create directories
.PHONY: h_blast_prepare
h_blast_prepare:
	-mkdir prep
	-mkdir prep/input
	-$(hadoop_base)/bin/hadoop dfs -rmr -skipTrash $(jid)

.PHONY: h_blast_post
h_blast_post:
	-rm -rf prep

# Convert to GFF (forward)
gff/%.gff: out/%.xml
	@echo "Create gff $@ from $<"
	cat $< | blast2gff -s $(blast_gff_source) -d query > $@

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
h_blast_report: $(blast_output_files)
	blastReport out/ -o $@

h_blast_clean:
	-rm -rf prep
	-rm -rf out
	-$(hadoop_base)/bin/hadoop dfs -rmr -skipTrash $(jid)