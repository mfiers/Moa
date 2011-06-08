#!/bin/bash 

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa simple -t test -- echo
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
moa simple -t subtest -- echo
moa show | grep dummy | grep -q bla
moa show | grep title | grep -q subtest\

rm -rf $tmpdir