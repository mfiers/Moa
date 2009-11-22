### WWWMoa ###############################
### HTMLError / Verbose Error Handling
### Version: 0.1
### Date: November 18, 2009

## Imports ##
import WWWMoaHTML
import WWWMoaInfo
import WWWMoaRW
import datetime
import os

## Error Handlers ##

## Outputs an HTML message for an error. The "isinternal" parameter can be set to True to indicate that the error came from within one of the WWWMoa libraries, as opposed to a resource that referenced them.
def throw_fatal_error(title, summary, isinternal=False):
    # finish sending headers
    WWWMoaRW.send_header("Cache-Control", "no-cache") # it is very likely that the output will be different later, since an error occured
    WWWMoaRW.send_header("Content-Type", "text/html") # this is an HTML message
    WWWMoaRW.send_status(500)
    WWWMoaRW.end_header_mode() # now it is time to send the body, so end header mode

    escaped_title=WWWMoaHTML.fix_text(title) # fix the title for use in HTML
    escaped_summary=WWWMoaHTML.translate_text(summary) # fix the summary for use in HTML

    # start document
    WWWMoaHTML.send_simple_tag_open("html")
    WWWMoaHTML.send_simple_tag_open("head")
    WWWMoaHTML.send_simple_tag_open("title")
    WWWMoaRW.send(escaped_title)
    WWWMoaHTML.send_simple_tag_close("title")
    WWWMoaHTML.send_simple_tag_close("head")

    # send main info
    WWWMoaHTML.send_tag_open("body", {"style" : "background-color:#808080; color:#000000; font-family:serif; font-weight:bold; font-size:12pt"})
    WWWMoaHTML.send_tag_open("div", {"style" : "border:1px solid #000000; background-color:#FFFFD0; padding:6px 4px 32px 4px"})
    WWWMoaHTML.send_tag_open("span", {"style" : "font-size:24pt; text-decoration:underline"})
    WWWMoaRW.send(escaped_title)
    WWWMoaHTML.send_tag_close("span")
    WWWMoaHTML.send_linefeed_tag()
    WWWMoaHTML.send_linefeed_tag()
    WWWMoaRW.send(escaped_summary)
    WWWMoaHTML.send_linefeed_tag()
    WWWMoaHTML.send_linefeed_tag()
    WWWMoaHTML.send_simple_tag("hr")
    WWWMoaHTML.send_linefeed_tag()

    # send debugging info
    WWWMoaRW.send("Below is some information to help with debugging.")
    WWWMoaHTML.send_linefeed_tag()

    dt=datetime.datetime.now()

    WWWMoaRW.send(WWWMoaHTML.translate_text("Time: " + str(dt.hour)+":"+str(dt.minute).rjust(2,"0")+":"+str(dt.second).rjust(2,"0")+"\n"))

    try:
        WWWMoaRW.send(WWWMoaHTML.translate_text("Release: " + WWWMoaInfo.get_string() + "\n"))
    except:
        pass

    try:
        WWWMoaRW.send(WWWMoaHTML.translate_text("Python OS Module: " + os.name + "\n"))
    except:
        pass

    # end body
    WWWMoaHTML.send_tag_close("div")
    WWWMoaHTML.send_simple_tag("body")

    # finish sending document
    WWWMoaHTML.send_simple_tag_close("html")
    WWWMoaRW.terminate()
    
