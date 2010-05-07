
This command aids in copying a directory with a Moa job to another
location. All job settings are copied as well. The simplest invocation
is:

     moa cp 20.source 30.target
     
which will create the `30.target` directory (if it is not present) and copy the job from `20.source`.

Alternatively it is possible to run the following shorthand:

    moa cp 20.source 30
    
in which case the job in `20.source` is copied to `30.source`.
