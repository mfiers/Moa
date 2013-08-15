#!/bin/bash

export MOA_GIT_ENFORCE=False

set -e
set -v

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t test
moa set process='echo something'
out=`moa run`
[[ "$out" =~ "something" ]] || (echo "invalid output" && false )

rm -rf $tmpdir