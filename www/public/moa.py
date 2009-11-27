### WWWMoa ###############################
### moa.py / Main Interface
### Version: 0.1
### Date: November 19, 2009

## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../lib/python")

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import cgiex
from wwwmoa.formats.html import error
from wwwmoa import info
from wwwmoa.formats import html
import wwwmoa.env
import os

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

if len(request)<=0: # if there are not any decoded elements
    obj_type="" # no object type was passed
else: # if there was at least one decoded element
    obj_type=request[0] # the first one is the object type

# retrieve the request method used
request_method=cgiex.get_request_method()

# filter out unsupported request methods
if (request_method!="GET") and (request_method!="POST") and (request_method!="PUT") and (request_method!="DELETE"):
    error.throw_fatal_error("Method Not Implemented","""The method you used in your request is not implemented.  Please try one of the following request methods:
* GET
* POST
* PUT
* DELETE""")

# load module by object type
if obj_type=="resources": # if a resource was requested
    import wwwmoa.mod.resource as server_mod
elif obj_type=="api": # if an action on the file system was requested
    import wwwmoa.mod.api as server_mod
elif obj_type=="hms": # if a helper module was requested
    import wwwmoa.mod.hm as server_mod
elif obj_type=="": # if no object type seems to have been passed
    # display specific message

    rw.send_header("Content-Type", "text/html")
    rw.send_header("Cache-Control", "no-cache")
    rw.send_header("Expires", "0")
    rw.end_header_mode()

    rw.send("""

<html>

<head>

<title>Magic Root</title>

</head>

<body>

You have reached the \"magic root\" of """+html.fix_text(info.get_name())+""".<br><br>

You might be interested in continuing to the home page.  If so, <a href=\""""+html.fix_text(rl.get_home())+"""\">click here</a>.

</body>

</html>

""")
    rw.terminate()
else: # if yet another object type was tried
    error.throw_fatal_error("Not Found", "I could not find the item you requested.")

try: # try to run the loaded module
    server_mod.run(request[1:],{"method" : request_method})
except Exception as e: # on failure, send something useful
    error.throw_fatal_error("Internal Error", "I did find the item that you requested.  However, it misbehaved in such a way that it could not continue.\n\nThe Python interpreter (which I run on) supplied me with the following reason for the failure (you might find the following  useful when debugging):\n\""+str(e)+"\"")
