#!/bin/bash -v

set -xe


export MOA_GIT_ENFORCE=False

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

echo "set up a simple job"


moa new simple -t 'something else'
moa set title='test'
moa set process='echo hello'

echo "check if the title is properly set"
moa show | grep 'title' | grep -q 'test'

echo "setting title to something new"
moa set title='something'

echo "check if the title is properly set to something"
moa show | grep 'title' | grep -q 'something'

echo "try to set an undefined variable"
moa set dummy='dumb'

echo "check if the dummy is set"
moa show | grep 'dummy' | grep -q 'dumb'

echo "create a job in a subdir"
mkdir sub
cd sub
moa new simple -t 'something else'
moa set title='test'

echo "dummy should still be set - check"
moa show -a | grep 'dummy' | grep -q 'dumb'


