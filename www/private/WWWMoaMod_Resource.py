### WWWMoa ###############################
### resource.cgi
### Version: 0.1
### Date: November 18, 2009

## Imports ##

import os # used to access file system
import WWWMoaRW # used to output arbitrary buffers
import WWWMoaHTMLError # used for error messages
import sys
## Helper Functions ##

def file_exists(path):
    return os.access(path,os.R_OK)

def output_error(err):
    WWWMoaHTMLError.throw_fatal_error("Resource Accessing Error", err)

def request_no_cache():
    WWWMoaRW.send_header("Cache-Control", "no-cache") # ask the browser not to cache resource
    WWWMoaRW.send_header("Expires", "0") # ask older browsers not to cache resource

def request_short_cache():
    WWWMoaRW.send_header("Cache-Control", "max-age=3600")


## Main Execution ##

def run(args = None, env = None):
    # check that required inputs exist
    if (args==None) or (env==None): # if not all required inputs exist
        output_error("An unexpected error occured.") # say so

    if len(args)<2: # if we do not have enough arguments
        output_error("You must specify both an id and a type.") # say so

    if env["method"]!="GET":
        output_error("You can only read the contents of the resource you requested.")

    # retrieve and process needed parameters
    id=args[1].strip() # trim whitespace
    type=args[0].strip().lower() # trim whitespace and make lowercase

    # check to make sure both processed parameters are alpha numeric strings with length greater than one
    if (not id.isalnum()) or (not type.isalnum()): # if a parameter problem is found
        output_error("The id or type you submitted is invalid.  All resource ids and types must be alpha-numeric strings of with a length of at least 1 character.") # show error message

    # start building relative path
    path="../media/"
    path2=""

    # set default mime-type value
    mime="text/plain"

    # set default file extension value
    extension=""

    # we will assume the file exists, and that the type is recognized
    exists=True
    typerec=True

    if type=="styles": # if type is style
        path2=path+"styles/"+id+".css" # we know the path will be this
        mime="text/css" # all styles will by CSS stylesheets

        if not file_exists(path2): # if the file does not exist
            exists=False # remeber that it does not exist
    elif type=="images": # if type is image
        path+="images/"+id # start building path, but leave off extension for the moment

        path2=path+".png" # make path for PNG
        mime="image/png" # set mimetype accordingly

        if not file_exists(path2): # if PNG does not exist
            path2=path+".gif" # make path for GIF
            mime="image/gif" # set mimetype accordingly
        if not file_exists(path2): # if GIF does not exist
            path2=path+".jpg" # make path for JPEG
            mime="image/jpeg" # set mimetype accordingly
        if not file_exists(path2): # if JPEG does not appear to exist at first
            path2=path+".jpeg" # try alternative pathname
        if not file_exists(path2): # if JPEG does not exist
            exists=False # no image file exists, so remember that it does not exist
    elif type=="scripts":
        path="../js/"

        # [!] Note: There is a special link in for wwwmoa.
        if id=="wwwmoa":
            import WWWMoaMod_JSCore

            WWWMoaMod_JSCore.run()        

        path2=path+id+".js"
        mime="text/javascript"

        if not file_exists(path2):
            exists=False
    else: # if type not recognized so far
        typerec=False # we will never recognize it

    if (not exists) or (not typerec): # if the file does not exist or the type is not recognized
        output_error("The resource you attempted to access could not be found.") # show error message

    # finish up HTTP headers
    WWWMoaRW.send_header("Content-Type", mime) # tell browser what type of file it is

    if type=="images":
        request_short_cache()
    else:
        request_no_cache()

    WWWMoaRW.end_header_mode() # end header mode

    # read file contents
    file=open(path2, "r") # open file
    buff=file.read() # read entire file into memory
    file.close() # close file

    if mime=="text/css":
        pass #buff=buff.replace("\x0A", "\x0D\x0A")

    WWWMoaRW.send(buff) # send file contents

    WWWMoaRW.terminate() # terminate script

