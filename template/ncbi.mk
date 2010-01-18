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

moa_targets += getFromNcbi
getFromNcbi_help = Download some data from NCBI

moa_ids += getFromNcbi
moa_title = "Download from NCBI"
moa_description = Download a set of sequences from NCBI based on a		\
  query string (ncbi_query) and database (ncbi_db). This tempate will	\
  run only once (!), after a succesful run it creates a 'lock' file		\
  that you need to remove to rerun

getFromNcbi_help = Downloads from NCBI

moa_must_define += ncbi_query
ncbi_query_help = NCBI query (for example txid9397[Organism%3Aexp])
ncbi_query_type = string

moa_may_define = ncbi_db
ncbi_db_help = NCBI database
ncbi_db_type = string
ncbi_db_default = nuccore

moa_may_define += ncbi_sequence_name
ncbi_sequence_name_help = Sequence name to download. When this			\
  parameter is set, the template assumes that only one sequence is to	\
  be downloaded, the rest will be discarded.
ncbi_sequence_name_type = string

prereqlist += prereq_xml_twig_tools prereq_wget

prereq_xml_twig_tools:
	@$(call checkPrereqPath,xml_grep,Please install xml_grep from xml-twig-tools)

prereq_wget:
	@$(call checkPrereqPath,wget,Please install wget)

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk

#define extra variables to register in couchdb
#moa_register_extra += fastadir
#moa_register_fastadir = $(shell echo `pwd`)/fasta 

################################################################################
.PHONY: getFromNcbi_prepare
getFromNcbi_prepare:
	-mkdir fasta
	-rm tmp.xml 
	-rm tmp.fasta 
	-rm fasta/*.fasta

.PHONY: getFromNcbi_post
getFromNcbi_post:

.PHONY: getFromNcbi
getFromNcbi: tmp.fasta
	if [[ -n "$(ncbi_sequence_name)" ]]; then 								\
		cat tmp.fasta 														\
			| sed "s/^>.*$$/>$(ncbi_sequence_name)/"							\
			| fastaSplitter -f - -n 1 -o fasta;								\
	else																	\
		fastaSplitter -f tmp.fasta -o fasta;								\
	fi
	touch lock

#the fasta file as downloaded from NCBI
tmp.fasta: webEnv=$(shell xml_grep --cond "WebEnv" tmp.xml --text_only)
tmp.fasta: queryKey=$(shell xml_grep --cond "QueryKey" tmp.xml --text_only)
tmp.fasta: tmp.xml
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&rettype=fasta&retmode=text&usehistory=y" \
		-O tmp.fasta

#tmp.xml contains the IDs of the sequences to download
tmp.xml: 
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y" \
		-O tmp.xml

getFromNcbi_clean:
	-rm -r fasta
	-rm tmp.xml
	-rm tmp.fasta
	-rm getFromNcbi