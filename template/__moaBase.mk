##
## Moabase - base library for all moa styled makefiles.
##
## Include this after all moa style definitions but before
## defining any target or (and this is important) any variable
## that depends on a variable defined in moa.mk
##

## we use bash!
SHELL := /bin/bash

## We use the Gnu Make Standard Library
## See: http://gmsl.sourceforge.net/
include $(shell echo $$MOABASE)/template/gmsl

## Load moa wide configuration
include $(shell echo $$MOABASE)/etc/moa.conf.mk

## some help variables
warn_on := \033[0;1;37;41;4;6m
warn_off := \033[0m

boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

#a colorful mark, showing that this comes from moabase
moamark := \033[0;41m \033[43m \033[42m \033[44m \033[45m \033[0m
echo = echo -e "$(moamark) $(1)"
errr = echo -e "$(moamark)$(warn_on) -- $(1) -- $(warn_off)"

## If moa.mk is defined, import it.
## moa.mk is used to store local variables

## Define number of processors to be used
MOA_PROCESSORS ?= 3

ifndef MOAMK_INCLUDE
-include ./moa.mk
MOAMK_INCLUDE=done
endif

## If not jid is defined, define one automatically here
jid ?= $(shell echo -n "moa_$(word 1 $,$(moa_ids))_"; \
			   echo -n `basename $$PWD`"_" ;\
			   echo "$$RANDOM" `pwd` `date` | md5sum | cut -c-12)

#ifeq ("$(call substr,$(jid),1,2)","__")
#jid ?= $(shell echo -n "moa_$(word 1 $,$(moa_ids))_"; \
#			   echo -n `basename $$PWD`"_" ;\
#			   echo "$$RANDOM" `pwd` `date` | md5sum | cut -c-12)
#endif

## moa default target - welcom, varcheck, prepare & post actions.
.DEFAULT_GOAL := moa_default_target
.PHONY: moa_default_target
moa_default_target: moa_welcome \
  moa_prepare_var \
  moa_preprocess \
  $(addsuffix _prepare, $(moa_ids)) \
  moa_main_targets \
  $(addsuffix _post, $(moa_ids)) \
  moa_postprocess \
  moa_register

#A list of all targets that can 'check' as valid.
#in other words, these targets can be used with
#   make all action=TARGET
moa_all_targets = $(call set_create, \
  set append clean register reset targets \
  $(addsuffix _prepare, $(moa_ids)) \
  check \
  $(moa_ids) \
  $(addsuffix _post, $(moa_ids)) )

.PHONY: targets
targets:
	@echo $(moa_all_targets)

moa_check_target:
	@echo $(moa_all_targets)
	@echo $(check)
	@if [ "$(call set_is_member, $(check), $(moa_all_targets))" == "$(true)" ];\
	  then \
	    echo "VALIDTARGET: $(check) is a valid target" ;\
	  else \
	    echo "NOTATARGET: $(check) is not a valid target" ;\
	fi

#the main targets - we run these as separate make instances
#since I really cannot Make to reevaluate what possible input
#files are inbetween steps
moa_main_targets:
	@for moa_main_target in $(moa_ids); do \
		$(call echo,calling $$moa_main_target) ;\
		$(MAKE) $$moa_main_target -j $(MOA_PROCESSORS) ;\
	done

execorder:
	@echo "moa_welcome"
	@echo "moa_preprocess"
	@echo "$(addsuffix _prepare, $(moa_ids))"
	@echo "moa_check"
	@echo "$(moa_ids)"
	@echo "$(addsuffix _post, $(moa_ids))"
	@echo "moa_postprocess"

moa_dummy:
	@echo "Targets to execute were"
	@echo "-----------------------"
	@echo moa_welcome moa_preprocess $(addsuffix _prepare, $(moa_ids)) \
	  moa_check $(moa_ids) \
	  $(addsuffix _post, $(moa_ids)) \
	  moa_postprocess


#override these if necessary
moa_preprocess:
moa_postprocess:

#each moa makefile should include a ID_clean target cleaning up after it..
#this one calls all cleans
.PHONY: clean
clean: $(call reverse, $(addsuffix _clean, $(moa_ids)))
	@echo "clean order $(clean_order)"

#display a welcome message
moa_welcome:
	@$(call echo, Welcome to MOA in $(shell pwd))


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
moa_may_define += jid 
name_help = A job id describing this project. No spaces! If this is not \
  defined, an autogenreated ID will be used.

moa_may_define += project 
name_help = A unique project name defining this job. Cannot have spaces.


##############################################################################
## Register this job usine Apache Couchdb
couchserver ?= 127.0.0.1:5984
couchdb ?= moa

## Define the function to get stuff from the couch db
cget = $(shell moacouch -d $(couchdb) -s $(couchserver) get $(1))

.PHONY: register
register: moa_register

.PHONY: moa_register
moa_register: moa_check_jid
	@$(call echo,Calling moa register. Couchdb server: $(couchserver))
	@moacouch -v -s $(couchserver) -d $(couchdb) register $(jid) \
		moa_ids="$(moa_ids)" pwd="`pwd`" date="`date`" \
		$(foreach v, $(moa_must_define), $(v)="$($(v))") \
		$(foreach v, $(moa_may_define), $(v)="$($(v))") \
		$(foreach v, $(moa_register_extra), $(v)=$(moa_register_$(v)))

moa_register_%:
	weka2 set moa.$(project).$(moa_main_id).$(name).$* $($*)

###################################################
## Moa check - is everything defined?


###########################################################################
#check prerequisites

prereqlist += prereq_moa_environment

.PHONY: prereqs $(prereqlist)
prereqs: $(prereqlist)

ter:
	$(call errr, Hello)

moa_check_lock:
	@if [ -f lock ]; then \
	    $(call errr, Job is locked!) ;\
	    exit 2 ; \
	fi

#check if MOABASE is defined
prereq_moa_environment:
	@if env | grep -q MOABASE ; then true; else \
		$(call errr, the environment variable MOABASE is not defined ) ;\
		false ;\
	fi

.PHONY: check
check: moa_prepare_var moa_check 

moa_var_checklist := $(addprefix checkvar_, $(moa_must_define))

.PHONY: moa_check
moa_check: moa_check_lock \
		   moa_check_jid prereqs $(moa_var_checklist)
	@$(call echo, Check - everything is fine)

#check if a job id is defined in moa.mk
.PHONY: moa_check_jid
moa_check_jid:
	@if ! grep -q "^jid" moa.mk; then \
		$(call echo,Storing jid="$(jid)" in moa.mk) ;\
		echo "jid=$(jid)" >> moa.mk ;\
	fi

.PHONY: checkvar_%
checkvar_%:
	@if [ "$(origin $(subst checkvar_,,$@))" == "undefined" ]; then \
		$(call errr, Error $(subst checkvar_,,$@) is undefined) ;\
		exit -1; \
	fi

# Set a variable!
.PHONY: set
set: set_mode =
set: set_prepare $(addprefix storevar_, $(moa_must_define) $(moa_may_define))

.PHONY: set_prepare
set_prepare:
	touch moa.mk

# or append
.PHONY: append
append: set_mode="+"
append: $(addprefix storevar_, $(moa_must_define) $(moa_may_define))


.PHONY: storevar_%
storevar_%:
	@#A regular value
	@if [ "$(origin $*)" == "command line" ]; then \
		mv moa.mk moa.mk.backup ;\
		cat moa.mk.backup | grep -v "^$* *[\+=]" > moa.mk ;\
		if [ ! "$$cval" == "-" ]; then \
			$(call echo, Set $* to '$($*)') ;\
			echo "$* $(set_mode)= $($*)" >> moa.mk ;\
		else \
			$(call echo, Removing $* from moa.mk) ;\
		fi ;\
	fi
	@#A couchdb value
	@if [ "$(origin c__$*)" == "command line" ]; then \
		$(call echo, set $* to couchdb: $(c.$*)) ;\
		mv moa.mk moa.mk.backup ;\
		cat moa.mk.backup \
			| grep -v "^$* *[\+=]" \
			| grep -v "^$*__couchdb *[\+=]" \
				> moa.mk ;\
		echo "$*__couchdb=$(call split,:,$(c__$*))" >> moa.mk ;\
	fi


.PHONY: show showvar_%
show: moa_prepare_var $(addprefix moa_showvar_, $(moa_must_define) $(moa_may_define))

moa_couch_filter = $(if $(call sne,$(origin $(1)__couchdb),undefined), $(1))

moa_prepare_vars = $(addprefix moa_prepvar_, \
					$(call map,moa_couch_filter, \
						$(moa_must_define) $(moa_may_define)))
.PHONY: moa_prepare_var
moa_prepare_var: $(moa_prepare_vars) 
	@#$(call echo,Called moa_prepare vars)
	@#$(call echo,  for $(moa_prepare_vars))

#.PHONY: $(moa_prepare_vars)
moa_prepvar_%: 
	@#$(call echo, Running moa_prepare_var $*)
	@#set the $* variable to the currenct couchdb val
	$(eval $*=$(call cget,$($*__couchdb)))
	@#store this in moa.mk as the actual value - this prevent
	@#prepvar having to be re-executed
	@if ! grep -q -E "^$*=$($*)$$" moa.mk; then \
		#$(call echo, Caching couchdb value $* in moa.mk) ;\
		mv moa.mk moa.mk.backup ;\
		cat moa.mk.backup \
			| grep -v "^$* *[\+=]" \
				> moa.mk ;\
		echo "$*=$(call cget,$($*__couchdb))" >> moa.mk ;\
	fi

moa_showvar_%:		 
	@echo -e "$*\t$($*)"



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
	@if [ "$(action)" == "" ]; then \
	  $(MAKE) ;\
	else \
	  if $(MAKE) moa_check_target check=$(action) | grep VALIDTARGET; \
	  then \
	    $(MAKE) $(action) ;\
	  else \
	    $(call errr, Ignoring $(action) - not valid in this context) ;\
	  fi \
	fi

.PHONY: $(moa_followups)
$(moa_followups):
	@if [[ -e $@/Makefile ]]; then \
		if [[ ! -e $@/lock ]]; then \
			$(call echo, Executing make $(action) in $@) ;\
			cd $@ && $(MAKE) all action=$(action) ;\
		else \
			$(call errr, Not going here : $@ is locked) ;\
		fi ; \
	fi


###############################################################################
# Help structure
.PHONY: help
help: moa_help_header \
	moa_help_target_header \
	moa_help_target \
	moa_help_target_footer \
	moa_help_vars_header \
	moa_help_vars \
	moa_help_vars_footer

.PHONY: moa_help_header
moa_help_header: \
	moa_help_header_title \
	moa_help_header_description

.PHONY: moa_help_header_title
moa_help_header_title:

#moa_description_LinkGather	
.PHONY: moa_help_header_description
moa_help_header_description: $(addprefix moa_help_header_description_, $(moa_ids))
	@echo

moa_help_header_description_%:
	@$(call echo, $(moa_title_$*))
	@echo -e "$(moa_description_$*)" | fold -w 70 -s 


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