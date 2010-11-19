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
## define all variables here that are not depending on moa.mk
###############################################################################

__MOA_INCLUDE_CORE = yes
#see if __prepare is already loaded, if not load:
include $(MOABASE)/lib/gnumake/prepare.mk

##load the plugins: contains core - post definition
$(foreach p,$(moa_plugins), \
	$(eval -include $(MOABASE)/lib/gnumake/plugins/$(p).mk) \
)


################################################################################
## EXECUTION
## Here we handle the execution of all targets necessary

## These targets need to be executed for a normal MOA run
moa_execute_targets = \
	$(moa_id)_prepare \
	moa_main_target \
	$(moa_id)_post \
	moa_finished

## The default Moa target - A single moa invocation calls a set of targets
.DEFAULT_GOAL: run
.PHONY: run
run:  $(moa_execute_targets)

.PHONY: moa_run_precommand
ifdef moa_precommand
moa_run_precommand:
	$(call warn,running moa_precommand)
	$e $(moa_precommand)
else:
moa_run_precommand:

endif

.PHONY: moa_run_postcommand
ifdef moa_postcommand
moa_run_postcommand:
	$(call echo, Running postcommand)
	$e $(moa_postcommand)
else
moa_run_postcommand:

endif

#catch undefine prepare steps - 
%_prepare:
	@echo -n

%_post:
	@echo -n

.PHONY: moa_finished
moa_finished:
	@$(call echo,Moa finished - Succes!)

## the main targets - we run these as separate make instances since I
## really cannot make Make to reevaluate what possible in-/output
## files are created inbetween steps
moa_main_target: minj=$(if $(MOA_THREADS),-j $(MOA_THREADS))
moa_main_target:
	$(call echo,calling $(moa_id)) ;		\
	$(MAKE) $(mins) $(minj) $(moa_id) $(moa_id)_main_phase=T ;

## each moa makefile should include a ID_clean target cleaning up
## after it..  this one calls all cleans. Note that the x_clean
## targets are called in reverse order.
.PHONY: clean
clean: $(moa_id)_clean


