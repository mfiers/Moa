#!/bin/bash

set -e
set -v

tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

for x in `seq -w 1 20`; do
   touch test.$x
done

moa map --np -t test
moa set process="echo {{ output }}; cp {{input}} {{ output }}"
moa set input="./test.*"  output="./out.*"

output=`moa run 2>&1`

echo "output:"
echo $output

# out.01 should be in the output (since it was processed)
[[ "$output" =~ "out.01" ]] || (echo "invalid output 1" && false )
output=`moa run 2>&1`

echo "output:"
echo $output

# out.01 should not be in the output (it was already processed last time)
[[ ! "$output" =~ "out.01" ]] || ( \
    echo "invalid output 2";
    echo $output
    ls
    false
)
touch test.01
output=`moa run 2>&1`
# out.01 should be in the output (it was touched since the last process)
[[ "$output" =~ "out.01" ]] || (echo "invalid output 3" && false )
# but out.02 not
[[ ! "$output" =~ "out.02" ]]  ||  (echo "invalid output 4" && false ) 
#echo $output



rm -rf $tmpdir