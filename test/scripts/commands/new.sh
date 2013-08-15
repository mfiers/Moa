#!/bin/bash

export MOA_GIT_ENFORCE=False

set -e
set -v

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t 'test' 2>/dev/null >/dev/null
[[ -d '.moa' ]]
[[ -f '.moa/template' ]]
[[ -d '.moa/template.d' ]]
[[ -f '.moa/template.d/simple.jinja2' ]]
[[ -f '.moa/template.meta' ]]

grep -q 'provider: core' .moa/template.meta
grep -q 'name: simple' .moa/template.meta
grep -q 'simple' .moa/template

moa new core:simple -ft 'test' 2>/dev/null >/dev/null

##hack to create a local:simple template
mkdir -p ~/.config/moa/template
cat .moa/template | sed 's/name: simple/name: newjobtest/' \
    | sed 's/moa_id: simple/moa_id: newjobtest/' \
    > ~/.config/moa/template/newjobtest.moa
cp .moa/template.d/simple.jinja2 ~/.config/moa/template/newjobtest.jinja2

moa new -f local:newjobtest
grep -q 'provider: local' .moa/template.meta
grep -q 'name: newjobtest' .moa/template.meta
moa set process='echo qwerqwer'
moa show
out=`moa run 2>/dev/null`
[[ "$out" =~ 'qwerqwer' ]]

cd
rm -rf $tmpdir
