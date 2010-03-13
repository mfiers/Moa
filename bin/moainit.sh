#!/bin/bash
 
if [[ "$0" =~ "moainit" ]]; then
    echo "Please *source* this file, run:"
    echo ". {PATH/}moainit_init.sh"
    echo "(note the dot!!)"
    exit -1;
fi

export MOABASE=`dirname $(dirname $(cd ${BASH_ARGV%/*} && echo $PWD/${BASH_ARGV##*/}))`
export PATH=$MOABASE/bin:$PATH