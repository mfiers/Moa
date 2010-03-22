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
## Git - use git to keep track of project history

## Add a hook for project_init
moa_hooks_postinit_project += moa_git_init_project
moa_hooks_postinit += moa_git_init

## Add a hook after a var got set
moa_hooks_postset += moa_git_postset

#files that need to be stored in the repository 
moa_git_files += Makefile moa.mk .gitignore

