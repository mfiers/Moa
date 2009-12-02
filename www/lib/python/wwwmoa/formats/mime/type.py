
## Imports ##

import os.path


## Lookup Dictionary ##

_ext_lookup={".jpeg" : "image/jpeg", ".jpg" : "image/jpeg",
         ".png" : "image/png",
         ".txt" : "text/plain",
         ".html" : "text/html",
         ".htm" : "text/html",
         ".css" : "text/css",
         ".gif" : "image/gif",
         ".pdf" : "application/pdf",
         ".js" : "text/javascript",
         ".svg" : "image/svg+xml",
         ".xml" : "text/xml"}


## Lookup Utilities ##

## Returns a MIMETYPE that seems like a good fit for a given
## file.  The MIMETYPE is found by inspecting the file's name.
## A MIMETYPE is always returned, even if the file's name did
## not correspond directly with a given MIMETYPE.
def guess_from_filename(filename):
    global _ext_lookup

    (root, ext)=os.path.splitext(filename) # partition the filename

    ext=ext.strip().lower() # prepare extension to make it more easy to detect

    if ext in _ext_lookup: # if extension has direct match
        return _ext_lookup[ext] # return the match
    else: # if the extension does not have a direct match
        return "text/plain" # we must always return a mimetype, so return mimetype for plain text


## Returns a MIMETYPE that seems like a good fit for a given
## file.  The MIMETYPE may be found using a variety of methods
## including inspection of the file's name and inspection of
## the contents of the file.  A MIMETYPE is always returned,
## even if the file did not correspond directly with a given
## MIMETYPE.
##
## Note that the input filename must be absolute, and it must
## correspond to an existing file.  If these two criteria
## cannot be gauranteed, use guess_from_filename().
def guess_from_file(filename):
    return guess_from_filename(filename) # just a wrapper for now
