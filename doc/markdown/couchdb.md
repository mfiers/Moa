Couchdb \citep{couchdb} is a novel type of database that is almost
copmletely unlike a SQL database. In it's simplest form it is a high
performance key-value datastore. Moa uses Couchdb to store information
on all analyses performed by Moa. This means that for each job that
Moa performs, a record is created in the Couchdb database. This record
has a unique identifier, called `jid`. Moa creates jids on the fly by
combining the template name, the directory name and a unique
identifier (to prevent collisions). These names are not always very
descriptive, so it is advisable to set a jid manually. This is
possible using the following command (do not use spaces!): 

    make set jid=SensibleName

Each time Moa executes, the analysis record in Couchdb is updated. The
record contains all parameters used, the type of analysis done and the
location (current directory) of the analysis. It is possible to update
the couchdb record without running the analysis using:

    make register

Moa/Couchdb records are a set of key/value pairs, that look like this:


The most important application of Couchdb in Moa is to refer to other
jobs using Couchdb identifiers. In a Moa project without couchdb
references to the output of other jobs is done by defining the path to
that analysis. If, at a certain moment, the project structure needs to
be rearranged, it can be hard to discover which path references need
to be updated. Use of couchdb solves this, instead of refering to a
path, it is now possible to refer to a jid / value combination.

 allows a user to refer to another Moa job by the
identifier, as opposed to using (relative) directories. The biggest
advantage is that is now possible to shuffle your directories around
without breaking the pipeline structure.

##Configuration

Please follow the couchdb documentation to set up a local server. Moa
has been developed with the latest version of Couchdb (currently
0.9.1). It might be possible to use an older version, but that has not
been tested.

All Moa configuration for couchdb is done in
`$MOABASE/etc/moa.conf.mk`.

The default setting of Moa is to not use couchdb. This can be
overrided by setting: 
    usecouchdb=T

Moa expects a Couchdb server on `localhost:5984`. This can be
overridden using:
    couchserver=other.server:portnumber

All information 

##Using couchdb with Moa

Instead of using \lstinline!make set key=value!, couchdb variables are
set using \lstinline!make cset jid^key!

 LocalWords:  jid SensibleName
