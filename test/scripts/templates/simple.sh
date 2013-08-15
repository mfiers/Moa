set -v

export MOA_GIT_ENFORCE=False

tmpdir=`mktemp -d -t moatest`

cd $tmpdir
echo "Running in $PWD"

moa new simple -t 'test simple'
moa set process='echo "hello" > output'
moa run
[[ -f output ]]
grep 'hello' output
echo "finished"

rm -rf $tmpdir