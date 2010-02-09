## Imports ##

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import cgiex

import wwwmoa.env
from wwwmoa.formats.html import error
import wwwmoa.info.moa as moainfo
import wwwmoa.formats.mime.type as mimetype

import os
import os.path
import json
import time
import sys
import urlparse
import shutil
import cgi
import StringIO




## Helper Functions ##

## Figures out whether or not a given path is equivalent to the
## psuedo-root directory.
def is_root(path):
    return os.path.samefile(wwwmoa.env.get_content_dir(), path)


## Figures out whether or not a given path is within the psuedo-root
## directory.
def in_root(path):
    return os.path.samefile(os.path.commonprefix([path, wwwmoa.env.get_content_dir()]),
                            wwwmoa.env.get_content_dir()
                            )


## Outputs a custom error message.
def output_error(err):
    error.throw_fatal_error("API Failure",
                            "\
The API request you made failed so badly that \
it could not continue.  More details can be found below.\n\n" + err
                            )


## Outputs headers appropriate to a JSON-formatted response.  The single
## argument should be the seconds that the response can be safely cached;
## the default is 0 seconds.
def output_json_headers(ttl=0):
    rw.send_header("Content-Type", "application/json") # we will be sending JSON

    ttl_int=int(ttl)

    if ttl_int<1: # if ttl is less than one second
        rw.send_header("Cache-Control", "no-cache") # this response should NOT be cached
        rw.send_header("Expires", "0") # some older browsers need
                                       #this to not cache a response
    else: # if ttl is non-trivial
        rw.send_header("Cache-Control", "max-age="+str(ttl_int)) # this response can be cached


## Adds the standard timestamping elements to a JSON response dictionary, 
## and returns the dictionary.  The ttl argument is the seconds that the
## response can be safely cached; the default is 0 seconds.
def add_timestamp(dct, ttl=0):
    dct["timestamp"]=time.time() # add the time that the timestamp was added
    if ttl>=0: # if ttl is meaningful
        dct["ttl"]=ttl # add the time interval that the response can be cached
    else: # if ttl is not meaningful
        dct["ttl"]=0 # add the default value for ttl

    return dct


## Outputs a standard "action message" to be used with API that perform an
## action, but do not return any data except for whether the action was
## successful or not.
def output_action_message(success, text=""):
    output_json_headers(0)
    rw.end_header_mode()

    rw.send(json.dumps(add_timestamp({"success" : success,
                                      "x-message" : text
                                      }, 0 # by its nature, this message
                                           # will timeout immediatly
                                     )))






## Main Interface Logic ##

