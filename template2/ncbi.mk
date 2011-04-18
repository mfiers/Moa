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

moa_targets += ncbi

moa_id = ncbi

prereqlist += prereq_xml_twig_tools prereq_wget

prereq_xml_twig_tools:
	@$(call checkPrereqPath,xml_grep,Please install xml_grep from xml-twig-tools)

prereq_wget:
	@$(call checkPrereqPath,wget,Please install wget)

#Include base moa code - does variable checks & generates help
include $(MOABASE)/lib/gnumake/core.mk

################################################################################
.PHONY: ncbi
ncbi: $(ncbi_sequence_name).fasta
	touch .moa/lock

$(ncbi_sequence_name).fasta: $(ncbi_sequence_name).gb
	seqret -filter -osdbname2 '$(ncbi_sequence_name) oid' < $< > $@

#the fasta file as downloaded from NCBI
$(ncbi_sequence_name).gb: webEnv=$(shell xml_grep --cond "WebEnv" query.xml --text_only)
$(ncbi_sequence_name).gb: queryKey=$(shell xml_grep --cond "QueryKey" query.xml --text_only)
$(ncbi_sequence_name).gb: query.xml
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&report=gb" -O $(ncbi_sequence_name).gb

#query.xml contains the IDs of the sequences to download
query.xml: 
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y" \
		-O query.xml

ncbi_clean:
	-$e rm  *.fasta query.xml fasta.tmp *.gb *.fasta .moa/lock 2>/dev/null
