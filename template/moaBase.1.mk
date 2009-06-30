##
## Moabase - base library for all moa styled makefiles.
##
## Include this after all moa style definitions but before
## defining any target or (and this is important) any variable
## that depends on a variable defined in moa.mk
##

## we use bash!
SHELL := /bin/bash

## some help variables
warn_on := \033[0;1;47;0;41;4;6m
warn_off := \033[0m

boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

## If moa.mk is defined, import it.
## moa.mk is used to store local variables
-include ./moa.mk

## moa default target - welcom, varcheck, prepare & post actions.
.DEFAULT_GOAL := moa_default_target
.PHONY: moa_default_target
moa_default_target: moa_welcome \
  $(addsuffix _prepare, $(moa_ids)) \
  moa_check $(moa_ids) \
  $(addsuffix _post, $(moa_ids))

# \
#  moa_register

#each moamakefile should include a ID_clean target cleaning up after it..
#this one calls all cleans
.PHONY: clean
clean: $(addsuffix _clean, $(moa_ids))

#display a welcome message
moa_welcome:
	@echo "Welcome to MOA"


# Add a few default targets to the set 
# of possible targets
moa_targets += check clean help show all prereqs set append

# and define help for these
check_help = Check variable definition
clean_helo = Clean up. 
show_help = Show the defined variables
help_help = This help!
all_help = Recursively run through all subdirectories (use make all \
  action=XXX to run "make XXX" recursively)
prereqs_help = Check if all prerequisites are present
set_help = set a variable to moa.mk
append_help = as set, but append the variable to a list.

#some default variable help defs
input_dir_help = Directory with the input data
input_extension_help = Extension of the input files

#prevent reinclusion of moabase
dont_include_moabase=defined

#each analysis MUST have a name
#Variable: set_name
moa_must_define += name 
name_help = A unique name defining this job. Cannot have spaces.

moa_must_define += project 
name_help = A unique project name defining this job. Cannot have spaces.

moa_register: moa_main_id = $(firstword $(moa_ids))
moa_register: $(addprefix moa_register_, $(moa_must_define)) \
  $(addprefix moa_register_, $(moa_may_define))
	weka2 set moa.$(project).$(moa_main_id).$(moa_ids).$(name).pwd $(shell pwd)
	weka2 set moa.$(project).$(moa_main_id).$(name).time "$(shell date)"

moa_register_%:
	weka2 set moa.$(project).$(moa_main_id).$(name).$* $($*)

###################################################
## Moa check - is everything defined?


###########################################################################
#check prerequisites

prereqlist += prereq_moa_environment

.PHONY: prereqs $(prereqlist)
prereqs: $(prereqlist)

moa_check_lock:
	@if [ -f lock ]; then \
	    echo -e "$(warn_on)Job is locked! won't execute. Remove the lock file$(warn_off)" ;\
	    exit 2 ; \
	fi

#check if MOABASE is defined
prereq_moa_environment:
	@if env | grep -q MOABASE ; then true; else \
		echo "MOABASE is not defined :(" ; \
		false ;\
	fi

.PHONY: check
check: moa_check 

moa_var_checklist :=  $(addprefix checkvar_, $(moa_must_define))

.PHONY: moa_check
moa_check: moa_check_lock prereqs $(moa_var_checklist)
	@echo "Checked: everything appears ok"

#.PHONY: checkvar_ncbi_db
checkvar_%:
	@if [ "$(origin $(subst checkvar_,,$@))" == "undefined" ]; then \
		echo " *** Error $(subst checkvar_,,$@) is undefined" ;\
		exit -1; \
	fi

# Set a variable!
.PHONY: set
set: set_mode =
set: $(addprefix storevar_, $(moa_must_define) $(moa_may_define))

# or append
.PHONY: append
append: set_mode="+"
append: $(addprefix storevar_, $(moa_must_define) $(moa_may_define))

.PHONY: storevar_%
storevar_%:
	@if [ "$(origin $(subst storevar_,,$@))" == "command line" ]; then \
		echo " *** Set $(subst storevar_,,$@) to $($(subst storevar_,,$@))" ;\
		echo "$(subst storevar_,,$@)$(set_mode)=$(set_mode)$($(subst storevar_,,$@))" >> moa.mk ;\
	fi
	@if [ "$(origin weka_$(subst storevar_,,$@))" == "command line" ]; then \
		echo " *** Set $(subst storevar_,,$@) to \"weka get $(weka_$(subst storevar_,,$@))\"" ;\
		echo -n "$(subst storevar_,,$@)$(set_mode)=$$" >> moa.mk ;\
		echo "(shell weka get $(weka_$(subst storevar_,,$@)))" >> moa.mk ; \
	fi

.PHONY: show showvar_%
show: $(addprefix showvar_, $(moa_must_define) $(moa_may_define))

showvar_%:		 
	@echo "$(subst showvar_,,$@) : $($(subst showvar_,,$@))"
# Traversal through subdirectories.

# by calling 'make all', all subdirs are made as well as the cd.As an extension,
# calling 'make all action=clean' calss make clean in the cd and all subdirs.
# action= can be replace by other actions. An interesting application is
# to set/change variables through a whole tree using:

# make all action=set KEY=VALUE

# The the variable KEY will be set to VALUE in this dir and all subdirs, but only
# when KEY is a defined variable for that moa-makefile


moa_followups ?= $(shell find . -maxdepth 1 -type d -regex "\..+" -exec basename '{}' \; | sort -n )

.PHONY: all
all: traverse_start_here $(moa_followups)

#start with executing ourselves.. we run make again with $(action) as target. If $(action)
#is not defined, it's just "make".
.PHONY: traverse_start_here
traverse_start_here:
	$(MAKE) $(action)

.PHONY: $(moa_followups)
$(moa_followups):
	@if [[ -e $@/Makefile ]]; then \
		if [[ ! -e $@/lock ]]; then \
			echo -e "\033[43;30;6m#### Executing make $(action) in $@ \033[0m"  ;\
			cd $@ && $(MAKE) all action=$(action) ;\
		else \
			echo -e "$(warn_on) in $@ is locked$(warn_off)" ;\
		fi ; \
	fi

#print a status report: / not full implemted yet!
moa_status_reports = $(addprefix status_, $(moa_ids))
.PHONY: status $(moa_status_reports)

status: status_start $(moa_status_reports)

status_start:
	@echo "Status reports: $(moa_status_reports)"
###############################################################################
# Help structure
help: moa_help_header \
	moa_help_deprecated \
	moa_help_target_header moa_help_target moa_help_target_footer \
	moa_help_vars_header moa_help_vars moa_help_vars_footer \
	moa_help_output_header moa_help_output moa_help_output_footer

moa_help_header: moa_help_header_title moa_help_header_description

moa_help_header_title: moa_title_list = $(foreach x, $(moa_ids),$(moa_title_$(x)) &)
moa_help_header_title: moa_all_title = $(wordlist 1, $(shell expr $(words $(moa_title_list)) - 1), $(moa_title_list))
moa_help_header_title:
	@echo "($(moa_ids))"
	@echo -n "=="
	@echo -n "$(moa_all_title)" | sed "s/./=/g"
	@echo "=="
	@echo -e "= $(bold_on)$(moa_all_title)$(bold_off) ="
	@echo -n "=="
	@echo -n "$(moa_all_title)" | sed "s/./=/g"
	@echo "=="

#moa_description_LinkGather	
moa_help_header_description: $(addprefix moa_help_header_description_, $(moa_ids))
	@echo

moa_help_header_description_%:	
	@echo -e "$(bold_on)$(moa_title_$(patsubst moa_help_header_description_%,%,$@)):$(bold_off)"
	@echo -e "$(moa_description_$(patsubst moa_help_header_description_%,%,$@))" | fold -w 70 -s 


moa_help_deprecated: $(addprefix moa_help_deprecated_, $(moa_ids))

moa_help_deprecated_%:
	@if [ -n "$(moa_deprecated_$*)" ]; then \
		echo -e "$(warn_on)*** There is a newer version of: $* *** $(warn_off)" ;\
	fi		

## Help - target section
moa_help_target_header:
	@echo -e "$(bold_on)Targets$(bold_off)"
	@echo "======="

moa_help_target: $(addprefix moa_target_, $(moa_targets))


moa_target_%:
	@if [ "$(origin $(subst moa_target_,,$@)_help)" == "undefined" ]; then \
		echo -e " - $(bold_on)$(subst moa_target_,,$@)$(bold_off)" ;\
	else \
		echo -e " - $(bold_on)$(subst moa_target_,,$@)$(bold_off): $($(subst moa_target_,,$@)_help)" \
			| fold -w 60 -s |sed '2,$$s/^/     /' ;\
	fi


moa_help_target_footer:
	@echo 

## Help - variable section
moa_help_vars_header:
	@echo -e "$(bold_on)Variables$(bold_off)"
	@echo "========="

moa_help_vars_footer:
	@echo -e "*these variables $(bold_on)must$(bold_off) be defined"
	@echo 

moa_help_vars: moa_help_vars_must moa_help_vars_may

moa_help_vars_must: help_prefix="*"
moa_help_vars_must: $(addprefix helpvar_, $(moa_must_define))

moa_help_vars_may: help_prefix=""
moa_help_vars_may: $(addprefix helpvar_, $(moa_may_define))

helpvar_%:	
	@if [ "$(origin $(subst helpvar_,,$@)_help)" == "undefined" ]; then \
		echo -en " - $(bold_on)$(help_prefix)$(subst helpvar_,,$@)$(bold_off)" ;\
	else \
		echo -e " - $(bold_on)$(help_prefix)$(subst helpvar_,,$@)$(bold_off): $($(subst helpvar_,,$@)_help)" \
			| fold -w 60 -s | sed '2,$$s/^/     /' ;\
	fi



## Help - output section
moa_help_output_header:
	@echo -e "$(bold_on)Outputs$(bold_off)"
	@echo "======="

moa_help_output: $(addprefix moa_output_, $(moa_outputs))

moa_output_%:	
	@if [ "$(origin $@_help)" == "undefined" ]; then \
		echo -e "- $(bold_on)$(subst moa_output_,, $@):$(bold_off) $($@)" ;\
	else \
		echo -e "- $(bold_on)$(subst moa_output_,, $@):$(bold_off) $($@) - $($(subst helpvar_,,$@)_help)" \
			 |fold -w 60 -s |sed '2,$$s/^/     /' ;\
	fi

moa_help_output_footer:
	@echo 


#%::
#	@echo -e "$(warn_on)NOTARGET!$(warn_off) Target $@ does not exist"