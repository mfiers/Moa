moa new -t "Test run" -p "Test project" traverse

[[ -e "moa.mk" ]]  || xx "moa.mk is not created"

[[ -e "Makefile" ]] || xx "Makefile is not created"

grep "title=Test run" moa.mk || xx "Title is not stored in moa.mk"
grep "project=Test project" moa.mk || xx "Title is not stored in moa.mk"

