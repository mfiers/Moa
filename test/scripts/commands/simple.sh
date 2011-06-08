#!/bin/bash 

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa simple --np -t test -- echo "something"
out=`moa run`
[[ "$out" =~ "something" ]] || (echo "invalid output" && false )

rm -rf $tmpdir