### WWWMoa ###############################
### RL / Resource Locator Lookup


## Imports ##
import urllib # will use this for URL encoding

## RL Lookup Functions ##

## Returns the absolute pathname of the psuedo-root directory that WWWMoa will use.  Always ends with a slash.
def get_pre():
    return "/"

## Returns the relative pathname of the home page for WWWMoa.
def get_home():
    return get_pre()+"index.py"

## Returns the relative pathname of the help page for WWWMoa.
def get_help():
    return get_pre()+"help.py"

## Returns the relative pathname of an image for WWWMoa.
def get_image(rrl):
    return get_pre()+"images/"+rrl

## Returns the relative pathname of a stylesheet for WWWMoa.
def get_style(rrl):
    return get_pre()+"styles/"+rrl

## Returns the relative pathname of a web script for WWWMoa.
def get_script(rrl):
    return get_pre()+"scripts/"+rrl

## Returns the relative pathname of a API command for WWWMoa, given the commands name and the file system path it operates on (optional).
def get_api(command, path=None):
    if path==None: # if the path was not passed
        path_notnone="" # assume that it was an empty string
    else: # otherwise
        path_notnone=path # use the path that was passed

    fragment=url_encode(path_notnone.strip("/")) # generate the fragment that contains the path
    
    if len(fragment)!=0: # if the fragment is not empty
        fragment+="/" # add a seperator as appropriate

    return get_pre()+"api/"+fragment+command

## Returns a relative pathname that can be used for direct access to a file in the content directory.
def get_direct(path):
    return get_pre()+"direct/"+url_encode(path.strip("/"))

## Performs a standard URL encoding.
def url_encode(txt):
    return urllib.quote(txt)

## Performs the inverse operation of url_encode().
def url_decode(txt):
    return urllib.unquote(txt)
