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
#
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
