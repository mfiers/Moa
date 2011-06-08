#!/bin/bash

cd `mktemp -d`
echo "Running in $PWD"

echo "set up a simple job"
moa simple --np -t test -- echo

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
moa new simple --np -t 'subtest' -- echo

echo "dummy should still be set"

echo "check if the dummy is set"
moa show | grep 'dummy' | grep -q 'dumb'


