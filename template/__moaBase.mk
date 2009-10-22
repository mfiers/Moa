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

## some help variables
warn_on := \033[0;41;37m
warn_off := \033[0m
boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

#a colorful mark, showing that this comes from moabase
moamark := \033[0;30;41m \033[46m -*MOA*- \033[41m \033[0m
moaerrr := \033[0;6;39m!!!\033[41;25;37mERROR\033[0;6;39m!!!\033[0m
moawarn := \033[0;30;46m \033[41m WARNING \033[46m \033[0m
echo = echo -e "$(moamark) $(1)"
warn = echo -e "$(moawarn) $(1)"
errr = echo -e "$(moaerrr)$(warn_on) -- $(1) -- $(warn_off)"


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

moa_may_define += moa_postcommand
moa_postcommand_help = A single shell command to be executed after the			\
Moa is finished. For more complex processing please override the				\
moa_postprocess target in the local Makefile.

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

## display a MOA welcome message before a run
parentheses_open=(
parentheses_close=)
moa_welcome:
	@$(call echo, Welcome to MOA $(parentheses_open)$(shell pwd)$(parentheses_close))

## If moa.mk is defined, and not yet imported: do so.
## moa.mk is used to store job specific variables
ifndef MOAMK_INCLUDE
$(shell moa conf cache)
-include ./moa.mk
MOAMK_INCLUDE=done
endif

###############################################################################
# Variable definition - post moa.mk include
#
# From here on moa.mk can be assumed to be included 
###############################################################################

## If the job identifier is not defined, define one here
generate_owner=$(shell whoami)
ifndef owner
owner := $(call generate_owner)
endif

generate_jid=$(shell moa db generate_jid \
			"$(title)" "$(project)" "$(owner)" "$(moa_ids)" )

ifeq ($(jid),)
jid := $(call generate_jid)
endif

.PHONY reinit:
reinit: jid:=$(call generate_jid)
reinit: owner:=$(call generate_owner)
reinit: set_mode=set
reinit: must_set=jid owner
reinit: __set
	@$(call echo,Jid: $(jid))

###############################################################################
# Define and executed a MOA run 
###############################################################################

## These targets need to be executed for a normal MOA run
moa_execute_targets =										\
	moa_welcome 											\
	moa_prepare_var 										\
	moa_check 												\
	moa_run_precommand										\
	moa_preprocess 											\
	$(addsuffix _prepare, $(moa_ids)) 						\
	moa_main_targets 										\
	$(addsuffix _post, $(moa_ids)) 							\
	moa_postprocess 										\
	moa_run_postcommand										\
	moa_register											\
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

## the main targets - we run these as separate make instances since I
## really cannot make Make to reevaluate what possible in-/output
## files are created inbetween steps
moa_main_targets:
	@for moa_main_target in $(moa_ids); do 										\
		$(call echo,calling $$moa_main_target) ;								\
		$(MAKE) $$moa_main_target 												\
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
		set append clean register reset targets check reinit		 			\
		$(moa_additional_targets)												\
		$(addsuffix _prepare, $(moa_ids)) 										\
		$(moa_ids) $(addsuffix _post, $(moa_ids))								\
	)

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
cruise: $(if $(call seq,$(action),), 											\
			moa_default_target,													\
			$(if $(call set_is_member, $(action), $(moa_cruise_targets)),		\
				$(action),														\
				$(warning Ignoring $(action) - not a valid target) ) )
	@$(call echo,Processing followups $(moa_followups) );
	@for FUP in $(moa_followups); do 											\
		$(call echo,Processing $$FUP from $(shell echo `pwd`));					\
		if [[ -e $$FUP/Makefile ]]; then 										\
			$(call echo,$$FUP/Makefile found);									\
			if [[ "$(ignore_lock)" == "T" ]]; then 								\
				$(call warn,Ignore lock checking) ;								\
				cd $$FUP;														\
				$(MAKE) cruise action=$(action);								\
				cd ..;															\
			else 																\
				$(call echo,No lock check $$FUP);								\
				if [[ ! -e $$FUP/lock ]]; then 									\
					$(call warn,Executing make $(action) in $$FUP) ;			\
					cd $$FUP;													\
					$(MAKE) cruise action=$(action);							\
					cd ..;														\
				else 															\
					$(call errr,Not going here : $$FUP is locked) ;				\
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
moa_may_define += project jid owner
moa_must_define += title
title_help = A title name defining this job. Cannot have spaces.
owner_help = Job owner (usually the unix username who created the job)
project_help ?= A project name - group your analyses.
title_help ?= A job name - describe your analysis (and find them them			\
back)
jid_help ?= Unique identifier for this job. Jids are autogenerated if			\
  undefined.  A unique jid is important.

moa_author ?= Mark Fiers

##############################################################################
## Register this job usine Apache Couchdb
## Don't use couchdb per default! 
usecouchdb ?= F
couchserver ?= 127.0.0.1:5984
couchdb ?= moa

.PHONY: moa_couchdb_unset
moa_couchdb_unset:
	@$(call errr,Couchdb is turned off!)
	@$(call errr,Have a look at: $(MOABASE)/etc/moa.conf.mk)

.PHONY: register
register: moa_register

.PHONY: moa_register
moa_register: moa_check_jid
	@if [ "$(usecouchdb)" == "T" ]; then \
		$(call echo,Calling moa register. Couchdb server: $(couchserver)) ;\
		moa -s $(couchserver) -d $(couchdb) register $(jid) \
			moa_ids="$(moa_ids)" pwd="`pwd`" date="`date`" \
			$(foreach v, $(moa_must_define), $(v)="$($(v))") \
			$(foreach v, $(addsuffix  __couchdb,$(moa_must_define)), \
								$(if $($(v)),$(v)="$($(v))")) \
			$(foreach v, $(moa_may_define), $(v)="$($(v))") \
			$(foreach v, $(addsuffix  __couchdb,$(moa_may_define)), \
								$(if $($(v)),$(v)="$($(v))")) \
			$(foreach v, $(moa_register_extra), $(v)=$(moa_register_$(v))) ;\
	fi

moa_register_%:
	weka2 set moa.$(project).$(moa_main_id).$(name).$* $($*)

###################################################
## Moa check - is everything defined?


###########################################################################
#check prerequisites

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

ter:
	$(call errr, Hello)

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
	@moa conf $(set_mode) \
		$(foreach v, $(moa_must_define) $(moa_may_define), \
			$(if $(call seq,$(origin $(v)),command line), \
				$(call set_func,$(v)) \
			) \
		) \
		$(foreach v,$(must_set), \
			$(call set_func,$(v)) \
		)

################################################################################
## make cset ###################################################################
#
#### Store couchdb variables in moa.mk
#
# usage: make cset Varname=couchdb_id:couchdb_attr
#                                    ^-- note: colon
#  or:
# usage: make cset Varname=couchdb_id
#
#
# Couchdb variables are stored in moa.mk in the following way:
#
# VARNAME__couchdb = couchdb-id couchdb-attribute
#                              ^-- note: space
#
# During the initialization phase of Moa makefile execution all *__couchdb
# variables are retrieved from couchdb and subsequently cached in moa.mk as
# regular variables. If a variable is defined as both couchdb & regular var,
# the regular var will get overwritten!
#
# A couchdb variable can defined on the commandline with or without an
# attribute defined. If the attribute is ommitted, moa looks for a
# default attribute, defined as VARNAME_default_attrib in the Makefile. If
# that also doesn't exists, pwd is used as the attribute, pointing to
# the directory where the other job lives.
#
################################################################################

## determines which attribute we want from couchdb - either it's
## defined using id:attr, or its defined in the defining Makefile via
## $*__default_attrib else use pwd.
##
## cdbsplit returns: coubdb_id couchdb_attribute
## with "pwd" as attribute if no attribute is defined
cdbsplit = $(call first,$(call split,^,$(1))) \
	$(call first, $(word 2,$(call split,^,$(1))) $($(2)_default_attrib) pwd) 

.PHONY: cset
cset: set_mode=set
cset: set_func=$(1)__couchdb="$(call cdbsplit,$($(1)),$(1))"
cset: $(if $(call seq,$(usecouchdb),T), __set, moa_couchdb_unset)

## TODO: think about cappend - do we need that??

################################################################################
## make show ###################################################################
#
#### Show the current variables from moa.mk
#
################################################################################

.PHONY: show showvar_%
show: moa_prepare_var \
	$(addprefix moa_showvar_, $(moa_must_define) $(moa_may_define))
moa_showvar_%:		 
	@echo -ne '$*\t'
	@echo '$(value $*)'


################################################################################
## make moa_prepare_var ########################################################
#
#### Cache couchdb values in moa.mk
#
# Handled by the moa script, to prevent any possible race condition
#
################################################################################

.PHONY: moa_prepare_var
moa_prepare_var:
	@if [ "$(usecouchdb)" == "T" ]; then \
		moa conf cache ;\
	fi

ifndef MOA_INCLUDE_HELP
include $(shell echo $$MOABASE)/template/__moaBaseHelp.mk
endif