set -v
tmpdir=`mktemp -d`
cd $tmpdir
echo "Running in $PWD"

moa new simple -t 'test simple'
moa set process='echo "hello" > output'
moa run
[[ -f output ]]
grep 'hello' output
echo "finished"

rm -rf $tmpdir