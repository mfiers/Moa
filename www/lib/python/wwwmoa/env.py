import os
import xml.sax
import os.path

from wwwmoa.formats.html import error
from wwwmoa import cgiex
from wwwmoa import info
import wwwmoa.info.moa as moainfo

_loaded_cleanly=False
_loading_failed=False
_path=None
_readonly=None


## Custom XML Handler ##

class EnvHandler(xml.sax.handler.ContentHandler):
    def startElement(this, name, attr):
        global _path
        global _readonly

        try:
            if name=="content":
                _path=attr["path"]
            elif name=="access":
                _readonly=(attr["write"]!="true")
        except KeyError:
            pass

    def endDocument(this):
        global _path
        global _readonly
        global _loaded_cleanly
        global _loading_failed

        _loaded_cleanly=(_path!=None) and (_readonly!=None)
        _loading_failed=not _loaded_cleanly


## Main Logic ##
       
_request_port=cgiex.get_request_port() # find the request port, since this
                                       # is what we use to identify an env

try:
    if _request_port!=-1: # if the request port could be found
        _env_file=os.path.join(moainfo.get_base(True), "etc/www/env/"+str(_request_port)+".xml")
    
        if not os.access(_env_file, os.R_OK): # if there is not a readable env configuration
            _loading_failed=True # we cannot possibly load the env
        else: # if a env configuration is available
            _handler=EnvHandler() # create a handler
            xml.sax.parse(_env_file, _handler) # parse the configuration
    else: # if the request port could not be found
        _loading_failed=True # we cannot possibly load the env
except MoaNotFoundError:
    _loading_failed=True

## Triggers an HTTP level error if the environment did not load properly.
def require_environment():
    global _loading_failed

    if _loading_failed:
        error.throw_fatal_error("Environment Failure", "I cannot continue, because the environment for " + info.get_name()+" could not be loaded.  Loading this environment is important, as it includes important resources like your personal content files.\n\nIf your "+info.get_name() +" installation is managed by technical support staff, please let them know you received this message.") 

## Returns the server-side file system root path, which may or may not be absolute.  The return path always ends with a slash. Returns None if the environment was not loaded successfully.
def get_content_dir():
    global _path
    global _loaded_cleanly

    if _loaded_cleanly: # if we were able to load the environment
        return _path # return the path
    else: # if we were not able to load the environment
        return None # return None as per specs

## Returns whether or not the env is read-only.
## Returns None if the environment was not
## loaded successfully.
def is_readonly():
    global _readonly
    global _loaded_cleanly

    if _loaded_cleanly: # if we were able to load the environment
        return _readonly # return the read-only flag
    else: # if we were not able to load the environment
        return None # return None as per specs
