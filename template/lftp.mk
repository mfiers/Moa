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
moa_title = lftp
moa_description = Use LFTP to download files. This template has two		\
  modi, one is set 'lftp_mode' to 'mirror' data, in which case both		\
  'lftp_url' and 'lftp_pattern' (default *) are used. The other modus	\
  is 'lftp_mode=get', when one file defined by 'lftp_url' is			\
  downloaded. In the mirror mode it is possible to download only those	\
  files that are newer as the files already downloaded by using the		\
  'lftp_timestamp' parameter

lftp_help = Download using ftp

# Help
moa_ids += lftp
lftp_help = execute the download

# Output definition
moa_outputs += lftp_output
moa_output_lftp_output = *
moa_output_lftp_output_help = anything you define

#varables that NEED to be defined
moa_must_define += lftp_url
lftp_url_help = The base url to download from

#variables that may be defined
moa_may_define += lftp_timestamp lftp_powerclean lftp_noclean lftp_pattern
lftp_pattern_help = glob pattern to download
lftp_timestamp_help = Depend on lftp to decide if a file needs updating, \
 else a touchfile is created that you need to delete or touch before updating \
 (T/*F*)
lftp_powerclean_help = Do brute force cleaning (T/F). Remove all files, \
  except moa.mk & Makefile when calling make clean. Defaults to F.
lftp_noclean_help = set of files not to be deleted by the powerclean

moa_may_define += lftp_user lftp_pass
lftp_user_help = username for the remote site
lftp_pass_help = password for the remote site, note that this can be \
  defined on the commandline using: 'make lftp_pass=PASSWORD'

moa_may_define += lftp_output_dir lftp_dos2unix
lftp_output_dir_help = subdir to create & write all output to. If not defined, \
  data will be downloaded to directory containing the Makefile
lftp_dos2unix_help = (T/F) Run dos2unix to prevent problems with possible dos \
  text files (default=F).

moa_may_define += lftp_mode
lftp_mode_help = Mode of operation - 'mirror' or 'get'. Mirror enables \
  timestamping. Get just gets a single file. If using get, consider setting \
  depend_lftp_timestamp to F. When using 'get', the full url should be in \
  lftp_url. lftp_pattern is ignored. Defaults to mirror.

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################
lftp_timestamp ?= T
lftp_powerclean ?= F

ifdef lftp_pattern
	lftp_mode = mirror
else
	lftp_mode = get
endif 

lftp_noclean +=  Makefile moa.mk 
lftp_output_dir ?= .
run_dos2unix ?= F

#download files using LFTP
.PHONY: lftp_prepare
lftp_prepare:
	-if [ "$(lftp_timestamp)" == "T" ]; then rm lftp; fi
	-mkdir $(lftp_output_dir)

lftp: fexcl=$(addprefix -not -name , $(lftp_noclean))
lftp:
	cd $(lftp_output_dir); 														\
	if [ -z "$(lftp_user)" ]; then 												\
		if [ "$(lftp_mode)" == "mirror" ]; then 								\
			lftp $(lftp_url) -e "mirror -nrL -I $(lftp_pattern); exit" ;		\
		else 																	\
			lftp -e "get $(lftp_url); exit";									\
		fi ;																	\
	else 																		\
		if [ "$(lftp_mode)" == "mirror" ]; then 								\
			lftp -u $(lftp_user),$(lftp_pass) $(lftp_url) 						\
				 -e "mirror -nrL -I $(lftp_pattern); exit" ;					\
		else 																	\
			lftp -u $(lftp_user),$(lftp_pass) -e "get $(lftp_url); exit";		\
		fi ;																	\
	fi
	if [ "$(lftp_timestamp)" == "F" ]; then 									\
		touch lftp ;															\
	fi
	if [ "$(run_dos2unix)" == "T" ]; then 										\
		find . -type f $(fexcl) | xargs -n 100 dos2unix -k ;					\
	fi

.PHONY: lftp_post
lftp_post:

lftp_clean: find_exclude_args = $(foreach v, $(lftp_noclean), -not -name $(v))
lftp_clean:
	@echo "start lftp_clean"
	if [ ! "$(lftp_output_dir)" == "." ]; then rm -rf $(lftp_output_dir); fi
	-rm lftp
	if [ "$(lftp_powerclean)" == "T" ]; then \
		find . -maxdepth 1 -type f $(find_exclude_args) \
			| xargs -n 20 rm -f ;\
	fi
