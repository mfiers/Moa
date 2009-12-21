### WWWMoa ###############################
### Mod_API / Main API

## Imports ##

from wwwmoa import rw
from wwwmoa import rl



import wwwmoa.env
from wwwmoa.formats.html import error
import wwwmoa.info.moa as moainfo

import os
import os.path
import json
import time
import sys


## Helper Functions ##

## Figures out whether or not a given path is equivalent to the psuedo-root directory.
def is_root(path):
    return os.path.samefile(wwwmoa.env.get_content_dir(), path)

## Figures out whether or not a given path is within the psuedo-root directory.
def in_root(path):
    return os.path.samefile(os.path.commonprefix([path, wwwmoa.env.get_content_dir()]), wwwmoa.env.get_content_dir())

## Outputs a custom error message.
def output_error(err):
    error.throw_fatal_error("API Failure", "The API request you made failed so badly that it could not continue.  More details can be found below.\n\n" + err)

## Outputs headers appropriate to a JSON-formatted response.  The single argument should be the seconds that the response can be safely cached; the default is 0 seconds.
def output_json_headers(ttl=0):
    rw.send_header("Content-Type", "application/json") # we will be sending JSON

    ttl_int=int(ttl)

    if ttl_int<1: # if ttl is less than one second
        rw.send_header("Cache-Control", "no-cache") # this response should NOT be cached
        rw.send_header("Expires", "0") # some older browsers need this to not cache a response
    else: # if ttl is non-trivial
        rw.send_header("Cache-Control", "max-age="+str(ttl_int)) # this response can be cached

## Adds the standard timestamping elements to a JSON response dictionary, and returns the dictionary.  The ttl argument is the seconds that the response can be safely cached; the default is 0 seconds.
def add_timestamp(dct, ttl=0):
    dct["timestamp"]=time.time() # add the time that the timestamp was added
    if ttl>=0: # if ttl is meaningful
        dct["ttl"]=ttl # add the time interval that the response can be cached
    else: # if ttl is not meaningful
        dct["ttl"]=0 # add the default value for ttl

    return dct

## Main Interface Logic ##


def run(args=None, env=None):
    if (args==None) or (env==None):
        output_error("An unexpected error has occurred.")

    moa_pylib_base=moainfo.get_pylib_base()

    if moa_pylib_base==None:
        output_error("A Moa implementation could not be found.")
    else:
        sys.path.append(moa_pylib_base)

        import moa.api as mwr

    
    # check to make sure we have enough parameters
    if len(args)<1: # if there is not at least one parameter
        output_error("The API request you made cannot be completed, because you did not supply enough information.")

    # extract the command and file system path
    command=rl.url_decode_x(args[len(args)-1])
    if len(args)>=2: # if there was a path sent
        content_path_array=args[:len(args)-1] # the subset of elements that would determine the path are all except for the last one
        content_path=("/".join(content_path_array)) # the path is directly determined by the elements
    else: # if there was not a path sent
        content_path_array=[] # the element array is empty
        content_path="" # just return the root (which is not absolute, so it is an empty string)

    
    import wwwmoa.api.ls

    path=os.path.join(wwwmoa.env.get_content_dir(), content_path) # get the complete pathname

    path=os.path.normpath(path) # make path as simple as possible

    if os.path.islink(path): # if the path is actually a symb link
        path=os.path.realpath(path) # find what the path really points to

    # make sure requested path is safe
    
    if not in_root(path): # if the requested path is not in the psuedo-root directory
        error.throw_fatal_error("Access Denied", "The directory you attempted to access cannot be, because you do not have the permission to do so.") # say so
    
    if not os.path.isdir(path): # if the request path does not exist
        error.throw_fatal_error("Target Not Found", "The directory you attempted to access does not exist.") # say so


    if command=="moa-jobinfo":
        if not mwr.isMoaDir(path): # if the path does not correspond to a Moa directory
            output_error("The directory or file you attempted to retrieve job information on is not a Moa directory.") # say so            

        job_info=mwr.getInfo(path)

        output_json_headers(0);
        rw.end_header_mode();
        rw.send(json.dumps(add_timestamp(job_info, 0)));

    elif command=="moa-jobparam":
        if not mwr.isMoaDir(path): # if the path does not correspond to a Moa directory
            output_error("The directory or file you attempted to retrieve and/or set job information on is not a Moa directory.") # say so

        if "key" in env["params"]:
            var_key=env["params"]["key"]
        else:
            output_error("The parameter key was not specified in the API request. The parameter key must be included in the API request.")

        if (env["method"]=="POST") or (env["method"]=="PUT"): # if a set was requested

            if "value" in env["params"]:
                var_value=env["params"]["value"]
            else:
                var_value=""
           
            mwr.setParameter(path, var_key, var_value)

        elif env["method"]=="GET": # if a get was requested
            var_value=mwr.getParameter(path, var_key)
        elif env["method"]=="DELETE" : # if a delete was requested
            mwr.setParameter(path, var_key, "")

    
        output_json_headers(0);
        rw.end_header_mode();
        rw.send(json.dumps(add_timestamp({"key" : var_key, "value" : var_value}, 0)));


    elif command=="ls":
        wwwmoa.api.ls.run(args, env, path)
    else: # if the request type is unknown
        output_error("The specific API request you made is not supported.") # say so
