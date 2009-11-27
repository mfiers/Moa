### WWWMoa ###############################
### Mod_HM / Helper Module Interface
### Version: 0.1
### Date: November 20, 2009

## Imports ##
from wwwmoa import rw
from wwwmoa import rl
import wwwmoa.env
from wwwmoa.formats.html import error
import os.path
import json
import time

## Helper Functions ##

## Figures out whether or not a given path is equivalent to the psuedo-root directory.
def is_root(path):
    return os.path.samefile(wwwmoa.env.get_content_dir(), path)

## Figures out whether or not a given path is within the psuedo-root directory.
def in_root(path):
    return os.path.samefile(os.path.commonprefix([path, wwwmoa.env.get_content_dir()]), wwwmoa.env.get_content_dir())

## Outputs a custom error message.
def output_error(err):
    error.throw_fatal_error("Helper Module Server-Side Failure", "The server-side code for a helper module has failed.  More details can be found below.\n\n" + err)


## Main Interface Logic ##

def run(args=None, env=None):
    
    if (args==None) or (env==None):
        output_error("An unexpected error has occurred.")

    # check to make sure we have enough parameters
    if len(args)<1: # if there is not at least one parameter
        output_error("The helper module request you made cannot be completed, because you did not supply enough information.")

    # extract the name and argument list
    name=rl.url_decode_x(args[len(args)-1])
    if len(args)>=2: # if there was an argument list sent
        argument_array=args[:len(args)-1] # the subset of elements that would determine the argument list are all except for the last one
    else: # if there was not an argument list sent
        argument_array=[] # the element array is empty

    if name=="fsbrowser": # if a FSBrowse helper module is requested
        import wwwmoa.hm.fsbrowser as helper_module # import the associate module
    else: # if the helper module could not be found
        output_error("The helper module you requested could not be found.") # say so

    # run helper module code
    helper_module.run(argument_array, env)
