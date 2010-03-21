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

MOA_INCLUDE_PLUGIN_GIT= yes

################################################################################
## Git - use git to keep track of project history

## Add a hook for project_init
moa_hooks_postinit_project += moa_git_init_project
moa_hooks_postinit += moa_git_init

## Add a hook after a var got set
moa_hooks_postset += moa_git_postset

#files that need to be stored in the repository 
moa_git_files += Makefile moa.mk .gitignore

#Initialize a git project
.PHONY: moa_git_init_project

#function to actually create the repos
moa_git_init_repository = git init 2>&1 > /dev/null
moa_git_init_gitignore = \
	if [[ ! -f .gitignore ]]; then \
		echo "*" > .gitignore; \
		for mgf in $(moa_git_files); do \
			echo "!$$mgf" >> .gitignore; \
		done; \
	fi \

##Determine git commit message
ifdef MOA_GITMESSAGE
	commit_message = $(MOA_GITMESSAGE)
else
	commit_message = moa $(MAKECMDGOALS) automated commit
endif

#Initialze a git repository
moa_git_init_project: $(if $(MOA_UNITTESTS),,moa_git_init_project_2)

moa_git_init_project_2:
	if ! git status 2>&1 | grep -q 'Not a git repo' ; \
	then \
		if [[ "$$MOA_GITFORCEINIT" ]] && ls .git | grep -q config ; \
		then \
			$(call warn,Initalizing GIT repository$(comma) removing old repository); \
			rm -rf .git; \
			$(call moa_git_init_repository); \
			$(call moa_git_init_gitignore); \
		else \
			$(call exer,Unable to  remove the old repository - GIT is not properly set up); \
		fi; \
	else \
		$(call echo,Initalizing a GIT repository); \
		$(call moa_git_init_repository); \
		$(call moa_git_init_gitignore); \
	fi

#do not run moa git init when in doing unittests
moa_git_init: $(if $(MOA_UNITTESTS),,moa_git_init_2)

.PHONY: moa_git_init
moa_git_init_2:
	if [[ -d "$(MOAPROJECTROOT)/.git" ]]; then \
		$(warning in git init)
		git add $(minv) --all; \
		git commit -qa -m "$(commit_message)" >/dev/null; \
	fi


.PHONY: moa_git_postset
moa_git_postset:
	$e echo $(MOAPROJECTROOT);
	if [[ -d "$(MOAPROJECTROOT)/.git" ]]; then \
		git add moa.mk; \
		git commit -q -m "$(commit_message)" moa.mk ; \
	fi


.PHONY: gitlog
gitlog:
	git log --pretty=oneline --abbrev-commit
