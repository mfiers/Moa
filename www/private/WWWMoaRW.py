### WWWMoa ###############################
### RW / Low-level Output Handlers
### Version: 0.1
### Date: November 18, 2009

## Imports ##
import sys # will use for string outputs
import cgi # will use for input parameter processing


## State / Buffer Variables ##
_request_params=cgi.FieldStorage() # _request_params will hold the input parameter object at import time
_in_header_mode=True # keeps track of whether we are in "header mode" or not

## Output Handlers ##

## Sends an arbitrary string to the output.
def send(str):
    sys.stdout.write(str)

## Sends a single linefeed character ("\n") to the output.
def send_linefeed():
    send("\n")

## Sends two linefeed characters ("\n\n") to the output.
def send_doublelinefeed():
    send_linefeed()
    send_linefeed()

## Ensures that the data sent using send() will not be interpreted as a header, but the actual body of the HTTP response.
def end_header_mode():
    global _in_header_mode

    send_linefeed() # a blank line will do the trick

    _in_header_mode=False # we are no longer in header mode

## Sends a header with a given name and value to the output.  If not in header mode, the function call will be ignored.
def send_header(name, value):
    global _in_header_mode

    if not _in_header_mode:
        return

    send(name)
    send(": ")
    send(value)
    send_linefeed()

## Sends a given HTTP status code.  If not in header mode, the functionc all will be ignored.
def send_status(id, brief=""):
    send_header("Status", str(int(id))+" "+brief)

## Returns a string with the contents of a given request parameter.  Note that an empty string will be returned if not such parameter was sent.
def get_request_param(name):
    global _request_params # we have already processed the request parameters

    return _request_params.getfirst(name,"") # locate the first request parameter with the given name

## Terminates the current script.
def terminate():
    sys.exit()

## Returns whether or not the output is in "header mode".
def is_in_header_mode():
    global _in_header_mode

    return _in_header_mode
