#!/bin/bash

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t test
moa set process='echo something'
out=`moa run`
[[ "$out" =~ "something" ]] || (echo "invalid output" && false )

rm -rf $tmpdir