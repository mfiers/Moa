### WWWMoa ###############################
### HTML / Light-weight HTML Utilities
### Version: 0.1
### Date: November 18, 2009

## Imports ##
from wwwmoa import rw # used in convience methods that directly send HTML code
import cgi # used to make arbitrary text safe


## State / Buffer Variables ##

_use_xhtml=False # selects whether XHTML syntax should be used


## Toggle Functions ##

## Instructs the library to output code using XHTML syntax.
def use_xhtml():
    global _use_xhtml

    _use_xhtml=True



## HTML Utility Functions ##

## Generates the HTML code for an "open" tag with a given tag name.  This function is a light-weight version of get_tag_open(), and does not accept additional parameters.
def get_simple_tag_open(tagname):
    return "<" + tagname + ">"

## Generates the HTML code for a "close" tag with a given tag name.  This function is a light-weight version of get_tag_close(), and does not accept additional parameters.
def get_simple_tag_close(tagname):
    return "</" + tagname + ">"

## Generates the HTML code for a "stand-alone" tag with a given tag name.  This function is a light-weight version of get_tag(), and does not accept additional parameters.
def get_simple_tag(tagname):
    global _use_xhtml # we need to find what state we are int

    tag="<" + tagname # tags always start like this

    if _use_xhtml: # if we are in XHTML mode
        tag+=" /" # tags have this

    tag+=">" # tags always end like this

    return tag

## Generates the HTML code for an "open" tag with a given tag name and a list of parameters.  The values of the parameters are made safe using HTML entities.
def get_tag_open(tagname, tagdict):
    return _get_tag_unended(tagname, tagdict)+">"

## Internal function to generate most of a tag, but without a "tail".  Do not use this method directly!
def _get_tag_unended(tagname, tagdict):
    tag="<"+tagname # tag always starts this way
    
    keys=tagdict.keys() # detect what parameters are being used
    
    for key in keys: # for each parameter
        tag+=" " # add nessesary spacing
        tag+=key+'="' # add nessesary syntax elements
        tag+=cgi.escape(tagdict[key], True) # add "escaped" version of parameter value
        tag+='"' # add nessesary syntax element
    
    return tag

## Generates the HTML code for a "close" tag with a given tag name.
def get_tag_close(tagname):
    return get_simple_tag_close(tagname) # this is a wrapper for get_simple_tag_close(), and is included for logical consistency.

## Generates the HTML code for a "stand-alone" tag with a given tag name and list of parameters.  The values of the parameters are made safe using HTML entities.
def get_tag(tagname, tagdict):
    global _use_xhtml # we need to find what state we are in

    tag=_get_tag_unended(tagname, tagdict) # get a large piece of the tag

    if _use_xhtml: # if we are in XHTML mode
        tag+=" /" # tags have this

    tag+=">" # tags always end like this

    return tag

## Generates the HTML code for a tag that adds a linefeed.
def get_linefeed_tag():
    return get_simple_tag("br") # might as well use light-weight version for this


## Convienance Functions ##

## Convienance function that outputs the result of get_simple_tag_open().
def send_simple_tag_open(tagname):
    rw.send(get_simple_tag_open(tagname))

## Convienance function that outputs the result of get_simple_tag_close().
def send_simple_tag_close(tagname):
    rw.send(get_simple_tag_close(tagname))

## Convienance function that outputs the result of get_tag_open().
def send_tag_open(tagname, tagdict):
    rw.send(get_tag_open(tagname, tagdict))

## Convienance function that outputs the result of get_tag_close().
def send_tag_close(tagname):
    rw.send(get_tag_close(tagname))

## Convienance function that outputs the result of get_simple_tag().
def send_simple_tag(tagname):
    rw.send(get_simple_tag(tagname))

## Convienance function that outputs the result of get_tag().
def send_tag(tagname, tagdict):
    rw.send(get_tag(tagname,tagdict))

## Convienance function that outputs the result of get_linefeed_tag().
def send_linefeed_tag():
    rw.send(get_linefeed_tag())


## HTML Safeguarding Functions ##

## Makes arbitrary text safe for inclusion in an HTML document.  Ensures quotes are made safe as well.
def fix_text(text):
    return cgi.escape(text, True)

## Makes arbitrary text safe for inclusion in an HTML document, and translates linefeeds appropriatly.
def translate_text(text):
    return fix_text(text).replace("\r", "").replace("\n", get_linefeed_tag()+"\n")
