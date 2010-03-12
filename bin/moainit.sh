#!/bin/bash
 
if [[ "$0" =~ "quick" ]]; then
    echo "Please source this file, run (note the additional dot)";
    echo ". {PATH/}quick_init.sh";
    exit -1;
fi

export MOABASE=$(dirname $(cd ${BASH_ARGV%/*} && echo $PWD/${BASH_ARGV##*/}))
export PATH=$MOABASE:$PATH

echo "The current shell is now set to to use the moa installation in"
echo "$MOABASE"
echo
echo "Note that this does not apply to any other shell that you might have opened or will open"
echo
echo "You can make this your default Moa install by adding the following lines to your .bashrc"
echo
echo "export MOABASE=$MOABASE"
echo "export PATH=\$PATH:$MOABASE/bin"