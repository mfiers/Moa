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

################################################################################
## pack  #######################################################################
#
################################################################################

.PHONY: moa_plugin_pack_test
moa_plugin_pack_test:
	$e touch x.bla
	$e touch y.bla
	$e mkdir 10.test
	$e cd 10.test;  moa -t 'testing pack' -d 10.test adhoc 'ls ../*.bla'
	$e cd 10.test; moa pack --pn ../pack.test
	$e ls * >&2
	$e moa unpack ./pack.test.tar.bz2 -d 20.test