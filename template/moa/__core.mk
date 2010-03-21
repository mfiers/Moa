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

__MOA_INCLUDE_CORE = yes
#see if __prepare is already loaded, if not load:
include $(MOABASE)/template/moa/prepare.mk

##load the plugins: contains core - post definition
$(foreach p,$(moa_plugins), \
	$(eval -include $(MOABASE)/template/moa/plugins/$(p).mk) \
)

##moa_list_plugins - list all loaded plugins
.PHONY: moa_list_plugins
moa_list_plugins:
	@echo $(moa_plugins)

## Prepare - fill in the defaults of all variables
## Fill in the default values of each variable
$(foreach v,$(moa_must_define) $(moa_may_define), \
	$(if $($v),, \
		$(if $($v_default), \
			$(eval $v=$($v_default))) ) )

## Evaluate & load the filesets
$(foreach v,$(_moa_filesets), \
	$(eval $(v)_files = $(wildcard $($(v)_dir)/$($(v)_glob).$($(v)_extension))))

moa_fileset_init = $(warning use of moa_fileset_init is deprecated)

################################################################################
## EXECUTION
## Here we handle the execution of all targets necessary

## These targets need to be executed for a normal MOA run
moa_execute_targets = \
	moa_check_lock \
	moa_set_runlock \
	$(moa_hooks_pre_welcome) \
	moa_welcome \
	$(moa_hooks_pre_check) \
	moa_check \
	moa_run_precommand \
	moa_preprocess \
	$(moa_id)_prepare \
	$(moa_hooks_pre_run) \
	$(moa_hooks_pre_run_$(moa_id)) \
	$(moa_id) \
	$(moa_id)_post \
	moa_postprocess \
	moa_run_postcommand \
	moa_clean_runlock \
	moa_finished


## The default Moa target - A single moa invocation calls a set of targets
.PHONY: moa_default_target
.DEFAULT_GOAL := moa_default_target
moa_default_target: $(moa_execute_targets)

moa_run_precommand:
	$e if [[ "$(value moa_precommand)" ]]; then \
		$(call echo,Running precommand); \
	fi
	$e $(moa_precommand)

.PHONY: moa_run_postcommand
moa_run_postcommand:
	$e if [ "$(value moa_postcommand)" ]; then \
		$(call echo, Running postcommand); \
	fi
	$e $(moa_postcommand)

#$(if ifneq(($(strip $(moa_postcommand)),)),$(moa_postcommand))

#catch undefine prepare steps - 
%_prepare:
	@echo -n

%_post:
	@echo -n

%_initialize:
	@echo -n

%_unittest:
	@$(call exer,$@ is undefined)


moa_welcome:
	@$(call echo, Starting MOA $(MAKECMDGOALS) in $(CURDIR))

###############################################################################
# Variable definition - post moa.mk include
#
# From here on moa.mk can be assumed to be included 
###############################################################################

.PHONY: moa_set_runlock
moa_set_runlock:
	$e if [[ -f 'moa.runlock' ]]; then \
		oldpid=`cat moa.runlock`; \
		oldexec=`ps -p $$oldpid -o comm=`; \
		if [[ "$$oldexec" == "make" ]]; then \
			$(call exer,This job is already running); \
		else \
			$(call warn,Found what appears to be a stale lockfile - removing); \
			rm moa.runlock; \
		fi; \
	fi; \
	$(call echo,Locking job for this run); \
	$(call echo,$(shell ps -p $$PPID -o comm=)); \
	echo $$PPID > moa.runlock

.PHONY: moa_clean_runlock
moa_clean_runlock:
	$(call echo,Removing run lock)
	-rm moa.runlock

.PHONY: moa_finished
moa_finished:
	@$(call echo,Moa finished - Succes!)

moa_all_targets = \
	$(moa_execute_targets) \
	$(moa_additional_targets) \
	set append clean register reset targets check

## print out a list of all targets
.PHONY: targets
targets:
	@for x in $(moa_all_targets); do \
		echo $$x; \
	done

## print a list of all moa_id
.PHONY: ids
ids:
	@echo $(moa_id)

## the main targets - we run these as separate make instances since I
## really cannot make Make to reevaluate what possible in-/output
## files are created inbetween steps
moa_main_targets: minj=$(if $(MOA_THREADS),-j $(MOA_THREADS))
moa_main_targets:
	$(call echo,calling $(moa_id)) ;							\
	$(MAKE) $(mins) $(minj) $(moa_id) 							\
				$(moa_id)_main_phase=T ;

## each moa makefile should include a ID_clean target cleaning up
## after it..  this one calls all cleans. Note that the x_clean
## targets are called in reverse order.
.PHONY: clean
clean: clean_start $(call reverse, $(addsuffix _clean, $(moa_id)))
	-$e rm moa.out moa.err moa.success 2>/dev/null || true
	-$e rm moa.failed moa.runlock lock 2>/dev/null || true

.PHONY: clean_start
clean_start: moa_welcome


################################################################################
# Initialize - to be executed when setting up the moa job  (i.e. calling moa new xxx)
#

.PHONY: initialize $(moa_id)_initialize
initialize: \
	$(moa_hooks_preinit)				\
	$(moa_hooks_preinit_$(moa_id)) 		\
	$(moa_id)_initialize				\
	$(moa_hooks_postinit_$(moa_id)) 	\
	$(moa_hooks_postinit)
	@echo -n

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

