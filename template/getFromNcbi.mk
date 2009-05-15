# Download a set of sequences from NCBI

# Main target - should be first in the file
moa_main_target: check get_from_ncbi set_weka


################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += get_from_ncbi set_weka clean clean_weka
get_from_ncbi_help = Download data from NCBI
set_weka_help = set location in the global weka db
clean_help = remove the downloaded data
clean_weka_help = clean location in the global weka db (will not run automatically)

# Help
moa_title = Get sequences from NCBI
moa_description = Download a set of sequences from NCBI based on a \
	query string (ncbi_query) and database (ncbi_db). This will \
	run only once (!) unless you touch the 'touched' file.

# Output definition
moa_outputs += fastafile
moa_output_fastafile = ./setname.fasta
moa_output_fastafile_help = The multi-fasta file with the downloaded sequence

#varables that NEED to be defined
moa_must_define += set_name ncbi_db ncbi_query
set_name_help = The name of the set, used to name the output fasta file
ncbi_db_help = NCBI database (for example nucest)
ncbi_query_help = NCBI query (for example txid9397[Organism%3Aexp])

#variables that may be defined
moa_may_define += fasta_file
fasta_file_help = Name of the fasta file to save the results to

#Include base moa code - does variable checks & generates help
ifneq $(include_moa_base) "no"
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################
# End of the generic part - from here on you're on your own :)

fasta_file ?= $(set_name).fasta

#default name of the fasta file

get_from_ncbi: get_from_ncbi_prepare $(fasta_file) 

get_from_ncbi_prepare:
	# check if touchfile exists. If not.. create it
	if [ ! -f touched ]; then \
		touch touched; \
	fi

set_weka:
	weka set $(set_name)::fasta `pwd`/$(fasta_file)
	
$(fasta_file): webEnv=$(shell xml_grep --cond "WebEnv" tmp.xml --text_only)
$(fasta_file): queryKey=$(shell xml_grep --cond "QueryKey" tmp.xml --text_only)
$(fasta_file): tmp.xml
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&rettype=fasta&retmode=text&usehistory=y" \
		-O $@
	
tmp.xml: touched
	wget "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y" \
		-O tmp.xml

clean: get_from_ncbi_clean

get_from_ncbi_clean:
	-rm $(fasta_file)
	-rm tmp.xml
	-rm touched
	
clean_weka:
	weka rm $(set_name)::fasta