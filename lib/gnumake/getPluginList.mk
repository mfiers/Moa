# A very simple makefile that does nothing more 
# than try to get a list of plugins if executed
# outside of a moa job folder

## Load moa system wide configuration
-include $(MOABASE)/etc/moa.conf.mk

-include ~/.moa/moa.conf.mk

-include ./moa.mk

.DEFAULT_GOAL := get_moa_plugins
.PHONY: get_moa_plugins
get_moa_plugins:
	@echo  $(moa_plugins)

