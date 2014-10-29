set -e

export MOA_GIT_ENFORCE=false

tmpdir=`mktemp -d -t moatest`
cd $tmpdir
echo "Running in $PWD"

mkdir 10.input
cd 10.input
for x in $(seq -w 1 10)
do
	touch input.$x
done
cd ..
mkdir 20.map
cd 20.map
moa new map -t 'test map'
moa set input='../10.input/input.*'
moa set output='./output.*'
moa set process='echo {{ input }} > {{ output }}'
moa run

grep '../10.input/input.01' output.01
grep '../10.input/input.04' output.04

cd ..
rm -rf $tmpdir