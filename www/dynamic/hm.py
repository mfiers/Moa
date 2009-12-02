
## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../lib/python")

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import cgiex
from wwwmoa.formats.html import error
import wwwmoa.env

## Main Interface Logic ##

# ensure that environment can be loaded properly
wwwmoa.env.require_environment()

# get the request passed to us during URL rewriting
raw_request=rw.get_request_param("request")

# split the request passed to us by the defined seperator
request_undecoded=raw_request.split("/")

# the completely decoded elements will be stored here
request=[]

# decode the elements
for r in request_undecoded: # for each undecoded element
    request.append(rl.url_decode_x(r)) # decode it and add it

# retrieve the request method used
request_method=cgiex.get_request_method()

# filter out unsupported request methods
if (request_method!="GET") and (request_method!="POST") and (request_method!="PUT") and (request_method!="DELETE"):
    error.throw_fatal_error("Method Not Implemented","""The method you used in your request is not implemented.  Please try one of the following request methods:
* GET
* POST
* PUT
* DELETE""")

import wwwmoa.mod.hm as server_mod

try: # try to run the loaded module
    server_mod.run(request,{"method" : request_method})
except Exception as e: # on failure, send something useful
    error.throw_fatal_error("Internal HM Error", "I did find the item that you requested.  However, it misbehaved in such a way that it could not continue.\n\nThe Python interpreter (which I run on) supplied me with the following reason for the failure (you might find the following  useful when debugging):\n\""+str(e)+"\"")
