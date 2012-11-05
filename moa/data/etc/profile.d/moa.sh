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

#few shortcuts
alias msp='moa set process'

#Set environment variables for moa
export MOADATA=`dirname $(dirname $(dirname $(cd ${BASH_ARGV%/*} && echo $PWD/${BASH_ARGV##*/})))`

echo $MOADATA
#export PATH=$MOADATA/bin:$PATH
#export PYTHONPATH=$MOADATA/lib/python:$PYTHONPATH

source $MOADATA/etc/bash_completion.d/moa

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
