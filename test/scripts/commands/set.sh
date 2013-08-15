#!/bin/bash
export MOA_GIT_ENFORCE=False

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t test
moa set process='echo'
moa show | grep title | grep -q test
moa show | grep title | grep -vq otherwise
moa set title=otherwise
moa show | grep title | grep -vq test
moa show | grep title | grep -q otherwise
moa set dummy=bla
moa show | grep dummy | grep -q bla

#now try recursive loading of variables
mkdir 10.subdir
cd 10.subdir
moa new simple -t subtest
moa set process=echo
moa show -a | grep dummy | grep -q bla
moa show | grep title | grep -q subtest

rm -rf $tmpdir