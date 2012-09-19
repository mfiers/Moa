#!/bin/bash

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t test
moa set process='echo'
moa set process='echo blabla'
moa show | grep -q 'echo blabla'
moa show | grep 'title' | grep -q 'test'

rm -rf $tmpdir