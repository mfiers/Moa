### WWWMoa ###############################
### CGIEx / Extended CGI Functionality


## Documentation ##
# This module was put together with the help of the 
# specification published at:
# <http://hoohoo.ncsa.illinois.edu/cgi/interface.html>


## Imports ##

import os
import sys
import urlparse


## State / Buffer Variables ##
_request_body=""
_request_body_loaded=False
_request_query=None


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

## Performs parsing on the query that was used in the request, if it has not already been performed.
def _parse_query():
    global _request_query

    if _request_query==None:
        try:
            _request_query=urlparse.parse_qs(get_request_query(), strict_parsing=True)
        except ValueError:
            _request_query={}


## Returns a query parameter that was used in the request.  If a parameter with the given key was not sent, returns a zero length string.
def get_request_query_value(key):
    global _request_query
    
    _parse_query()
    
    if key in _request_query:
        if len(_request_query[key])<1:
            return ""
        else:
            return _request_query[key][0]
    else:
        return ""


## Returns the keys that are present in the query that was used in the request.
def get_request_query_keys():
    global _request_query

    _parse_query()

    return _request_query.keys()


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

## Returns the body that was sent with the request.  If not found, returns a zero length string.
def get_request_body():
    global _request_body
    global _request_body_loaded

    if _request_body_loaded:
        return _request_body

    length=get_request_body_length()
    
    _request_body=sys.stdin.read(length)
    
    _request_body_loaded=True

    return _request_body

## Returns the length of the body that was sent with the request.
def get_request_body_length():
    if "CONTENT_LENGTH" in os.environ:
        a=os.environ["CONTENT_LENGTH"] # get length directly from environment
    else:
        return 0

    if a is None: # if the variable does not exist
        return 0 # return zero

    return int(a) # otherwise, return it after processing
