#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

-include moa.mk
MOAMK_INCLUDE=done

## moa_preprocess & moa_postprocess are targets that can
## be overridden here. They are executed before & after
## the main execution

.PHONY: moa_preprocess
moa_preprocess:

.PHONY: moa_postprocess
moa_postprocess:

dont_include_moabase=true
include $(shell echo $$MOABASE)/template/traverse.mk
include $(shell echo $$MOABASE)/template/__moaBase.mk
