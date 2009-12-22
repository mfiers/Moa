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

moa_ids += test
moa_title = Unittest template
moa_description = Not to be used - is used by unittests

unittest_help = Do nothing - no need to call this. 

## define a few test variables

#an obligatory variable
moa_must_define = txt
txt_help = test variable
txt_type = string

#and an optional one
moa_may_define = test_opt
test_opt_help = test variable
test_opt_type = string
test_opt_default = konijntje

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

test_prepare:
test_post:
test_clean:
	-rm moa_test
#default function is to create the file 'moa_test' with content 'test.  
test: 
	$e echo '$(txt)' > moa_test

unittests: unittest_moabase_var
.PHONY: unittest_moabase_var
unittest_moabase_var:
	$e $(call moa_unittest_var,title,Test title)
	$e $(call moa_unittest_var,txt,test variable 1)
	$e $(call moa_unittest_var,txt,test variable 2)
	$e $(call tstm,Test removing the value of txt)
	$e moa $(minv) set txt=
	$e grep -q "txt" moa.mk && $(call exer,variable txt was not removed!) || true
	$e $(call tstm,Check if moa will run with an obligatory variable unset)
	$e ( moa $(minv) >/dev/null \
			&& $(call exer,Should not finished succesfully - txt is not defined) \
		) || true	
	$e $(call tstm,Check automatic assignment of variables works)
	$e ( moa show | grep "test_opt" | grep "konijntje"  ) \
		|| $(call exer,Default variable assignment seems broken)
	$e moa set test_opt=olifantje
	$e $(call tstm,Finished all variable releated unittests)
