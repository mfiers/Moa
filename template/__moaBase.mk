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
###
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

ifndef MOAMK_INCLUDE
$(shell moa conf cache)
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
  moa_check \
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
		$(MAKE) $$moa_main_target ;\
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
set: set_func=$(1)="$($(1))"
set: __set

.PHONY: append
append: set_mode=append
append: set_func=$(1)="$($(1))"
append: __set

.PHONY: __set
__set:
	@moa conf $(set_mode) \
		$(foreach v, $(moa_must_define) $(moa_may_define), \
			$(if $(call seq,$(origin $(v)),command line), \
				$(call set_func,$(v)) \
			) \
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
# default attribute, defined as VARNAME_cdbattr in the Makefile. If
# that also doesn't exists, pwd is used as the attribute, pointing to
# the directory where the other job lives.
#
################################################################################

#determines which attribute we want from couchdb - either it's defined 
#using id:attr, or its defined in the defining Makefile via $*__cdbattr
#else use pwd.
#cdbsplit returns: coubdb_id couchdb_attribute
#if no attribute can be determine
cdbsplit = $(call first,$(call split,^,$(1))) \
	$(call first, $(word 2,$(call split,^,$(1))) $($(2)_cdbattr) pwd) 

.PHONY: cset
cset: set_mode=set
cset: set_func=$(1)__couchdb="$(call cdbsplit,$($(1)),$(1))"
cset: $(if $(call seq,$(usecouchdb),T), __set, moa_couchdb_unset)

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
	@echo -e "$*\t$($*)"


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


##############################################################################
# Generate Latex 
#
.PHONY: latex
latex: \
	moa_latex_header \
	moa_latex_description \
	moa_latex_vars \
	moa_latex_footer

.PHONY: moa_latex_header
moa_latex_header: 
	@echo "\section{$(moa_ids)}"

.PHONY: moa_latex_description
moa_latex_description: $(addprefix moa_latex_description_, $(moa_ids))

moa_latex_description_%:
	@echo $(moa_title_$*)
	@echo -e "$(moa_description_$*)"

moa_latex_vars: moa_latex_vars_start \
		moa_latex_vars_must \
		moa_latex_vars_may
	@echo "\end{description}"

moa_latex_vars_start:
	@echo "\subsection{Variables}"
	@echo "\textbf{Must be defined:}"
	@echo "\begin{description}"

moa_latex_vars_must: $(addprefix  moa_latex_var_, $(moa_must_define))
	@if [ -z "$^" ]; then \
		echo "\end{description}" ;			\
	else 									\
		echo "\end{description}";			\
		echo "\bf{May be defined:}";		\
		echo "\begin{description}";		\
	fi

moa_latex_vars_may: $(addprefix moa_latex_var_, $(moa_may_define))

moa_latex_var_%:	
	@if [ "$(origin $*_help)" == "undefined" ]; then \
		echo "\item[$*]"; 		\
	else 						\
		echo "\item[$*] $($*_help)"; \
	fi

.PHONY: moa_latex_footer
moa_latex_footer:


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