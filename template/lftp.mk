#
#    Copyright 2009 Mark Fiers
#
#    This file is part of Moa 
#
#    Moa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Moa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Moa.  If not, see <http://www.gnu.org/licenses/>.
#
#    See: http://github.com/mfiers/Moa/
## lftp a set of files

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += lftp
lftp_help = Download using ftp

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
moa_may_define += lftp_timestamp lftp_powerclean lftp_noclean
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
lftp_mode_help = Mode of operation - "mirror" or "get". Mirror enables \
  timestamping. Get just gets a single file. If using get, consider setting \
  depend_lftp_timestamp to F. When using "get", the full url should be in \
  lftp_url. lftp_pattern is ignored. Defaults to mirror.

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################
lftp_timestamp ?= T
lftp_powerclean ?= F
lftp_user ?= NoNoNo
lftp_pass ?= NoNoNo
lftp_mode ?= mirror
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
	cd $(lftp_output_dir); \
	if [ "$(lftp_user)" == "NoNoNo" ]; then \
		if [ "$(lftp_mode)" == "mirror" ]; then \
			lftp $(lftp_url) -e "mirror -nrL -I $(lftp_pattern); exit" ;\
		else \
			echo lftp -e "get `urlsplit $(lftp_url) path`; exit" `urlsplit $(lftp_url) start` ;\
			lftp -e "get `urlsplit $(lftp_url) path`; exit" `urlsplit $(lftp_url) start` ;\
		fi ;\
	else \
		if [ "$(lftp_mode)" == "mirror" ]; then \
			lftp -u $(lftp_user),$(lftp_pass) $(lftp_url) \
				 -e "mirror -nrL -I $(lftp_pattern); exit" ;\
		else \
			echo "### lftp -u $(lftp_user),$(lftp_pass) -e "get `urlsplit $(lftp_url) path`; exit" `urlsplit $(lftp_url) start` ";\
			lftp -u $(lftp_user),$(lftp_pass) -e "get `urlsplit $(lftp_url) path`; exit" `urlsplit $(lftp_url) start` ;\
		fi ;\
	fi
	if [ "$(lftp_timestamp)" == "F" ]; then \
		touch lftp ;\
	fi
	if [ "$(run_dos2unix)" == "T" ]; then \
		find . -type f $(fexcl) | xargs -n 100 dos2unix -k ;\
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
