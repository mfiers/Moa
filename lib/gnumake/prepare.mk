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

##old include statement
#ifndef dont_include_moabase
#  include $(shell echo $$MOABASE)/template/__moaBase.mk
#endif

## for the time being, mixing two templates is not allowed anymore
## this becomes too complex since Make really needs to be able to depend
## on moaBase included in exactly that spot. This also means that we're not
## using the variable dont_include_moabase anymore. And hence moaBase will allways
## be included from the Makefiles that were created until now. We use a new 
## variable to make sure that we don't inlcue moabase twice, accidentallly

ifndef MOA_INCLUDE_PREPARE
 include $(MOABASE)/lib/gnumake/__prepare.mk
endif
