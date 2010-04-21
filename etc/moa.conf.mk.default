##
## HELP
##
## where is pandoc binary located? 
## default is use the pandoc in the path

pandocbin = pandoc
#pandocbin ?= $(shell which pandoc)

## How to process man output, use the mand command:
#mancommand=man -l -

## or, this is possibly safer:
mancommand=nroff -c -mandoc 2>/dev/null | less -is

## plugins - Add functionality to Moa

##
## THE FOLLOWING PLUGINS ARE CORE PLUGINS _ DO NOT DELETE THESE!!
##

# filesets - utilities to define sets of files
# not - it is probably a good idea to load this early
moa_plugins += fileset

# configure - set a variable
moa_plugins += configure

# newjob - Create new Moa jobs
moa_plugins += newjob

# Generate help
moa_plugins += help 

# display a small Moa logo at start of operation 
moa_plugins += logo

# unittest code
moa_plugins += test

# info - display machine and human readable info on a job
moa_plugins += info

##
## THE REMAINING PLUGINS ARE OPTIONAL - remove them at will
##

# Version control using git
#moa_plugins += git 

# Some utilities for making moa easier to use
moa_plugins += moautil 


# state - report on the current state of the pipeline
# moa_plugins += state
