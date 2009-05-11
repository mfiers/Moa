# Perform a set of standardized operations on or with sequences
#
# Actions defined here are (and the variables that need to be defined)
#
#   - create_blast_db: 
#		- set_name
#   - download (lftp): 
#		- set_name uri 
#   - concatenate a set of files into one: 
#		- set_name
#		- input_dir
#		- input_glob
#   - get_from_ncbi: 
#		- set_name
#		- ncbi_db
#		- ncbi_query
#   - repeatmask: 
#		- set_name
#		- input_dir
#		- input_glob
#
# Parameters:
#   - set_name: Base name of this set. Must be defined!
#   - fasta_file: The base fasta file containing all sequences (defaults to
#       '$(set_name).fasta'
#   - protein: Is this a set of proteins (T) or not (F, default)
#   - input_dir: where to get sequences from (if applicable, defaults to
#       './fasta'
#   - input_glob: filename of the sequences (defaults to '*.fasta')
#   - ncbi_db: the ncbi db to query (when using get_from_ncbi)
#   - ncbi_query: the query to send to ncbi (when using get_from_ncbi)
#
# Definitions, prerequisites and conditions
#   - a set_name must be defined!
#   - If this concerns protein sequences set "protein = T". Default is
#     nucleotides (protein = F). Obviously some actions do not apply
#     to proteins
#   - if a corresponding fasta file is required the name will allways be:
#       ./$(setname).fasta (for example, for concatenate

################################################################################
# Variable checks
ifeq ($(origin set_name), undefined)
$(error You must define the variable set_name)
endif

#The rest of the vars are not obligatory.. We could add other checks
#in makefiles inheriting from this one.

#default name of the fasta file
fasta_file ?= $(set_name).fasta

#is the protein variable defined? If not, set it to F
protein ?= F

#default input dir and glob
input_dir ?= ./fasta
input_glob ?= *.fasta

#if not defined, the ncbi database is set to nucest and the query retrieves
#all ests from bats... (that'll teach you to set the parameters :))
ncbi_db ?= nucest
ncbi_query ?= txid9397[Organism%3Aexp]

################################################################################
# Command definiton

main_help:
	@echo "Please read the template makefile for help"
	exit 1

###############################################################################
# Create blast db
create_blast_db:
	formatdb -i $(fasta_file) -p $(protein) -o T -n $(set_name)
	sdbset $(set_name).blastdb `pwd`/$(set_name)

###############################################################################
# Concatenate
concatenate:
	-rm $(fasta_file)
	find $(input_dir) -name '$(input_glob)' -exec cat {} \; > $(fasta_file)

###############################################################################
# Concatenate	
get_from_ncbi: get_from_ncbi_1 get_from_ncbi_2

get_from_ncbi_1: ncbi_url_1 = http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=$(ncbi_query)&db=$(ncbi_db)&retmax=1000000&usehistory=y 
get_from_ncbi_1:
	-rm $(fasta_file)
	-rm _tmp.xml
	wget '$(ncbi_url_1)' \
		-O _tmp.xml

get_from_ncbi_2: webEnv=$(shell xml_grep --cond "WebEnv" _tmp.xml --text_only)
get_from_ncbi_2: queryKey=$(shell xml_grep --cond "QueryKey" _tmp.xml --text_only)
get_from_ncbi_2: ncbi_url_2=http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=$(ncbi_db)&WebEnv=$(webEnv)&query_key=$(queryKey)&rettype=fasta
get_from_ncbi_2:
	wget '$(ncbi_url_2)' \
		-O $(fasta_file)
	-rm _tmp.xml

clean: clean_create_blast_db clean_concatenate

clean_create_blast_db:
	-rm $(set_name).nhr $(set_name).nin $(set_name).nsd $(set_name).nsi \
		$(set_name).nsq $(set_name).phr $(set_name).pin $(set_name).psd \
		$(set_name).psi $(set_name).psq

clean_concatenate:
	-rm $(fasta_file)