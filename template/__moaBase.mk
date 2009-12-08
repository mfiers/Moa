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
###############################################################################
# Variable definition - pre moa.mk include
#
## define all variables here that are not depending on moa.mk
###############################################################################

SHELL := /bin/bash

## We use the Gnu Make Standard Library
## See: http://gmsl.sourceforge.net/
include $(shell echo $$MOABASE)/template/gmsl

## Load moa wide configuration
include $(shell echo $$MOABASE)/etc/moa.conf.mk

## Files that moa uses
moa_system_files = Makefile moa.mk moa.archive 

## some help variables
warn_on := \033[0;41;37m
warn_off := \033[0m
boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

#a colorful mark, showing that this comes from moabase
moamark := \033[0;42;30mm\033[0m
moaerrr := \033[0;1;37;41m!!!\033[0m
moawarn := \033[0;43m>>\033[0m
echo = echo -e "$(moamark) $(1)"
warn = echo -e "$(moawarn) $(1)"
errr = echo -e "$(moaerrr) $(1)"
exer = echo -e "$(moaerrr) $(1)"; exit -1


## default variables used in generating help

## Pandoc is used widely to convert to & from documentation
## formats. A pandoc version >= v1.2 is recomended.
pandocbin?=$(shell which pandoc)


#pre & postprocess targets. these need to be overridden
.PHONY: moa_preprocess moa_postprocess
moa_preprocess:
moa_postprocess:

## aditional  pre/post process command - to be definable in moa.mk
## this is only one single command.
moa_may_define += moa_precommand
moa_precommand_help = A single command to be executed before the main			\
operation starts. For more complicated processing, please override the			\
moa_preprocess target in the local Makefile.
moa_precommand_type = string
moa_precommand_category = advanced

moa_may_define += moa_postcommand
moa_postcommand_help = A single shell command to be executed after the			\
Moa is finished. For more complex processing please override the				\
moa_postprocess target in the local Makefile.
moa_postcommand_category = advanced
moa_postcommand_type = string

.PHONY: moa_run_precommand
moa_run_precommand:
	@if [ "$(moa_precommand)" ]; then 										\
		$(call echo, Running precommand); 									\
		$(call echo, $(moa_precommand));									\
	fi
	$(if ifneq(($(strip $(moa_precommand)),)),$(moa_precommand))

.PHONY: moa_run_postcommand
moa_run_postcommand:
	@if [ "$(moa_postcommand)" ]; then 										\
		$(call echo, Running postcommand); 									\
		$(call echo, $(moa_postcommand));									\
	fi
	$(if ifneq(($(strip $(moa_postcommand)),)),$(moa_postcommand))

#Find project root (if there is one)
# ifndef in_project_loop
# project_root = $(shell \
# 	C=`pwd`; \
# 	$(warning processing $C);\
# 	while [[ "$$C" && ("$$C" != "/") ]]; do \
# 		if [[ -f "$$C/Makefile" ]]; then \
# 			if moa  -f $$C/Makefile ids in_project_loop=T | grep -q "project"; then \
# 				echo $$C; \
# 				break; \
# 			fi; \
# 		fi; \
# 		C=`dirname $$C`; \
# 	done; 			\
# 	echo "/";		\
# )
# endif
# .PHONY: project_info
# project_info:
# 	@if [[ "$(project_root)" != '/' ]]; then \
# 		$(shell make -s -C $(project_root) title);\
# 	fi

## 
.PHONY: is_moa
is_moa:
	@echo "Yes"

## display a MOA welcome message before a run
parentheses_open=(
parentheses_close=)
moa_welcome:
	@$(call echo, Welcome to MOA $(parentheses_open)$(shell pwd)$(parentheses_close))

## If moa.mk is defined, and not yet imported: do so.
## moa.mk is used to store job specific variables
ifndef MOAMK_INCLUDE
$(shell moa conf resolve)
-include ./moa.mk
MOAMK_INCLUDE=done
endif

###############################################################################
# Variable definition - post moa.mk include
#
# From here on moa.mk can be assumed to be included 
###############################################################################

.PHONY: title
title:
	@echo $(title)

###############################################################################
# Define and executed a MOA run 
###############################################################################

## These targets need to be executed for a normal MOA run
moa_execute_targets =										\
	moa_welcome 											\
	moa_check 												\
	moa_run_precommand										\
	moa_preprocess 											\
	$(addsuffix _prepare, $(moa_ids)) 						\
	moa_main_targets 										\
	$(addsuffix _post, $(moa_ids)) 							\
	moa_postprocess 										\
	moa_run_postcommand										\
	moa_finished

.PHONY: moa_finished
moa_finished:
	@$(call echo, Moa finished - Succes!)

## The default Moa target - A single moa invocation calls a set of targets
.PHONY: moa_default_target
.DEFAULT_GOAL := moa_default_target
moa_default_target: $(moa_execute_targets)

moa_all_targets = 											\
	$(moa_execute_targets)									\
	$(moa_additional_targets)								\
	set append clean register reset targets check			

## print out a list of all targets
.PHONY: targets
targets:
	@for x in $(moa_all_targets); do	 					\
		echo $$x;											\
	done
## print a list of all moa_ids
.PHONY: ids
ids:
	@echo $(moa_ids)

## the main targets - we run these as separate make instances since I
## really cannot make Make to reevaluate what possible in-/output
## files are created inbetween steps
moa_main_targets: minj=$(if $(MOA_THREADS),-j $(MOA_THREADS))
moa_main_targets:
	@for moa_main_target in $(moa_ids); do 										\
		$(call echo,calling $$moa_main_target) ;								\
		$(MAKE) $(minj) $$moa_main_target 												\
				$${moa_main_target}_main_phase=T ;								\
	done

## Print a list of all targets executed, in the order that they are
## executed
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
	@echo moa_welcome moa_preprocess $(addsuffix _prepare, $(moa_ids)) 			\
	  moa_check $(moa_ids) \
	  $(addsuffix _post, $(moa_ids)) \
	  moa_postprocess

## each moa makefile should include a ID_clean target cleaning up
## after it..  this one calls all cleans. Note that the x_clean
## targets are called in reverse order.
.PHONY: clean
clean: $(call reverse, $(addsuffix _clean, $(moa_ids)))
	-@rm lock 2>/dev/null || true


################################################################################
# Cruising - i.e. run this template and then walk through all subdirs
#
# by calling 'make all', all subdirs are made as well as the cd.As an extension,
# calling 'make all action=clean' calss make clean in the cd and all subdirs.
# action= can be replace by other actions. An interesting application is
# to set/change variables through a whole tree using:
#
# make all action=set KEY=VALUE
#
# The the variable KEY will be set to VALUE in this dir and all subdirs, but only
# when KEY is a defined variable for that moa-makefile
#
################################################################################

## A list of all valid targets that can be used to cruise a tree. In
## other words, these targets can be used with "make all
## action=TARGET"
moa_cruise_targets = 															\
	$(call set_create, 															\
		set append clean reset targets check						 			\
		$(moa_additional_targets)												\
		$(addsuffix _prepare, $(moa_ids)) 										\
		$(moa_ids) $(addsuffix _post, $(moa_ids))								\
	)

moa_ignore_lock_targets = \
	set append clean targets check 

## A list of all subdirectories
moa_followups ?= 																\
	$(shell find . -maxdepth 1 -type d -regex "\..+" 							\
				   -exec basename '{}' \; | sort -n )


#"all" is a synonym for cruise
.PHONY: all
all: cruise

## cruise depeends on properly executing this job, using either
## "action" as a target or the default target. Once this job is
## finished, start traversin through all subdirectories and execyte
## them as wll
.PHONY: cruise
cruise: ignore_lock?=$(strip $(if $(action), 											\
			$(if $(filter $(action),$(moa_ignore_lock_targets)),				\
				yes,)))
cruise: $(if $(call seq,$(action),), 											\
			moa_default_target,													\
			$(if $(call set_is_member, $(action), $(moa_cruise_targets)),		\
				$(action),														\
				$(warning Ignoring $(action) - not a valid target) ) )
	@for FUP in $(moa_followups); do 											\
		$(call echo,Processing $$FUP);											\
		$(call echo, +- in $(shell echo `pwd`));								\
		if [[ -e $$FUP/Makefile ]]; then 										\
			if [[ "$(ignore_lock)" == "yes" ]]; then 							\
				$(call warn,Ignore lock check);									\
				cd $$FUP;														\
				$(MAKE) cruise action=$(action);								\
				cd ..;															\
			else 																\
				if [[ ! -e $$FUP/lock ]]; then 									\
					$(call echo,Executing make $(action) in $$FUP) ;			\
					cd $$FUP;													\
					$(MAKE) cruise action=$(action);							\
					cd ..;														\
				else 															\
					$(call warn,Not going here : $$FUP is locked) ;				\
				fi ;															\
			fi;																	\
		else																	\
			$(call echo,$$FUP is not a moa directory);							\
		fi;																		\
	done

.PHONY: cruise_start_here
cruise_start_here: 																\
	$(if $(call seq,$(action),),												\
			moa_default_target,													\
			$(if $(call set_is_member, $(action), $(moa_cruise_targets)),		\
				$(action),														\
				$(warning Ignoring $(action) - not a valid target)				\
			)																	\
	)

# Add a few default targets to the set 
# of possible targets
moa_targets += check clean help show all prereqs set append

# and define help for these
check_help = Check variable definition
moa_clean_help = Clean. 
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
#moa_may_define += project
moa_must_define += title
title_type = string
title_help ?= A job name - Describe what you are doing

## author of this template
moa_author ?= Mark Fiers

###################################################
## Moa check - is everything defined?

## check prerequisites

prereqlist += prereq_moa_environment

checkPrereqExec = \
	if ! eval $(1) > /dev/null 2>/dev/null; then 								\
		$(call errr,Prerequisite check);										\
		$(call errr,Cannot execute $(1). Is properly executable?); 				\
			if [[ -n "$(2)" ]]; then 											\
				$(call errr,$(2)); 												\
			fi;																	\
			false ;																\
	fi

checkPrereqPath = \
	if ! which $(1) >/dev/null; then 											\
		$(call errr,Prerequisite check);										\
		$(call errr,Cannot find $(1) in your PATH, is it installed?); 			\
		if [[ -n "$(2)" ]]; then 												\
			$(call errr,$(2)); 													\
		fi;																		\
		false ;																	\
	fi

.PHONY: prereqs $(prereqlist)
prereqs: $(prereqlist)

moa_check_lock:
	@if [[ "$(ignore_lock)" == "T" ]]; then \
		$(call echo, Ignore lock checking);\
	else \
		if [[ -f lock ]]; then \
	    	$(call errr, Job is locked!) ;\
		    exit 2 ; \
		fi;\
	fi

#check if MOABASE is defined
prereq_moa_environment:
	@if env | grep -q MOABASE ; then true; else \
		$(call errr, the environment variable MOABASE is not defined ) ;\
		false ;\
	fi

.PHONY: check
check: moa_check 

moa_var_mustexists := $(addprefix mustexist_, $(moa_must_define))
moa_var_checkall := $(addprefix varcheck_, $(moa_must_define) $(moa_may_define))


.PHONY: moa_check
moa_check: moa_check_lock prereqs $(moa_var_mustexists) $(moa_var_checkall)
	@$(call echo, Check - everything is fine)

moa_var_check_dir:=[[ -d "$(2)" ]] || $(call exer,$(1)=$(2) is not a directory)
moa_var_check_file:=[[ -f "$(2)" ]] || $(call exer,$(1)=$(2) is not a file)

.PHONY: $(moa_var_all)
varcheck_%: chtargets=
varcheck_%: 
	@$(foreach v,$($*_type),$(ifneq("$($*)",""), $(call echo,checking $*);$(call moa_var_check_$(v),$*,$($*)), \
			$(call warn,$* is undefined)))



.PHONY: $(moa_var_mustexists)
mustexist_%:
	@if [ "$(origin $*)" == "undefined" ]; then \
		$(call errr, Error is undefined) ;\
		exit -1; \
	fi

################################################################################
## make set/append #############################################################
#
#### Store regular variables in moa.mk
#
# Usage: make set var=value
#   or:
# Usage: make append var=value
#
# Regular variables are stored in moa.mk in the following way:
#
# VARNME = VALUE
#
# or, if append is called:
#
# VARNAME += VALUE
#
# make set/append can be used to store any definable variable (from
# moa_must_define & moa_may_define and stores them as key-value pairs
# in moa.mk
#
# To make writing to the moa.mk file safe for parallel operations,
# it's being done by the moa utility script. I could not come up with
# a satisfactory locking mechanism that plays well with make/bash 
#
################################################################################

.PHONY: set
set: set_mode=set
set: __set

.PHONY: append
append: set_mode=append
append: __set

## actually writing the values to set to moa.mk is deferred to the moa
## script. This is because it's much, much easier to read & write
## files in python than it is from a Makefile.
.PHONY: __set
__set: set_func=$(1)='$(value $(1))'
__set:
	@moa conf  $(set_mode) \
		$(foreach v, $(moa_must_define) $(moa_may_define), \
			$(if $(call seq,$(origin $(v)),command line), \
				$(call set_func,$(v)) \
				$(if $($(v)_default_attrib),$(v)_default_attrib=$($(v)_default_attrib)) \
			) \
		) \
		$(foreach v,$(must_set), \
			$(call set_func,$(v)) \
		)

################################################################################
## make show ###################################################################
#
#### Show the current variables from moa.mk
#
################################################################################

.PHONY: show showvar_%
show: $(addprefix moa_showvar_, $(moa_must_define) $(moa_may_define))

moa_showvar_%:		 
	@echo -ne '$*\t'
	@echo '$(value $*)'

ifndef MOA_INCLUDE_HELP
include $(shell echo $$MOABASE)/template/__moaBaseHelp.mk
endif

################################################################################
## make info ###################################################################
#
#### Show lots of information on the current job
#
################################################################################


comma=,
info_keyval = "$(1)" : "$(subst '"',"'",$(2))"
info_keyvallist = "$(1)" : [$(call merge,$(comma),$(foreach v,$(2),"$(subst '"',"'",$(v))"))]

.PHONY: info info_header 
		info_parameters 			\
		info_parameters_optional 	\
		info_parameters_required 

info: info_header info_parameters

info_header:
	@echo -e 'moa_title\t$(moa_title)'
	@echo -e 'moa_description\t$(moa_description)'
	@echo -e 'moa_targets\t$(moa_ids) all clean $(moa_additional_targets)'

info_parameters: info_parameters_required info_parameters_optional

info_parameters_required: mandatory=yes
info_parameters_required: $(addprefix info_par_,$(moa_must_define))

info_parameters_optional: mandatory=no
info_parameters_optional: $(addprefix info_par_,$(moa_may_define))

info_par_%:
	@echo -en 'parameter'
	@echo -en '\tname=$*'
	@echo -en '\tmandatory=$(mandatory)'
	@echo -en '\ttype=$*'
	@echo -en '\tvalue=$($*)'
	@echo -en '\tdefault=$($*_default)'
	@echo -en '\tallowed=$($*_allowed)'
	@echo -en '\ttype=$($*_type)'
	@echo -en '\tcategory=$($*_category)'
	@echo -en '\thelp=$($*_help)'
	@echo



