### WWWMoa ###############################
### Mod_FS / File System Interface
### Version: 0.1
### Date: November 20, 2009

## Imports ##
import WWWMoaRW
import WWWMoaRL
import WWWMoaEnv
import WWWMoaHTMLError
import os.path

## Helper Functions ##

## Figures out whether or not a given path is equivalent to the psuedo-root directory.
def is_root(path):
    return os.path.samefile(WWWMoaEnv.get_content_dir(), path)

## Figures out whether or not a given path is within the psuedo-root directory.
def in_root(path):
    return os.path.samefile(os.path.commonprefix([path, WWWMoaEnv.get_content_dir()]), WWWMoaEnv.get_content_dir())

## Outputs a custom error message.
def output_error(err):
    WWWMoaHTMLError.throw_fatal_error("File System Server-Side Failure", "The server-side code for an action related to the file system has failed.  More details can be found below.\n\n" + err)


## Main Interface Logic ##

def run(args=None, env=None):
    
    if (args==None) or (env==None):
        output_error("An unexpected error has occurred.")

    # check to make sure we have enough parameters
    if len(args)<1: # if there is not at least one parameter
        output_error("The file system request you made cannot be completed, because you did not supply enough information.")

    # extract the command and file system path
    command=WWWMoaRL.url_decode_x(args[len(args)-1])
    if len(args)>=2: # if there was a path sent
        content_path_array=args[:len(args)-1] # the subset of elements that would determine the path are all except for the last one
        content_path=("/".join(content_path_array)) # the path is directly determined by the elements
    else: # if there was not a path sent
        content_path_array=[] # the element array is empty
        content_path="" # just return the root (which is not absolute, so it is an empty string)

    path=os.path.join(WWWMoaEnv.get_content_dir(), content_path) # get the complete pathname

    path=os.path.normpath(path) # make path as simple as possible

    if os.path.islink(path): # if the path is actually a symb link
        path=os.path.realpath(path) # find what the path really points to

    # make sure requested path is safe
    
    if not in_root(path): # if the requested path is not in the psuedo-root directory
        WWWMoaHTMLError.throw_fatal_error("Access Denied", "The directory you attempted to access cannot be, because you do not have the permission to do so.") # say so
    
    if not os.path.isdir(path): # if the request path does not exist
        WWWMoaHTMLError.throw_fatal_error("Target Not Found", "The directory you attempted to access cannot be, because the directory does not exist.") # say so

    path_viewable=os.path.relpath(path,WWWMoaEnv.get_content_dir()) # get the path that the user can see

    if command=="browsehm": # if an AJAX request for a file viewer has been made
        
        import WWWMoaMod_FS_BrowseHM
        
        WWWMoaMod_FS_BrowseHM.run_fs({"path" : path, "rel_path" : path_viewable, "content_path" : WWWMoaEnv.get_content_dir(), "request_method" : env["method"]}) # run segment of code for AJAX file viewer
    else:
        output_error("The specific file system request you made is not supported.")

