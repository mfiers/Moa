
## Imports ##

from wwwmoa import rw
from wwwmoa import rl

import wwwmoa.env
from wwwmoa.formats.html import error
import wwwmoa.info.moa as moainfo
import moa.api as moaapi
import moa.dispatcher as dispatcher

import os
import os.path
import json
import time
import sys
import stat
import subprocess

from wwwmoa.api import output_error
from wwwmoa.api import in_root
from wwwmoa.api import is_root
from wwwmoa.api import add_timestamp
from wwwmoa.api import output_json_headers

## Main Interface Logic ##

def run(args=None, env=None, path=None):

    (command_min, command_max)=(None, None) # we will start off by assuming that a valid min and max was NOT passed
    (command_filter, command_filter_type, command_filtered)=(None, None, False)

    try:
        command_filter=env["params"]["filter"]
        command_filter_type=env["params"]["filter-type"]

        if command_filter_type==None:
            raise

        if command_filter==None:
            raise

        if "filter-ignorecase" in env["params"]:
            command_filter_sensitive=(env["params"]["filter-ignorecase"]!="1")
        else:
            command_filter_sensitive=True

        command_filter=command_filter.strip()
        command_filter_type=command_filter_type.strip().lower()
        
        if command_filter_type!="exactly" and command_filter_type!="contains":
            raise

        command_filtered=True

    except:
        (command_filter, command_filter_type)=(None, None)

    try: # the inputs may be invalid (or non-existant), so we need to be careful
        command_min=int(env["params"]["start"]) # attempt to retrieve min
        command_max=int(env["params"]["end"]) # attempt to retrieve max
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
                                    "x-is-moa" : moaapi.isMoaDir(path_exploded_current)
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
    ls_filter=[]


    if command_filtered:
        if command_filter_type=="contains":
            if command_filter_sensitive:
                for l in ls:
                    if l.find(command_filter)!=-1:
                        ls_filter.append(l)
            else:
                for l in ls:
                    if l.lower().find(command_filter.lower())!=-1:
                        ls_filter.append(l)

        if command_filter_type=="exactly":
            if command_filter_sensitive:
                for l in ls:
                    if l==command_filter:
                        ls_filter.append(l)
            else:
                for l in ls:
                    if l.lower()==command_filter.lower():
                        ls_filter.append(l)

        ls=ls_filter


    # before we cut out some entries, we should capture the size of the listing
    ls_total_count=len(ls)

    if not command_min==None and not command_max==None: # if the min and max are valid
        ls=ls[command_min-1:command_max] # cut the list in accordance with this min and max

        
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
                           "x-is-moa" : moaapi.isMoaDir(l_complete)
                           })
        
    # add both lists to paliminary final list
    ls_final.extend(ls_dir) # dirs go first
    ls_final.extend(ls_file) # files go last



    output_json_headers(0) # out appropriate headers
    rw.end_header_mode() # get ready to send response

    rw.send(json.dumps(add_timestamp({ # send response
                "dir" : path_exploded_final, # the dir path components
                "x-dir-is-moa" : moaapi.isMoaDir(path),
                "ls" : ls_final, # the final listing
                "ls-available" : ls_total_count, # the total number of entries that are potentially available
                "ls-returned" : len(ls_final), # the total number of entries that we returned
                "ls-filtered" : command_filtered
                }, 0))) # the ttl is 0
