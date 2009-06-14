
# Help
moa_ids += traverse
moa_title_traverse = Traverse
moa_description_traverse = Do noting, except be a part in executing full directory structures

#Include base moa code - does '*:blastn.self' variable checks & generates help

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

traverse_main:
	@echo "Traversing through `pwd`"

traverse_prepare:
traverse:
traverse_post:
traverse_clean:
