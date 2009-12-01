moa new -t "Test run" traverse

make set project="test project" || xx "Make set does not execute"

project=`make show | grep "^project" | cut -f 2`
[[ "$project" == "test project" ]] \
    || xx "Make show: 'project' != 'test project'"
