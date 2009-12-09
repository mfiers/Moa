moa new -t "Test run" -p "Test project" traverse

make show || \
    xx "Make show does not execute"

make show | grep "^title" \
    || xx "Make show does not print 'title'"

title=`make show | grep "^title" | cut -f 2`

[[ "$title" == "Test run" ]] \
    || xx "Make show: 'title' != 'Test run'"

make show | grep "^project" \
    || xx "Make show does not print 'project'"

project=`make show | grep "^project" | cut -f 2`

[[ "$project" == "Test project" ]] \
    || xx "Make show: 'title' != 'Test project'"

make show | grep "moa_precommand" \
    || xx "Make show does not show moa_precommand"

make show | grep "moa_postcommand" \
    || xx "Make show does not show moa_postcommand"

