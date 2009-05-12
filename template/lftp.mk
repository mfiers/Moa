# lftp a set of files

# Main target - should be first in the file
moa_main_target: check lftp

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += lftp clean
lftp_help = Download using ftp
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_title = LFTP
moa_description = use lftp to download a (set of) file(s). This makefile does not \
employ a touchfile since lftp checks for updates before downloading.

# Output definition
moa_outputs += lftp_output
moa_output_lftp_output = ./*
moa_output_lftp_output_help = Anything you define to be downloaded

#varables that NEED to be defined
moa_must_define += lftp_url lftp_pattern
lftp_url_help = The base url to download from
lftp_pattern_help = glob pattern to download

#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################


#download files using LFTP 
lftp: lftp_prepare
    lftp $(lftp_url) -e "mirror -nrL -I $(lftp_pattern); exit"
    -for x in *gz; do \
        gunzip -c $$x > `basename $$x .gz`; \
    done

set_weka:
	weka set $(set_name)::fasta `pwd`/$(fasta_file)

clean: get_from_ncbi_clean

get_from_ncbi_clean:
	-rm $(fasta_file)
	-rm tmp.xml
	-rm touched
	
clean_weka:
	weka rm $(set_name)::fasta