### WWWMoa ###############################
### Env / Operating Environment



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

class EnvHandler(xml.sax.handler.ContentHandler):
    def startElement(this, name, attr):
        global _path

        if name=="content":
            _path=attr["path"]

    def endDocument(this):
        global _path
        global _loaded_cleanly
        global _loading_failed

        _loaded_cleanly=(_path!=None)
        _loading_failed=not _loaded_cleanly

       
_request_port=cgiex.get_request_port()

if _request_port!=-1 and moainfo.get_base()!=None:
    _env_file=os.path.join(moainfo.get_base(), "etc/www/env/"+str(_request_port)+".xml")
    
    if not os.access(_env_file, os.R_OK):
        _loading_failed=True
    else:
        _handler=EnvHandler()
        xml.sax.parse(_env_file, _handler)
else:
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
