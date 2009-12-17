### WWWMoa ###############################
### CGIEx / Extended CGI Functionality


## Documentation ##
# This module was put together with the help of the 
# specification published at:
# <http://hoohoo.ncsa.illinois.edu/cgi/env.html>
# which was accessed on November 19, 2009.


## Imports ##

import os


## CGI Functions ##

## Returns the HTTP method used in the request.  If not found, returns a zero length string.  The returned string has had whitespace stripped and has been uppercased. No checking is performed to make sure that the request method is a true HTTP request method.
def get_request_method():
    if "REQUEST_METHOD" in os.environ:
        a=os.environ["REQUEST_METHOD"] # get method directly from environment
    else:
        return ""

    if a is None: # if the variable does not exist
        return "" # return zero length string

    return a.strip().upper() # otherwise, return it after processing

## Returns the query that was used in the request.  If not found, returns a zero length string.
def get_request_query():
    if "QUERY_STRING" in os.environ:
        a=os.environ["QUERY_STRING"] # get method directly from environment
    else:
        return ""

    if a is None: # if the variable does not exist
        return "" # return zero length string

    return a.strip() # otherwise, return it after processing

## Returns the port number that the server was accessed at.  If not found or not valid, will return -1.  The returned port will be an integer, not a string.
def get_request_port():
    if "SERVER_PORT" in os.environ:
        a=os.environ["SERVER_PORT"] # get port directly from environment
    else:
        return -1 # return -1 as per specs

    if a is None: # if the variable does not exist
        return -1 # return -1 as per specs

    try: # attempt conversion to an integer
        return int(a)
    except: # on conversion failure
        return -1 # return -1 as per specs