def run(args=None, env=None):
    if (args==None) or (env==None): # if we were not handed args or env
        output_error("An unexpected error has occurred.") # say so

    try: # attempt to find Moa implementation
        moa_pylib_base=moainfo.get_pylib_base(True)
        sys.path.append(moa_pylib_base) # add Moa Python library to search path
    except moainfo.MoaNotFoundError: # if we could not find a Moa implementation
        output_error("A Moa implementation could not be found.") # say so

    # now that we have updated the search path,
    # attempt to load Moa Python library API
    import moa.api as moaapi



    # check to make sure we have enough parameters
    if len(args)<1: # if there is not at least one parameter
        output_error("\
The API request you made cannot be completed, because you did not supply \
enough information.")

    # extract the command and file system path
    command=args[len(args)-1]
    command=command.strip()
    if len(args)>=2: # if there was a path sent
        content_path_array=args[:len(args)-1] # the subset of elements that
                                              # determine the path are all 
                                              # except for the last one
        content_path=("/".join(content_path_array)) # the path is directly 
                                                    # determined by the elements
    else: # if there was not a path sent
        content_path_array=[] # the element array is empty
        content_path="" # just return the root (which is not 
                        # absolute, so it is an empty string)



    # load API package internals
    import wwwmoa.api.ls as api_ls
    import wwwmoa.api.reg as apireg
    import wwwmoa.api.doc as apidoc



    # before we go any further, make sure the command is supported
    if command=="": # if an API command was not specified
        output_error("You did not specify an API request to complete.") # say so

    if not apireg.isMethodSupported(command, env["method"]): # if the command is not supported
        output_error("The specific API request you made is not supported.") # say so



    # get the complete pathname
    path=os.path.join(wwwmoa.env.get_content_dir(), content_path)

    # make path as simple as possible
    path=os.path.normpath(path)

    if os.path.islink(path): # if the path is actually a symb link
        path=os.path.realpath(path) # find what the path really points to



    # make sure requested path is safe
    
    if not in_root(path): # if the requested path is not in the content directory
        error.throw_fatal_error("Access Denied",
                                "You do not have permission to access the path you specified."
                                ) # say so
    
    if not os.path.isdir(path) and not os.path.isfile(path): # if the request path does not exist
        error.throw_fatal_error("Target Not Found",
                                "The item you attempted to access does not exist."
                                ) # say so

    if not apireg.pathSatisfiesRequirements(path, command, env["method"]): # if path is not suitable
        output_error("\
The directory or file you specified cannot be used with \
\"{0}\" when accessed with \"{1}\".".format(command, env["method"])) # say so


    
    # make sure the required parameters have been supplied

    required_params=apireg.getRequiredParameters(command, env["method"]) # retrieve required parameters

    for r in required_params: # for each required parameter
        if not r in env["params"]: # if the parameter was not supplied
            output_error("\
When \"{0}\" is accessed with \"{1}\", you must supply \
the \"{2}\" parameter.\n\n\"{2}\" parameter information:\n\
".format(command, env["method"], r) + apireg.getParameterHelp(command, env["method"], r)) # say so




    # now we are ready to actually process the specific request



    ## moa-jobinfo Command ##

    # Note: This command is now deprecated.  "moa-job" / GET should be
    # used instead.  This command will likely be removed in the future.

    if command=="moa-jobinfo":
        job_info=moaapi.getInfo(path)

        output_json_headers(0)
        rw.end_header_mode()
        rw.send(json.dumps(add_timestamp(job_info, 0)))




    ## moa-jobsession Command ##

    elif command=="moa-jobsession":
        job_status=moaapi.status(path)

        if env["method"]=="GET":
            job_obj={"status" : job_status}

            try:
                job_output=env["params"]["output"]=='1'
            except KeyError:
                job_output=False

            if job_output:
                job_obj["output"]=moaapi.getMoaOut(path)
                job_obj["output-error"]=moaapi.getMoaErr(path)

            output_json_headers(0)
            rw.end_header_mode()
            rw.send(json.dumps(add_timestamp(job_obj, 0)))

        elif job_status!="running":
            if env["method"]=="PUT":
                if "target" in env["params"]:
                    moaapi.runMoa(path, env["params"]["target"])
                else:
                    moaapi.runMoa(path)

                output_action_message(True, "The Moa job has been started.")
            elif env["method"]=="DELETE":
                moaapi.runMoa(path, "clean")

                output_action_message(True, "The Moa job has been cleaned.")
        else:
            output_action_message(False, "The Moa job is already running.")




    ## moa-jobparams Command ##

    elif command=="moa-jobparams":


        if env["method"]=="POST": # if a single set was requested
            var_key=env["params"]["key"]
            var_value=cgiex.get_request_body()
            moaapi.setParameter(path, var_key, var_value)

            output_action_message(True, "The Moa job parameter has been set.")
        elif env["method"]=="PUT": # if a set was requested
            try:
                var_dict=json.loads(cgiex.get_request_body())
            except ValueError:
                output_action_message(False, "The Moa job parameter set you sent was not valid.")
            else:
                for v in var_dict.keys():
                    moaapi.setParameter(path, v, var_dict[v])
                    
                output_action_message(True, "The supplied Moa job parameters have been set.")
        elif env["method"]=="GET": # if a get was requested
            output_json_headers(0)
            rw.end_header_mode()
            rw.send(json.dumps(add_timestamp({"parameters" : moaapi.getInfo(path)["parameters"]}, 0)))


    ## moa-templates Command ##

    elif command=="moa-templates":
        output_json_headers(0)
        rw.end_header_mode()
        rw.send(json.dumps(add_timestamp({"templates" : moaapi.templateList()}, 0)))




    ## moa-job Command ##

    elif command=="moa-job":
        err_string="""

The templates that are currently installed are:
"""+"\n".join(["* \"{0}\"".format(l) for l in moaapi.templateList()])

        if env["method"]=="PUT":
            job_template=env["params"]["template"]

            if "title" in env["params"]:
                job_title=env["params"]["title"].strip()
            else:
                job_title=None

            if not (job_template in moaapi.templateList()):
                output_error("The template you specified does not exist."+err_string)

        if env["method"]=="GET":
            job_info=moaapi.getInfo(path)

            output_json_headers(0)
            rw.end_header_mode()
            rw.send(json.dumps(add_timestamp(job_info, 0)))
        else:
            moaapi.removeMoaFiles(path)

            if env["method"]=="PUT":
                moaapi.newJob(job_template, job_title, path, [], False)
                output_action_message(True, "Created new Moa job.")
            else:
                output_action_message(True, "Removed Moa job.")




    ## ls Command ##

    elif command=="ls":
        api_ls.run(args, env, path)




    ## s Command ##

    elif command=="s":
        
        if env["method"]=="GET":
            s_info={}

            s_path=os.path.relpath(path, wwwmoa.env.get_content_dir())

            if os.path.isdir(path):
                s_info["location"]=rl.get_api("ls", s_path)
                s_info["size"]=-1
                s_info["mimetype"]=""
            else:
                s_info["location"]=rl.get_direct(s_path)
                s_info["size"]=os.path.getsize(path)
                s_info["mimetype"]=mimetype.guess_from_file(path)

            output_json_headers(0)
            rw.end_header_mode()
            rw.send(json.dumps(add_timestamp(s_info, 0)))

        elif env["method"]=="PUT" or env["method"]=="POST":
            try:
                s_multipart=(env["params"]["multipart"]=="1")
            except KeyError:
                s_multipart=False

            s_contents=cgiex.get_request_body()
            
            if s_multipart:
                s_store=cgi.FieldStorage(StringIO.StringIO(s_contents))

                s_contents=s_store.getfirst("file")
                

            if env["method"]=="PUT":
                s_file=open(path, "wb")
                s_file.write(s_contents)
                s_file.close()

                output_action_message(True, "The file has been updated.")
            else:
                s_path=os.path.join(path, env["params"]["name"])
                
                if not os.path.samefile(os.path.dirname(s_path), path):
                    output_action_message(False, "The specified name does not meet restrictions.")

                try:
                    s_dir=(env["params"]["directory"]=="1")
                except KeyError:
                    s_dir=False

                if os.access(s_path, os.F_OK):
                    output_action_message(False, "The file or directory you attempted to create already exists.")
                else:
                    if s_dir:
                        os.mkdir(s_path)
                        
                        output_action_message(True, "The directory has been created.")
                    else:
                        s_file=open(s_path, "wb")
                        s_file.write(s_contents)
                        s_file.close()
                        
                        output_action_message(True, "The file has been created.")
                

        elif env["method"]=="DELETE":
            if os.path.isdir(path):
                shutil.rmtree(path)
                output_action_message(True, "Deleted directory (and its contents).")
            else:
                os.unlink(path)
                output_action_message(True, "Deleted file.")




    ## preview Command ##

    elif command=="preview":
        try:
            piece_offset=int(env["params"]["offset"])
        except (KeyError, ValueError):
            piece_offset=0

        try:
            piece_size=int(env["params"]["size"])
        except (KeyError, ValueError):
            piece_size=1024

        if piece_size<0 or piece_offset<0:
            output_error("One or more of the parameter values you passed are out of range.")

        if piece_size>65536:
            output_error("The size you specified exceeds the limit of 64 KiB.")

        output_json_headers(0)
        rw.end_header_mode()

        piece={}

        # Note: We will create the preview as if the file was encoded using the
        # ISO-8859-1 / Latin-1 character encoding.

        piece_file=open(path, "rb")
        piece_file.seek(piece_offset)
        piece["contents"]=piece_file.read(piece_size).replace("\0", "?")
        piece_file.close()

        piece["mimetype"]=mimetype.guess_from_file(path)
        
        rw.send(json.dumps(add_timestamp(piece, 0), encoding="latin-1"))


    ## help Command ##

    elif command=="help":
        rw.send_header("Content-Type", "text/html")
        rw.end_header_mode()

        if "command" in env["params"]:
            rw.send(apidoc.getCommandDoc(env["params"]["command"], apidoc.FORMAT_HTML))
        else:
            rw.send(apidoc.getCommandsDoc(apidoc.FORMAT_HTML))




    ## All Other Commands ##

    else:
        output_error("\
Something very unexpected occurred, and your command was not handled.  \
This was almost certainly due to a bug in the API system.")
