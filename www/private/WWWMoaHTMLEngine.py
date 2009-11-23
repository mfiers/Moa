### WWWMoa ###############################
### HTMLEngine / High-level HTML Generator
### Version: 0.1
### Date: November 18, 2009

## Imports ##
import sys # used to terminate execution
import cgi # used to make arbitrary text safe
import random # used to make document id

# various WWWMoa modules
import WWWMoaRW # used to facilitate output
import WWWMoaHTML # used to generate certain HTML code
import WWWMoaRL # used to locate various resource paths
import WWWMoaInfo # used to find out about WWWMoa in general

## State / Buffer Variables ##
_title="Untitled" # holds the current title associated with an HTML document
_current_section_id=0 # holds the next section id to use
_sections_currently_open=0 # holds the number of sections that have been opened
_last_unique_id=0 # holds the last unique id that was generated
_output_started=False # holds whether the HTML header has been sent
_lock_header=False # holds whether the HTML header content should be locked down
_document_id=random.randint(0,4026531840) # holds a random integer associated with the document
_header_scripts=[] # will hold custom scripts to add to header

## DOCTYPE Functions ##

## Returns the DOCTYPE associated with the version of HTML that the generator outputs.
def get_doctype():
    return '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'

## Convienance function that outputs the result of get_doctype().
def send_doctype():
    WWWMoaRW.send(get_doctype())


## Output State Handlers ##

## Gets the state of the output ready for the body of the HTML document.  Finishes "header mode" (meaning that headers can no longer be sent) and sends the header of the HTML document.  Certain functions (e.g. set_title()) can no longer be called.
def start_output():
    global _lock_header
    global _output_started

    WWWMoaRW.send_header("Content-Type", "text/html; charset=UTF-8") # this is an HTML message
    WWWMoaRW.send_header("Cache-Control", "no-cache") # do not cache
    WWWMoaRW.send_header("Expires", "0") # do not cache for some (old) browsers
    WWWMoaRW.end_header_mode() # done with headers, so end header mode

    _lock_header=True # we will soon be using header contents, so lock them down

    # send the DOCTYPE
    send_doctype()
    WWWMoaRW.send_doublelinefeed()

    # start HTML document
    WWWMoaHTML.send_simple_tag_open("html")
    WWWMoaRW.send_doublelinefeed()

    # start header
    WWWMoaHTML.send_simple_tag_open("head")
    WWWMoaRW.send_doublelinefeed()

    # send header contents
    send_header()
    WWWMoaRW.send_doublelinefeed()

    # end header
    WWWMoaHTML.send_simple_tag_close("head")
    WWWMoaRW.send_doublelinefeed()

    # start body
    WWWMoaHTML.send_simple_tag_open("body")
    WWWMoaRW.send_doublelinefeed()

    # start visual wrapper
    WWWMoaHTML.send_tag_open("div", {"id" : "wrapper"})

    # add page title
    WWWMoaHTML.send_tag_open("span", {"class" : "title"})
    place_text(get_title())
    WWWMoaHTML.send_tag_close("span")
    WWWMoaHTML.send_linefeed_tag()
    WWWMoaHTML.send_linefeed_tag()

    _output_started=True # we are ready for the body to be started

## Gets the state of the output ready for custom HTML.  Finishes "header mode" (meaning that headers can no longer be sent).  Certain functions (e.g. set_title()) can no longer be called. This function does not send any HTML content at all, which may be useful for a resource that is just an HTML "snippet".
def start_output_silent():
    global _output_started

    WWWMoaRW.end_header_mode()

    _output_started=True # we are ready for the body to be started

## Gets the state of the output so that the HTML document is sent.  Sends what is left of the HTML document, and terminates the script.
def end_output():
    global _output_started
    global _sections_currently_open

    while _sections_currently_open>0: # while there are sections still open
        end_section() # close a section

    _output_started=False # output should be closed down

    # end visual wrapper
    WWWMoaHTML.send_tag_close("div")
    WWWMoaRW.send_doublelinefeed()

    # start "small notices"
    WWWMoaHTML.send_tag_open("div", {"id" : "smallnotices"})
    WWWMoaRW.send_linefeed()

    # send the text of "small notices"
    place_text("This is the pre-release version of "+WWWMoaInfo.get_name()+".")
    place_text("\n" + WWWMoaInfo.get_name()+" is powered by ")
    WWWMoaHTML.send_tag_open("a", {"href" : "http://www.python.org/"})
    place_text("Python")
    WWWMoaHTML.send_tag_close("a")
    place_text(". Best viewed in ")
    WWWMoaHTML.send_tag_open("a", {"href" : "http://www.mozilla.com/firefox"})
    place_text("Firefox Web Browser")
    WWWMoaHTML.send_tag_close("a")
    place_text(".")

    # end "small notices"
    WWWMoaRW.send_linefeed()
    WWWMoaHTML.send_tag_close("div")
    WWWMoaRW.send_doublelinefeed()

    # end body
    WWWMoaHTML.send_simple_tag_close("body")
    WWWMoaRW.send_doublelinefeed()

    # end HTML document
    WWWMoaHTML.send_simple_tag_close("html")
    WWWMoaRW.send_linefeed()

    end_output_silent() # terminate the script

