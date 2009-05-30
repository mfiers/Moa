SHELL := /bin/bash

.PHONY: set show help check prereqs

# If moa.mk is defined, import it.
# moa.mk is used to store local variables
-include moa.mk

# Add a few default targets to the set 
# of possible targets
moa_targets += check help show all clean_all prereqs

# and define help for these
check_help = Check variable definition
show_help = show defined variables
help_help = This help!
all_help = Recursively run through all subdirectories (use make all \
  action=XXX to run "make XXX" recursively)
prereqs_help = Check if all prerequisites are present

#some default variable help defs
input_dir_help = Directory with the input data
input_extension_help = Extension of the input files

#prevent reinclusion of moabase
dont_include_moabase=defined
###################################################
## Moa check - is everything defined?


###########################################################################
#check prerequisites

prereqlist += prereq_moa_environment
.PHONY: prereqs $(prereqlist)

prereqs: $(prereqlist)

#check if MOABASE is defined
prereq_moa_environment:
	@if env | grep -q MOABASE ; then true; else \
		echo "MOABASE is not defined :(" ; \
		false ;\
	fi
#check if this moa makefile is deprecated
moa_help_deprecated_%:
	#echo depreation check $*
	@if [ -n "$*" ]; then \
		echo -e "\033[0;1;47;0;41;4;6m *** There is a newer version of: $* *** \033[0m" ;\
	fi
.PHONY: check
check: prereqs $(addprefix checkvar_, $(moa_must_define)) moa_help_deprecated
	@echo "Variable check: everything appears ok"

#.PHONY: $(addprefix checkvar_, $(moa_must_define))
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

.PHONY: $(moa_followups) all clean_all

all_check:
	@echo "would run make $(action)"
	@echo "in the following dirs"
	@echo $(moa_followups)

#action ?= undefined
all: traverse_start_with_this $(moa_followups)

traverse_start_with_this:
	#if [ "$(action)" == "undefined" ]; then \
	#	echo "running all without action, also run default action" ;\
	#	$(MAKE) ;\
	#fi
    #run the required action in this directory
	-$(MAKE) $(action)
	@echo "Following up with:" $(moa_followups)

$(moa_followups):
	@echo "  ###########################"
	@echo "  ## Executing make $(action)"
	@echo "  ##   in $@ " 
	@echo "  ###########################"
	@if [ -e $@/Makefile ]; then \
		cd $@ && $(MAKE) all action=$(action) ;\
	fi
###############################################################################
# Help structure
boldOn = \033[0;1;47;0;32;4m
boldOff = \033[0m
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
	@echo -e "= $(boldOn)$(moa_all_title)$(boldOff) ="
	@echo -n "=="
	@echo -n "$(moa_all_title)" | sed "s/./=/g"
	@echo "=="

#moa_description_LinkGather	
moa_help_header_description: $(addprefix moa_help_header_description_, $(moa_ids))
	@echo

moa_help_header_description_%:	
	@echo -e "$(boldOn)$(moa_title_$(patsubst moa_help_header_description_%,%,$@)):$(boldOff)"
	@echo -e "$(moa_description_$(patsubst moa_help_header_description_%,%,$@))" | fold -w 70 -s 


moa_help_deprecated: $(addprefix moa_help_deprecated_, $(moa_ids))

moa_help_deprecated_%:
	@if [ -n "$(moa_deprecated_$*)" ]; then \
		echo -e "\033[0;1;47;0;41;4;6m *** There is a newer version of: $* *** \033[0m" ;\
	fi		

## Help - target section
moa_help_target_header:
	@echo -e "$(boldOn)Targets$(boldOff)"
	@echo "======="

moa_help_target: $(addprefix moa_target_, $(moa_targets))


moa_target_%:
	@if [ "$(origin $(subst moa_target_,,$@)_help)" == "undefined" ]; then \
		echo -e " - $(boldOn)$(subst moa_target_,,$@)$(boldOff)" ;\
	else \
		echo -e " - $(boldOn)$(subst moa_target_,,$@)$(boldOff): $($(subst moa_target_,,$@)_help)" \
			| fold -w 60 -s |sed '2,$$s/^/     /' ;\
	fi


moa_help_target_footer:
	@echo 

## Help - variable section
moa_help_vars_header:
	@echo -e "$(boldOn)Variables$(boldOff)"
	@echo "========="

moa_help_vars_footer:
	@echo -e "*these variables $(boldOn)must$(boldOff) be defined"
	@echo 

moa_help_vars: moa_help_vars_must moa_help_vars_may

moa_help_vars_must: help_prefix="*"
moa_help_vars_must: $(addprefix helpvar_, $(moa_must_define))

moa_help_vars_may: help_prefix=""
moa_help_vars_may: $(addprefix helpvar_, $(moa_may_define))

helpvar_%:	
	@if [ "$(origin $(subst helpvar_,,$@)_help)" == "undefined" ]; then \
		echo -en " - $(boldOn)$(help_prefix)$(subst helpvar_,,$@)$(boldOff)" ;\
	else \
		echo -e " - $(boldOn)$(help_prefix)$(subst helpvar_,,$@)$(boldOff): $($(subst helpvar_,,$@)_help)" \
			| fold -w 60 -s | sed '2,$$s/^/     /' ;\
	fi



## Help - output section
moa_help_output_header:
	@echo -e "$(boldOn)Outputs$(boldOff)"
	@echo "======="

moa_help_output: $(addprefix moa_output_, $(moa_outputs))

moa_output_%:	
	@if [ "$(origin $@_help)" == "undefined" ]; then \
		echo -e "- $(boldOn)$(subst moa_output_,, $@):$(boldOff) $($@)" ;\
	else \
		echo -e "- $(boldOn)$(subst moa_output_,, $@):$(boldOff) $($@) - $($(subst helpvar_,,$@)_help)" \
			 |fold -w 60 -s |sed '2,$$s/^/     /' ;\
	fi


moa_help_output_footer:
	@echo 
