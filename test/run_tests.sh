#!/bin/bash

echo "running unittests"

python -m unittest discover -p 'test_*.py'
