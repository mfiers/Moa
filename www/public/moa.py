### WWWMoa ###############################
### moa.py / Main Interface
### Version: 0.1
### Date: November 19, 2009

## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../private/")

import WWWMoaRW
import WWWMoaRL
import WWWMoaCGIEx
import WWWMoaHTMLError
import WWWMoaInfo
import os

## Main Interface Logic ##

# get the request passed to us during URL rewriting
raw_request=WWWMoaRW.get_request_param("request")

# split the request passed to us by the defined seperator
request_undecoded=raw_request.split("/")

# the completely decoded elements will be stored here
request=[]

# decode the elements
for r in request_undecoded: # for each undecoded element
    request.append(WWWMoaRL.url_decode_x(r)) # decode it and add it

if len(request)<=0: # if there are not any decoded elements
    obj_type="" # no object type was passed
else: # if there was at least one decoded element
    obj_type=request[0] # the first one is the object type

# retrieve the request method used
request_method=WWWMoaCGIEx.get_request_method()

# filter out unsupported request methods
if (request_method!="GET") and (request_method!="POST") and (request_method!="PUT") and (request_method!="DELETE"):
    WWWMoaHTMLError.throw_fatal_error("Method Not Implemented","""The method you used in your request is not implemented.  Please try one of the following request methods:
* GET
* POST
* PUT
* DELETE""")

# load module by object type
if obj_type=="resources": # if a resource was requested
    import WWWMoaMod_Resource as WWWMoaMod
elif obj_type=="api": # if an action on the file system was requested
    import WWWMoaMod_API as WWWMoaMod
elif obj_type=="hms": # if a helper module was requested
    import WWWMoaMod_HM as WWWMoaMod
elif obj_type=="": # if no object type seems to have been passed
    import WWWMoaHTMLEngine

    # show geek view
    WWWMoaHTMLEngine.set_title("Geek View")
    WWWMoaHTMLEngine.start_output()
    WWWMoaHTMLEngine.start_section()
    WWWMoaHTMLEngine.place_section_title("Welcome to Geek View!")
    WWWMoaHTMLEngine.place_text("This view will show you various things that you might be interested in knowing... if you are a geek.")
    WWWMoaHTMLEngine.end_section()
    WWWMoaHTMLEngine.start_section()
    WWWMoaHTMLEngine.place_section_title("Modules Currently Mapped")
    WWWMoaHTMLEngine.place_text("""WWWMoaMod_Resource => resources""")
    WWWMoaHTMLEngine.place_text("""\nWWWMoaMod_API => api""")
    WWWMoaHTMLEngine.place_text("""\nWWWMoaMod_HM => hms""")
    WWWMoaHTMLEngine.place_text("""\nWWWMoaMod_ErrorNF => (anything not caught elsewhere)""")
    WWWMoaHTMLEngine.end_section()
    WWWMoaHTMLEngine.start_section()
    WWWMoaHTMLEngine.place_section_title("Install Information")
    WWWMoaHTMLEngine.place_text("""Install Name: """+WWWMoaInfo.get_string()+"\n")
    WWWMoaHTMLEngine.place_text("""Python OS Module: """+os.name+"\n")
    WWWMoaHTMLEngine.end_section()
    WWWMoaHTMLEngine.end_output()
else: # if yet another object type was tried
    import WWWMoaMod_ErrorNF as WWWMoaMod

try: # try to run the loaded module
    WWWMoaMod.run(request[1:],{"method" : request_method})
except Exception as e: # on failure, send something useful
    WWWMoaHTMLError.throw_fatal_error("Internal Error", "I did find the item that you requested.  However, it misbehaved in such a way that it could not continue.\n\nThe Python interpreter (which I run on) supplied me with the following reason for the failure (you might find the following  useful when debugging):\n\""+str(e)+"\"")