## Gets the state of the output so that what has been written is sent.  Terminates the script without sending any additional content.  This may be useful for a resource that is just an HTML "snippet".
def end_output_silent():
    sys.exit() # terminate script


## Body Content Generating Functions ##

## Starts a new section in the HTML document.  The section is assigned its own id (which is returned).  Sections can be nested.  Sections should be closed (eventually) using end_section().
def start_section():
    global _current_section_id # we need to know what section id we are up to
    global _sections_currently_open
    global _document_id

    strid="sec-"+str(_document_id)+"-"+str(_current_section_id) # create the section id
    
    _current_section_id=_current_section_id+1 # create the next section id
    _sections_currently_open=_sections_currently_open+1 # keep track of how many sections have been opened

    # start the section
    WWWMoaRW.send_doublelinefeed()
    WWWMoaHTML.send_tag_open("div", {"class" : "section", "id" : strid})
    WWWMoaRW.send_linefeed()

    return strid # the caller might be interested in what id we have used

## Ends a section in the HTML document. If called after all currently open sections have been closed, the function call is ignored.
def end_section():
    global _sections_currently_open

    # there is no sense in closing more sections than we have opened
    if _sections_currently_open<1:
        return

    # we are closing a single section, so keep track of how many are still open
    _sections_currently_open=_sections_currently_open-1

    # end the section
    WWWMoaRW.send_linefeed()
    WWWMoaHTML.send_tag_close("div")
    WWWMoaRW.send_doublelinefeed()

## Gets HTML code for a section's title.  In practice, the title will be stylized.  The title input will be made safe, so embeded HTML code will not function as such.
def get_section_title(title):
    return WWWMoaHTML.get_tag_open("span",{"class" : "title"}) + cgi.escape(title, True) + WWWMoaHTML.get_tag_close("span")+WWWMoaHTML.get_linefeed_tag()

## Convienance function that outputs the result of get_section_title().
def place_section_title(title):
    WWWMoaRW.send(get_section_title(title))

## Wrapper function that outputs arbitary text, after making it safe for use in an HTML document using HTML entities.  Additionally, linefeeds are translated appropriatly.
def place_text(text):
    place_code(WWWMoaHTML.translate_text(text))

## Wrapper function that makes an arbitary string HTML safe.
def get_safe_code(text):
    return WWWMoaHTML.fix_text(text)

## Wrapper function that outputs a string without processing it at all.
def place_code(code):
    WWWMoaRW.send(code)

## "Setter" for the HTML document's title. If called after the header has been sent, calls to this function will be ignored.
def set_title(title):
    global _title
    global _lock_header

    if _lock_header: # if state is not right
        return # ignore the function call

    _title=title

## "Getter" for the HTML document's title.
def get_title():
    global _title
    return _title

## Generates the HTML document's header.
def get_header():
    global _header_scripts

    header=""

    # output the title tag
    header+=WWWMoaHTML.get_simple_tag_open("title")
    header+=get_safe_code(get_title())
    header+=" - "
    header+=get_safe_code(WWWMoaInfo.get_name())
    header+=WWWMoaHTML.get_simple_tag_close("title")
    header+="\n\n"

    # output a reference to the CSS stylesheet
    header+=WWWMoaHTML.get_tag("link", {"rel" : "stylesheet", "type" : "text/css", "href" : WWWMoaRL.get_style("normal")})#WWWMoaRL.get_style("normal")})
    header+="\n\n"

    # add link to Dojo Toolkit
    add_script_to_header("dojo")

    # add link to Main Library
    add_script_to_header("wwwmoa")

    # add scripts to header
    header_scripts_unique=set(_header_scripts) # remove duplicates
    
    for h in header_scripts_unique: # for each script
        header+=WWWMoaHTML.get_tag_open("script", {"src" : WWWMoaRL.get_script(h), "type" : "text/javascript"}) # add script to header
        header+=WWWMoaHTML.get_tag_close("script") # we must end script tag
        header+="\n"

    header+="\n"

    # output a reference to the favicon
    header+=WWWMoaHTML.get_tag("link", {"rel" : "shortcut icon", "href" : WWWMoaRL.get_image("MOAfavA")})
    header+="\n\n"

    # output meta information
    header+=WWWMoaHTML.get_tag("meta", {"name" : "Generator", "content" : WWWMoaInfo.get_string()}) # brand it as being created by WWWMoa

    return header

## Adds a script to be included in the header.  The script must be part of the WWWMoa code base; it cannot be an arbitrary resource locator. If duplicate items are added, they will automatically be included only once. All scripts should be text/javascript (no VB script allowed!).
def add_script_to_header(id):
    global _header_scripts

    _header_scripts.append(id)

## Convienance function that outputs the result of get_header().
def send_header():
    WWWMoaRW.send(get_header())

## Generates an id that is guaranteed to be unique throughout the HTML document.  All ids that are used by custom-created HTML code should be generated using this function, or conflicts may occur with the ids created by the generator.
def get_unique_id():
    global _last_unique_id # we must take into account the last id we issued
    global _document_id    

    _last_unique_id=_last_unique_id+35 # figure out the next one to be issued

    return "uni-"+str(_document_id)+"-"+str(_last_unique_id) # generate the unique id
