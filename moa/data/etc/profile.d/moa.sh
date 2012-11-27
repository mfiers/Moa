#!/bin/bash
#
# This script is supposed to be executed in the context of an
# installed moa version - in the case of a uninstalled version,
# as checked out from github, try ./util/moainit_u
#

#make sure we're being sourced
if [[ "$0" =~ "moainit" ]]; then
    echo "Please *source* this file, run:"
    echo ". {PATH/}moainit.sh"
    echo "(note the dot!!)"
    exit -1;
fi

#shortcut
alias msp='moa set process'
alias mst='moa set title'

###
### Moa prompt stuff!
alias moa_prompt_off='unset MOA_PROMPT'
alias moa_prompt_on='export MOA_PROMPT=yes'

if [[ ! "$PROMPT_COMMAND" =~ "_moa_prompt" ]]
then
    export PROMPT_COMMAND="_moa_prompt;$PROMPT_COMMAND"
fi

function _moa_prompt {

    #Get the last command
    #based on:
    #http://stackoverflow.com/questions/945288/...
    #     ...saving-current-directory-to-bash-history

    local lc=$(history 1)
    lc="${lc# *[0-9]*  }"

    #save the last command to a user specific location
    if [[ ! -d '~/.config/moa' ]]
    then
        mkdir -p ~/.config/moa
    fi
    echo $lc > ~/.config/moa/last.command

    #if not in a moa dir - stop here
    [[ -d '.moa' ]] || return 0

    #and add it to the local history if this is a mob job
    if [[ -w '.moa' ]]
    then
        if [[ ! -a '.moa/local_bash_history' ]]
        then
            touch .moa/local_bash_history
        fi
        if [[ -w '.moa/local_bash_history' ]]
        then
            echo $lc >> .moa/local_bash_history 2>/dev/null || true
        fi
    fi
    if [[ "$MOA_PROMPT" ]]
    then
        #farm this out to a python script
        moaprompt
    fi
}


# Bash completion stuff

__moa_is_moadir() {
	if [[ -e ".moa/template" ]]; then
		echo "yes";
	else
		echo "no"
	fi
}

__moa_get_template() {
	echo `moa template`
}

__moa_all_templates() {
	#return a list of all known moa templates
    echo `moa list`
}

__moa_all_vars() {
    #return a list of all known moa templates
    if [[ $(__moa_is_moadir) == "yes" ]]
    then
        if [[ -f ".moa/completion/parameters" ]]
        then
            echo `cat .moa/completion/parameters`
        else
	    echo `moa raw_parameters`
	fi
    fi
}

_moa()
{
    local cur prev opts shopts moacomms moacommand
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="--help --force --verbose --bg --title"
    shopts="-h -f -v -j -t"
    moacommand=""

    if [[ ${cur} == --* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts} ${shopts}" -- ${cur}) )
        return 0
    fi

    if [[ ${prev} == moa ]]; then
        globalcommandfile="~/.config/moa/globalCommands"
        if [[ -f ".moa/completion/commands" ]]
        then
            local commands=`cat .moa/completion/commands`
        elif [[ -f ".moa/template" ]]
        then
            echo 'raw'
            local commands=`moa raw_commands`
        elif [[ -f `eval "echo ~/.config/moa/globalCommands"` ]]
        then
            local commands=`cat  ~/.config/moa/globalCommands`
        else
            echo 'raw2'
            local commands=`moa raw_commands`;
        fi
    	COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi

    #Find the currently entered command (if there is one)
        for x in $(seq 1 ${COMP_CWORD})
	  do
	  [[ ${COMP_WORDS[x]} == -* ]] && continue
	  moacommand=${COMP_WORDS[x]}
          for y in $(seq $((x+1)) ${COMP_CWORD})
	  do
	      [[ ${COMP_WORDS[y]} == -* ]] && continue
	      moaSecCommand=${COMP_WORDS[y]}
	      break
	  done
	  break
	done

    case "${moacommand}" in

	new)
       	   local templates=$(__moa_all_templates)
       	   COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
            ;;
        set)
	    local vars=$(__moa_all_vars)
	    COMPREPLY=( $(compgen -o nospace -W "${vars}" -- ${cur}) )
	    ;;
        *)
        	;;
    esac
}
complete -o nospace -o default -o bashdefault -F _moa moa
