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

    return get_pre()+"api/"+fragment+url_encode_x(command)

## Returns the relative pathname of a helper module for WWWMoa, given the helper modules name and argument list (optional).
def get_hm(name, args=[]):
    args_fixed=[] # create buffer for fixed arguments
    for a in args: # for each argument
        args_fixed.append(url_encode_x(a)) # fix it

    fragment=url_encode("/".join(args_fixed)) # generate the argument fragment

    if len(fragment)!=0: # if the fragment is not empty
        fragment+="/" # add a seperator as appropriate

    return get_pre()+"hm/"+fragment+url_encode_x(name)

## Performs a standard URL encoding.
def url_encode(txt):
    return urllib.quote(txt)

## Performs the inverse operation of url_encode().
def url_decode(txt):
    return urllib.unquote(txt)

## Performs a modified version of URL encoding so that "/" will not be present in the output string.  In addition, special characters are escaped with "%" as in a usual url encoding process.
def url_encode_x(txt):
    return urllib.quote(txt.replace("@","@@").replace("/","@x"))

## Performs the inverse operation of url_encode_x().
def url_decode_x(txt):
    return urllib.unquote(txt).replace("@x", "/").replace("@@", "@")
