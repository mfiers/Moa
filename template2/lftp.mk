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

# Help
moa_id = lftp

include $(MOABASE)/lib/gnumake/core.mk

ifdef lftp_user
ifdef lftp_pass
	lftp_auth = -u $(lftp_user),$(lftp_pass)
	curl_auth = -u '$(lftp_user):$(lftp_pass)'
else
	lftp_auth = -u $(lftp_user)
	curl_auth = -u $(lftp_user)
endif
endif

#download files using LFTP
.PHONY: lftp_prepare
lftp_prepare:
	if [[ "$(lftp_output_dir)" != "." ]]; then	\
		mkdir $(lftp_output_dir) || true;		\
	fi

lftp: fexcl=$(addprefix -not -name , $(lftp_noclean))
lftp: lftp_$(lftp_mode) lftp_dos2unix

.PHONY: lftp_mirror
lftp_mirror:
	cd $(lftp_output_dir); \
		echo lftp $(lftp_auth) $(lftp_url) -e "mirror -nrL -I $(lftp_url)/$(lftp_pattern); exit" ; \
		lftp $(lftp_auth) $(lftp_url) -e "mirror -nrL -I $(lftp_url)/$(lftp_pattern); exit" ;
	if [ "$(lftp_lock)" == "T" ]; then touch lock ; fi

.PHONY: lftp_get
lftp_get: _addcl=$(if $(lftp_get_name),-o $(lftp_get_name))
lftp_get: _server=$(shell echo "$(lftp_url)" | sed -r "s|(http[s]?:\/\/)?([^ \/]*)\/.*$$|\2|")
lftp_get:
	$e $(call echo,Getting data from server $(_server))
	$e cd $(lftp_output_dir);									\
		for xx in $(lftp_url); do								\
			echo curl -Ok $(curl_auth) "$$xx" ;\
			curl -Ok $(curl_auth) "$$xx";\
		done
	$e if [ "$(lftp_lock)" == "T" ]; then touch lock ; fi

.PHONY: lftp_dos2unix
lftp_dos2unix:
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

################################################################################
## Test fixture
################################################################################
.PHONY: unittest_lftp
unittest_lftp:
	@$(call moa_unittest_var,title,lftp unittest new title)
	@$(call moa_unittest_var,lftp_output_dir,out)
	@$(call moa_unittest_var,lftp_lock,T)
	@$(call moa_unittest_var,lftp_timestamp,F)
	@$(call moa_unittest_var,lftp_powerclean,F)
	@$(call moa_unittest_var,lftp_dos2unix,F)
	@$(call moa_unittest_var,lftp_mode,get)
	@$(call moa_unittest_var,lftp_url,ftp://ftp.arabidopsis.org/Sequences/blast_datasets/README)
	moa
	@$(call moa_unittest_direxists,out/)
	@$(call moa_unittest_fileexists,out/README)
	moa clean
	@$(call moa_unittest_filenotexists,out/README)
	@$(call moa_unittest_dirnotexists,out/)
	ls -Rl
