##
## Couchdb
##

#Use couchdb? (T/F) (default=F)
usecouchdb=T

#The default couchdb server lives at: localhost:5984
#if you want to use an alternative couchdb server:
#couchserver = 127.0.0.1:5984

#the database name to use with couchdb (default: moa)
#couchdb ?= moa

##
## HELP
##
#where is pandoc binary located? 
#default is use the pandoc in the path
#pandocbin=/path/to/pandoc
pandocbin=/usr/local/bin/pandoc121
#
#How to process man output, use the mand command:
#mancommand=man -l -
# or, this is possibly safer:
mancommand=nroff -c -mandoc 2>/dev/null | less -is
