# Download a set of sequences from NCBI

################################################################################
# Definitions
# targets that the enduser might want to use

moa_targets += getFromNcbi
getFromNcbi_help = Download some data from NCBI

moa_ids += getFromNcbi
moa_title_getFromNcbi = Get sequences from NCBI
moa_description_getFromNcbi = Download a set of sequences from NCBI based on a \
  query string (ncbi_query) and database (ncbi_db). This will \
  run only once (!) unless you touch the 'touched' file.# Output definition

moa_outputs += fastafile
moa_output_fastafile = ./fasta/*.fasta
moa_output_fastafile_help = A set of fasta files#varables that NEED to be defined

moa_must_define += ncbi_db ncbi_query
ncbi_db_help = NCBI database (for example nucest)
ncbi_query_help = NCBI query (for example txid9397[Organism%3Aexp])

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

#define extra variables to register in couchdb
moa_register_extra += fastadir
moa_register_fastadir = $(shell echo `pwd`)/fasta 


################################################################################
.PHONY: getFromNcbi_prepare
getFromNcbi_prepare:
	-mkdir fasta
	-rm tmp.xml 
	-rm tmp.fasta 
	-rm fasta/*.fasta


.PHONY: getFromNcbi_post
getFromNcbi_post:


getFromNcbi: fasta_files

.PHONY: fasta_files
fasta_files: tmp.fasta
	fastaSplitter -f tmp.fasta -o fasta	

#the fasta file as downloaded from NCBI
tmp.fasta: webEnv=$(shell xml_grep --cond "WebEnv" tmp.xml --text_only)
tmp.fasta: queryKey=$(shell xml_grep --cond "QueryKey" tmp.xml --text_only)
tmp.fasta: tmp.xml
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&rettype=fasta&retmode=text&usehistory=y" \
		-O tmp.fasta

#tmp.xml contains the IDs of the sequences to download
tmp.xml: executed
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y" \
		-O tmp.xml

executed:
	touch executed

getFromNcbi_clean:
	-rm -r fasta
	-rm tmp.xml
	-rm tmp.fasta
	-rm executed
