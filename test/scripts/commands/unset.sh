#!/bin/bash

set -vex

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"


moa new simple -t test
moa set process='echo'
moa show | grep 'title' | grep -q 'test'
moa unset title
[[ ! `moa show | grep 'title' | grep -q 'test'` ]]
# recursive unset
moa set aaa=bbb
moa show | grep 'aaa' | grep -q 'bbb'
mkdir 10.sub
cd 10.sub
moa new simple -t sub
moa set process=echo

moa set aaa=bbb
moa show | grep 'aaa' | grep -q 'bbb'

rm -rf $tmpdir