## A list of all valid targets that can be used to all a tree. In
## other words, these targets can be used with "make all
## action=TARGET"
moa_all_targets = \
	$(call set_create, \
		set append clean reset targets check \
		$(moa_additional_targets) \
		$(moa_id)_prepare \
		$(moa_id) \
		$(moa_id)_post \
	)

moa_ignore_lock_targets = \
	set append clean targets check 

## A list of all subdirectories
moa_followups ?= \
	$(shell find . -maxdepth 1 -type d -regex "\..+" \
				   -exec basename '{}' \; | sort -n )

## all depends on properly executing this job, using either
## "action" as a target or the default target. Once this job is
## finished, start traversin through all subdirectories and execyte
## them as wll
.PHONY: all
all:  ignore_lock?=$(strip $(if $(action), \
			$(if $(filter $(action),$(moa_ignore_lock_targets)), \
				yes,)))
all: $(if $(call seq,$(action),), \
			moa_default_target, \
			$(if $(call set_is_member, $(action), $(moa_all_targets)), \
				$(action), \
				$(warning Ignoring $(action) - not a valid target) ) )
	$e for FUP in $(moa_followups); do \
		set -e \
		$(call echo,Processing $$FUP \
			$(if $(call seq,$(ignore_lock),yes), \
				$(p_open)IGNORING LOCK!$(p_close))); \
		$(call echo, +- in $(shell echo `pwd`)); \
		if [[ -e $$FUP/Makefile ]]; then \
			if [[ "$(ignore_lock)" == "yes" ]]; then \
				cd $$FUP; \
				$(MAKE) $(mins) all action=$(action); \
				cd ..; \
			else \
				if [[ ! -e $$FUP/lock ]]; then \
					cd $$FUP; \
					$(MAKE) $(mins) all action=$(action); \
					cd ..; \
				else \
					$(call warn,Not going here : $$FUP is locked) ; \
				fi ; \
			fi; \
		else \
			$(call echo,$$FUP is not a moa directory); \
		fi; \
	done
	$(call echo,Successfully finished moa all run $(if $(action),action=$(action)))


# Add a few default targets to the set 
# of possible targets
moa_targets += check clean show all prereqs set

# and define help for these
check_help = Check variable definition
moa_clean_help = Clean. 
show_help = Show the defined variables
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

## check prerequisites
prereqlist += prereq_moa_environment

checkPrereqExec = \
	if ! eval $(1) > /dev/null 2>/dev/null; then \
		$(call errr,Prerequisite check); \
		$(call errr,Cannot execute $(1). Is properly executable?); \
			if [[ -n "$(2)" ]]; then \
				$(call errr,$(2)); \
			fi; \
			$(call exerUnlock); \
	fi

checkPrereqPath = \
	if ! which $(1) >/dev/null 2>/dev/null; then \
		$(call errr,Prerequisite check: \
			Cannot find $(1) in your PATH $(comma).); \
		if [[ "$(strip $(2))" ]]; then \
			$(call errr,$(2)); \
		fi; \
		$(call exerUnlock); \
	fi

.PHONY: prereqs $(prereqlist)
prereqs: $(prereqlist) \
	$(addprefix moa_prereq_simple_check_,$(moa_prereq_simple))

moa_prereq_simple_check_%:
	$e $(call checkPrereqPath,$*)

moa_check_lock:
	@if [[ "$(ignore_lock)" == "T" ]]; then \
		$(call echo, Ignore lock checking);\
	else \
		if [[ -f lock ]]; then \
	    	$(call exer, Job is locked!) ;\
		fi;\
	fi

.PHONY: moa_lock lock
lock: moa_lock
moa_lock:
	touch lock

.PHONY: moa_unlock unlock
unlock: moa_unlock
moa_unlock:
	-rm lock

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
moa_check: prereqs $(moa_var_mustexists) $(moa_var_checkall)
	@$(call echo,everything is fine)

moa_var_check_dir:=[[ -d "$(2)" ]] || $(call exer,$(1)=$(2) is not a directory)
moa_var_check_file:=[[ -f "$(2)" ]] || $(call exer,$(1)=$(2) is not a file)

.PHONY: $(moa_var_all)
varcheck_%: chtargets=
varcheck_%: 
	@$(foreach v,$($*_type),$(ifneq("$($*)",""), $(call echo,checking $*);$(call moa_var_check_$(v),$*,$($*)), \
			$(call warn,$* is undefined)))

mustexist_%:	
	@if [ "$(origin $*)" == "undefined" ]; then \
		$(call exerUnlock,Error: $* is undefined) ;\
	fi

################################################################################
## make show ###################################################################
#
#### Show the current variables from moa.mk
#
################################################################################

.PHONY: show moa_showvar_%
show: $(addprefix moa_showvar_, $(moa_must_define) $(moa_may_define))

moa_showvar_%:		 
	$e echo -ne '$*\t'	
	$e echo '$(value $*)'

.PHONY: get moa_getvar_%
get: $(addprefix moa_getvar_, $(filter $(var),$(moa_must_define) $(moa_may_define)))

moa_getvar_%:
	@echo '$(value $*)'


################################################################################
## make showvars ###############################################################
#
#### print a list of all definable variables
#
################################################################################

.PHONY: showvars
showvars:
	for x in $(moa_must_define) $(moa_may_define); do \
		echo $$x; \
	done

