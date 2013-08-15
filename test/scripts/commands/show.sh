#!/bin/bash

export MOA_GIT_ENFORCE=False

set -e
set -v

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t test
moa set process='echo'
moa set process='echo blabla'
moa show | grep -q 'echo blabla'
moa show | grep 'title' | grep -q 'test'

rm -rf $tmpdir