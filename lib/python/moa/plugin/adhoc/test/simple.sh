#!/bin/bash

moa simple --np -t test -- echo "something"
out=`moa run`
[[ "$out" =~ "something" ]] || (echo "invalid output" && false )
