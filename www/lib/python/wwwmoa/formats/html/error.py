### WWWMoa ###############################
### HTMLError / Verbose Error Handling


## Imports ##
from wwwmoa.formats import html
from wwwmoa import info
from wwwmoa import rw

import datetime
import os

## Error Handlers ##

## Outputs an HTML message for an error. The "isinternal" parameter can be set to True to indicate that the error came from within one of the WWWMoa libraries, as opposed to a resource that referenced them.
def throw_fatal_error(title, summary, isinternal=False):
    # finish sending headers
    rw.send_header("Cache-Control", "no-cache") # it is very likely that the output will be different later, since an error occured
    rw.send_header("Expires", "0") # required for old browsers
    rw.send_header("Content-Type", "text/html") # this is an HTML message
    rw.send_status(500)
    rw.end_header_mode() # now it is time to send the body, so end header mode

    escaped_title=html.fix_text(title) # fix the title for use in HTML
    escaped_summary=html.translate_text(summary) # fix the summary for use in HTML


    # start document

    rw.send("""<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">

""")


    rw.send("""<html>

<head>

<title>"""+escaped_title+"""</title>

</head>

""")


    # send main info

    rw.send("""<body style=\"background-color:#808080; color:#000000; font-family:serif; font-weight:bold; font-size:12pt\">

<div style=\"border:1px solid #000000; background-color:#FFFFD0; padding:6px 4px 32px 4px\">

<span style=\"font-size:24pt; text-decoration:underline\">"""+escaped_title+"""</span>

<br><br>

"""+escaped_summary+"""

<br><br>

<hr>

<br>

Below is some information to help with debugging.

<br>

""")

    # attempt to send debugging info

    try: # try to retrieve and send time
        dt=datetime.datetime.now()

        rw.send(html.translate_text("Time: " + str(dt.hour)+":"+str(dt.minute).rjust(2,"0")+":"+str(dt.second).rjust(2,"0")+"\n"))
    except: # if we cannot, we just pass 
        pass

    try: # try to send version of software
        rw.send(html.translate_text("Release: " + info.get_string() + "\n"))
    except: # if we cannot, we just pass
        pass

    try: # try to send Python version information
        rw.send(html.translate_text("Python OS Module: " + os.name + "\n"))
    except: # if we cannot, we just pass
        pass

    # end body
    rw.send("""
</div>

</body>

</html>""")

    # finish sending document
    
    rw.terminate()
