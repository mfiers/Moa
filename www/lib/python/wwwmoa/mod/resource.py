### WWWMoa ###############################
### resource.cgi
### Version: 0.1
### Date: November 18, 2009

## Imports ##

import os # used to access file system
import os.path
from wwwmoa import rw # used to output arbitrary buffers
from wwwmoa.formats.html import error # used for error messages
from wwwmoa.formats.mime.type import guess_from_filename # used for mimetype lookups
import sys

## Helper Functions ##

def file_exists(path):
    return os.access(path,os.R_OK)

def output_error(err):
    error.throw_fatal_error("Resource Accessing Error", err)

def request_no_cache():
    rw.send_header("Cache-Control", "no-cache") # ask the browser not to cache resource
    rw.send_header("Expires", "0") # ask older browsers not to cache resource

def request_short_cache():
    rw.send_header("Cache-Control", "max-age=3600")

## State Variables ##

_file_dir=os.path.dirname(__file__)

## Main Execution ##

def run(args = None, env = None):
    global _file_dir

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
    path=os.path.join(_file_dir, "../../../../static/")
    path2=""

    # we will assume the file exists, and that the type is recognized
    exists=True
    typerec=True

    if type=="styles": # if type is style
        path2=path+"styles/"+id+".css" # we know the path will be this

        if not file_exists(path2): # if the file does not exist
            exists=False # remeber that it does not exist
    elif type=="images": # if type is image
        path+="images/"+id # start building path, but leave off extension for the moment

        path2=path+".png" # make path for PNG

        if not file_exists(path2): # if PNG does not exist
            path2=path+".gif" # make path for GIF
        if not file_exists(path2): # if GIF does not exist
            path2=path+".jpg" # make path for JPEG
        if not file_exists(path2): # if JPEG does not appear to exist at first
            path2=path+".jpeg" # try alternative pathname
        if not file_exists(path2): # if JPEG does not exist
            exists=False # no image file exists, so remember that it does not exist
    elif type=="scripts":
        path="../lib/js/"

        # [!] Note: There is a special link in for wwwmoa.
        if id=="wwwmoa":
            import wwwmoa.mod.jscore

            wwwmoa.mod.jscore.run()        

        path2=path+id+".js"

        exists=file_exists(path2)
    else: # if type not recognized so far
        typerec=False # we will never recognize it

    if (not exists) or (not typerec): # if the file does not exist or the type is not recognized
        output_error("The resource you attempted to access could not be found.") # show error message
    
    # finish up HTTP headers
    rw.send_header("Content-Type", guess_from_filename(path2)) # tell browser what type of file it is

    if type=="images":
        request_short_cache()
    else:
        request_no_cache()

    rw.end_header_mode() # end header mode

    # read file contents
    file=open(path2, "r") # open file
    buff=file.read() # read entire file into memory
    file.close() # close file

    rw.send(buff) # send file contents

    rw.terminate() # terminate script

