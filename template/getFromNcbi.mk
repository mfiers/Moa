# Download a set of sequences from NCBI

################################################################################
# Definitions
# targets that the enduser might want to use

moa_targets += getFromNcbi setWeka cleanWeka
getFromNcbi_help = Download some data from NCBI
setWeka_help = set location in the global weka db
cleanWeka_help = clean location in the global weka db (will not run automatically)# Help

moa_ids += getFromNcbi
moa_title_getFromNcbi = Get sequences from NCBI
moa_description_getFromNcbi = Download a set of sequences from NCBI based on a \
  query string (ncbi_query) and database (ncbi_db). This will \
  run only once (!) unless you touch the 'touched' file.# Output definition

moa_outputs += fastafile
moa_output_fastafile = ./fasta/*.fasta
moa_output_fastafile_help = A set of fasta files#varables that NEED to be defined

moa_must_define += ncbi_db ncbi_query set_name
ncbi_db_help = NCBI database (for example nucest)
ncbi_query_help = NCBI query (for example txid9397[Organism%3Aexp])
set_name_help=Name of the set to download (used by the wekadb)

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################
.PHONY: getFromNcbi_prepare
getFromNcbi_prepare:
	-mkdir fasta

.PHONY: getFromNcbi_post
getFromNcbi_post:


getFromNcbi:  fasta_files

.PHONY: set_weka
setWeka:
	weka set $(set_name)::fastadir `pwd`/fasta

executed:
	touch executed.PHONY: fasta_files
fasta_files: tmp.fasta  
	cd fasta; seqretsplit -sequence ../tmp.fasta -outseq out.fasta
	cd fasta; for x in *.fasta ; do \
		name=`grep ">" $$x | head -1 | cut -c2- | cut -f1 -d' '`.fasta ;\
		mv $$x $$name ;\
	done

tmp.fasta: webEnv=$(shell xml_grep --cond "WebEnv" tmp.xml --text_only)
tmp.fasta: queryKey=$(shell xml_grep --cond "QueryKey" tmp.xml --text_only)
tmp.fasta: tmp.xml
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&rettype=fasta&retmode=text&usehistory=y" \
		-O tmp.fasta

#tmp.xml contains the IDs of the sequences to download
tmp.xml:
	-rm tmp.xml 
	-rm tmp.fasta 
	-rm fasta/*.fasta
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y" \
		-O tmp.xml

clean: get_from_ncbi_clean

get_from_ncbi_clean:
	-rm -r fasta
	-rm tmp.xml
	-rm tmp.fasta
	-rm executed

clean_weka:
	weka rm $(set_name)::fasta
