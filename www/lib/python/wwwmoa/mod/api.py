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


## Main Interface Logic ##

def run(args=None, env=None):
    
    if (args==None) or (env==None):
        output_error("An unexpected error has occurred.")


    moa_pylib_base=moainfo.get_pylib_base()

    if moa_pylib_base==None:
        output_error("A Moa implementation could not be found.")
    else:
        sys.path.append(moa_pylib_base)
        from moa import dispatcher
    
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

    path=os.path.join(wwwmoa.env.get_content_dir(), content_path) # get the complete pathname

    path=os.path.normpath(path) # make path as simple as possible

    if os.path.islink(path): # if the path is actually a symb link
        path=os.path.realpath(path) # find what the path really points to

    # make sure requested path is safe
    
    if not in_root(path): # if the requested path is not in the psuedo-root directory
        error.throw_fatal_error("Access Denied", "The directory you attempted to access cannot be, because you do not have the permission to do so.") # say so
    
    if not os.path.isdir(path): # if the request path does not exist
        error.throw_fatal_error("Target Not Found", "The directory you attempted to access cannot be, because the directory does not exist.") # say so

    if command=="ls" or command[:3]=="ls-": # if we are dealing with an ls request
        command_exploded=command.partition("-") # break the command into pieces
        
        (command_min, command_max)=(None, None) # we will start off by assuming that a valid min and max was NOT passed

        if command_exploded[1]=="-": # if the command contained a "-" seperator
            command_minmax=command_exploded[2].partition("to") # break the piece after the "-" seperator (the parameter)
            
            if command_minmax[1]=="to": # if the piece contained a "to" seperator
                try: # the inputs may be invalid, so we need to be careful
                    command_min=int(command_minmax[0]) # attempt to retrieve min
                    command_max=int(command_minmax[2]) # attempt to retrieve max
                except: # on conversion failure
                    (command_min, command_max)=(None, None) # reset min and max
                else: # on conversion success, do sanity check
                    if command_min>command_max: # if min is ever greater than max
                        (command_min, command_max)=(None, None) # reset min and max
            
                    if command_min<1 or command_max<1: # if min or max is less than one (min and max are based at 1)
                        (command_min, command_max)=(None, None) # reset min and max

        # create a list of the path components for the requested directory
        path_exploded=[] # start with no components in list
        path_exploded_current=path # start with the full directory
        path_exploded_str=[] # start with no components in the list
        path_exploded_str_current="" # start with zero length string
        path_exploded_final=[] # start with no components in the list
        while not is_root(path_exploded_current): # while we have not reached the root
            (path_exploded_current_h, path_exploded_current_t)=os.path.split(path_exploded_current) # skim off the next path component
            path_exploded.append(path_exploded_current_t) # add the component to the list

            path_exploded_str.append(os.path.join(path_exploded_current_t, path_exploded_str_current)) # append the path name
            path_exploded_str_current=path_exploded_str[len(path_exploded_str)-1] # remember this last path name


            path_exploded_final.append({"name" : path_exploded_current_t, # the name of the dir
                                        "size" : -1, # -1 since this is a dir [!] Note: This may be changed to the size of the directory contents in the future.
                                        "link" : os.path.islink(path_exploded_current), # whether or not the dir is a link
                                        "type" : "dir", # that it is a dir
                                        "read-allowed" : in_root(path_exploded_current) and os.access(path_exploded_current, os.R_OK), # whether or not we will be able to read it using other API calls
                                        "write-allowed" : in_root(path_exploded_current) and os.access(path_exploded_current, os.W_OK), # whether or not we will be able to write it using other API calls
                                        "path" : "", # path for later access, since simple concat may not work well
                                        "x-is-moa" : dispatcher.isMoa(path_exploded_current)
                                        })

            for p in path_exploded_final: # for each entry in the final dir path listing
                if p["path"]!="": # if the path has been started before this cycle
                    p["path"]=os.path.join(path_exploded_current_t, p["path"]) # add the appropriate path element to it
                else: # if the path has just been started
                    p["path"]=path_exploded_current_t # use it without joining it to anything

            path_exploded_current=path_exploded_current_h # now we will deal with the rest of the path

        path_exploded.reverse() # reverse the listing so that it will be in correct order
        path_exploded_str.reverse() # reverse the path listing so that it will be in correct order
        path_exploded_final.reverse() # reverse the final "rich" listing so that it will be in correct order
        


        # create directory listing
        ls=os.listdir(path) # get raw listing
        ls.sort() # sort the listing (alpha and ascending)
        
        ls_file=[] # create list that will contain just the files
        ls_dir=[] # create list that will contain just the dirs
        ls_final=[] # create the final list that will be sent back to the user
        
        for l in ls: # for each entry in the raw directory listing
            l_complete=os.path.join(path,l) # create the full pathname for the entry

            if os.path.isfile(l_complete): # if the entry is a file
                try: # attempt to get its size
                    l_size=os.path.getsize(l_complete)
                except: # on failure to get size
                    l_size=-1 # return -1 to signify an "undefined" size
                
                # to the file list append
                ls_file.append({"name" : l, # the name of the file
                                "size" : l_size, # the size of the file (or -1)
                                "link" : os.path.islink(l_complete), # whether or not the file is a link
                                "type" : "file", # that it is a file
                                "read-allowed" : in_root(l_complete) and os.access(l_complete, os.R_OK), # whether or not we will be able to read it using other API calls
                                "write-allowed" : in_root(l_complete) and os.access(l_complete, os.W_OK), # whether or not we will be able to write it using other API calls
                                "path" : os.path.join(path_exploded_str_current, l), # path for later access, since simple concat may not work well
                                "x-is-moa" : False
                                })
            elif os.path.isdir(l_complete): # if the entry is a dir
                ls_dir.append({"name" : l, # the name of the file
                               "size" : -1, # -1 since this is a dir [!] Note: This may be changed to the size of the directory contents in the future.
                               "link" : os.path.islink(l_complete), # whether or not the dir is a link
                               "type" : "dir", # that it is a dir
                               "read-allowed" : in_root(l_complete) and os.access(l_complete, os.R_OK), # whether or not we will be able to read it using other API calls
                               "write-allowed" : in_root(l_complete) and os.access(l_complete, os.W_OK), # whether or not we will be able to write it using oher API calls
                               "path" : os.path.join(path_exploded_str_current, l), # path for later access, since simple concat may not work well
                               "x-is-moa" : dispatcher.isMoa(l_complete)
                               })
        
        # add both lists to paliminary final list
        ls_final.extend(ls_dir) # dirs go first
        ls_final.extend(ls_file) # files go last

        # before we cut out some entries, we should capture the size of the listing
        ls_total_count=len(ls_final)

        if not command_min==None and not command_max==None: # if the min and max are valid
            ls_final=ls_final[command_min-1:command_max] # cut the list in accordance with this min and max



       
        rw.send_header("Content-Type", "application/json") # we will be sending JSON
        rw.send_header("Cache-Control", "no-cache") # this response should NOT be cached
        rw.send_header("Expires", "0") # some older browsers need this to not cache a response
        rw.end_header_mode() # get ready to send response

        rw.send(json.dumps({ # send response
                    "dir" : path_exploded_final, # the dir path components
                    "x-dir-is-moa" : dispatcher.isMoa(path),
                    "ls" : ls_final, # the final listing
                    "ls-available" : ls_total_count, # the total number of entries that are potentially available
                    "ls-returned" : len(ls_final), # the total number of entries that we returned
                    "timestamp" : time.time(), # the time stamp
                    "ttl" : 0 # how long we should cache this response (never cache)
                    }))
       
    else: # if the request type is unknown
        output_error("The specific API request you made is not supported.") # say so

