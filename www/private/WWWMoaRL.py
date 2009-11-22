### WWWMoa ###############################
### RL / Resource Locator Lookup
### Version: 0.1
### Date: November 18, 2009

## Imports ##
import urllib # will use this for URL encoding


## RL Lookup Functions ##

## Returns the absolute pathname of the psuedo-root directory that WWWMoa will use.  Always ends with a slash.
def get_base():
    return "/"

## Returns the absolute pathname of the directory that is to be used for magic queries.  Always ends with a slash.
def get_magic_base():
    return get_base()+"moa/"

## Returns the absolute pathname of the directory that is to be used for hm queries.  Always ends with a slash.
def get_hm_base():
    return get_magic_base()+"hms/"

## Returns the relative pathname of the home page for WWWMoa.
def get_home():
    return get_base()+"index.py"

## Returns the relative pathname of the help page for WWWMoa.
def get_help():
    return get_base()+"help.py"

## Returns the relative pathname of an image for WWWMoa.
def get_image(id):
    return get_magic_base()+"resources/images/"+url_encode_x(id)

## Returns the relative pathname of a stylesheet for WWWMoa.
def get_style(id):
    return get_magic_base()+"resources/styles/"+url_encode_x(id)

## Returns the relative pathname of a web script for WWWMoa.
def get_script(id):
    return get_magic_base()+"resources/scripts/"+url_encode_x(id)


## Performs a modified version of URL encoding so that "/" will not be present in the output string.  In addition, special characters are escaped with "%" as in a usual url encoding process.
def url_encode_x(txt):
    return urllib.quote_plus(txt.replace("@","@@").replace("/","@x"))

## Performs the inverse operation of url_encode_slash().
def url_decode_x(txt):
    return urllib.unquote_plus(txt).replace("@x", "/").replace("@@", "@")
