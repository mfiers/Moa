
## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../lib/python")

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import cgiex
from wwwmoa.formats.html import error
import wwwmoa.env
import urlparse
import os

## Main Interface Logic ##

# ensure that environment can be loaded properly
wwwmoa.env.require_environment()

# get the request passed to us during URL rewriting
raw_request=cgiex.get_request_query()
raw_request_part=raw_request.partition("?")

# split the request passed to us by the defined seperator
request_path_undecoded=raw_request_part[0].split("/")

# the completely decoded elements will be stored here
request_path=[]

# decode the elements
for r in request_path_undecoded: # for each undecoded element
    request_path.append(rl.url_decode(r)) # decode it and add it

# retrieve the request method used
request_method=cgiex.get_request_method()

# retrieve the request parameters
request_parameters_listed=urlparse.parse_qsl(raw_request_part[2])
request_parameters={}

for r in request_parameters_listed:
    request_parameters[r[0]]=r[1]

# filter out unsupported request methods
if (request_method!="GET") and \
       (request_method!="POST") and \
       (request_method!="PUT") and \
       (request_method!="DELETE"):
    error.throw_fatal_error(
        "Method Not Implemented",
        "The method you used in your request is not implemented. "+
        "Please use GET, POST, PUT or DELETE")

import wwwmoa.api

try:
    #try to run the loaded module
    wwwmoa.api.run(
        request_path,
        {"method" : request_method,
         "params" : request_parameters})
    
except Exception as e:
    # on failure, send something useful
    error.throw_fatal_error(
        "Internal API Error",
        "Python debugging information:\n"+str(e))
