#!/bin/bash 

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa simple -t test -- echo
moa show | grep 'title' | grep -q 'test'
moa unset title
moa show | grep 'title' | grep -qv 'test'
# recursive unset
moa set aaa=bbb
moa show | grep 'aaa' | grep -q 'bbb'
mkdir 10.sub
cd 10.sub
moa simple -t sub -- echo
moa set aaa=bbb
moa show | grep 'aaa' | grep -q 'bbb'
cd ..
moa unset -r aaa >/dev/null
moa show | grep 'aaa' | grep -qv 'bbb'
cd 10.sub
moa show | grep 'aaa' | grep -qv 'bbb'

rm -rf $tmpdir