set -e

export MOA_GIT_ENFORCE=False

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
mkdir 20.reduce
cd 20.reduce
moa new reduce -t 'test reduce'
moa set input=../10.input/input.*
moa set output=./output
moa set process='echo {{ input|join(" ") }} > {{ output }}'
moa run
ls -l
cat ./output
grep '../10.input/input.07' ./output
grep '../10.input/input.02' ./output
grep '../10.input/input.12' ./output || false && true
cd ..

rm -rf $tmpdir