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
moa_ids += lftp
moa_title_lftp = lftp
moa_description_lftp = use lftp to download a (set of) file(s). This makefile does not \
  employ a touchfile since lftp checks for updates before downloading.

# Output definition
moa_outputs += lftp_output
moa_output_lftp_output = *
moa_output_lftp_output_help = anything you define

#varables that NEED to be defined
moa_must_define += lftp_url lftp_pattern
lftp_url_help = The base url to download from
lftp_pattern_help = glob pattern to download

#variables that may be defined
moa_may_define += depend_lftp_timestamp
depend_lftp_timestamp_help = Depend on lftp to decide if a file needs updating, \
 else a touchfile is created that you need to delete or touch before updating \
 (T/*F*)
 
moa_may_define += lftp_user lftp_pass
lftp_user_help = username for the remote site
lftp_pass_help = password for the remote site, note that this can be defined on \
  the commandline using: 'make lftp_pass=PASSWORD'

moa_may_define += output_dir run_dos2unix
output_dir_help = subdir to create & write all output to. If not defined, data \
  will be downloaded to directory containing the Makefile
run_dos2unix_help = (T/F) Run dos2unix to prevent problems with possible dos text \
  files (default=F).
  
#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################
depend_lftp_timestamp ?= T
lftp_user ?= NoNoNo
lftp_pass ?= NoNoNo
lftp_noclean ?= Makefile moa.mk 
output_dir ?= .
run_dos2unix ?= F

#download files using LFTP
.PHONY: lftp lftp_prepare
 
lftp: lftp_prep lftp_run

lftp_prep:
	-if [ "$(depend_lftp_timestamp)" == "T" ]; then rm lftp_run; fi
	-if [ ! "$(output_dir)" == "." ]; then mkdir $(output_dir); fi
	
lftp_run: fexcl=$(addprefix -not -name , $(lftp_noclean))
lftp_run:
	if [ "$(lftp_user)" == "NoNoNo" ]; then \
		cd $(output_dir); lftp $(lftp_url) -e "mirror -nrL -I $(lftp_pattern); exit" ;\
	else \
		cd $(output_dir); lftp -u $(lftp_user),$(lftp_pass) $(lftp_url) \
			 -e "mirror -nrL -I $(lftp_pattern); exit" ;\
	fi	
	if [ "$(depend_lftp_timestamp)" == "F" ]; then \
		touch lftp_run ;\
	fi
	if [ "$(run_dos2unix)" == "T" ]; then \
		find . -type f $(fexcl) | xargs -n 100 dos2unix -k ;\
	fi		
	
clean: lftp_clean

lftp_clean: fexcl=$(addprefix -not -name , $(lftp_noclean))
lftp_clean:
	if [ ! "$(output_dir)" == "." ]; then rm -rf $(output_dir); done
	for x in `find . -maxdepth 1 -type f $(fexcl)`; do \
		rm $$x ;\
	done
	