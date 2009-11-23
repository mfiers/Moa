### WWWMoa ###############################
### index.py / Main User Agent Program
### Version: 0.1
### Date: November 19, 2009

## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../private/")

import WWWMoaRW
import WWWMoaRL
import WWWMoaCGIEx
import WWWMoaHTMLError
import WWWMoaInfo
import WWWMoaHTML
import WWWMoaHTMLEngine
import WWWMoaJS
import os

## Document Preparation ##

WWWMoaHTMLEngine.set_title("Main View")
WWWMoaHTMLEngine.add_script_to_header("wwwmoaui") # we will use ui functionality

# start pushing code
WWWMoaHTMLEngine.start_output()


## JavaScript Backup Plan ##
WWWMoaHTML.send_simple_tag_open("noscript")
WWWMoaHTMLEngine.start_section()
WWWMoaHTMLEngine.place_section_title("JavaScript Interpreter Required")
WWWMoaHTMLEngine.place_text("Your browser does not seem to have JavaScript support.  Unfortunatly, since this web application is highly interactive, it requires that your browser support JavaScript.\n\nHowever, do not panic!  There are several ways that you remedy this problem:\n")
WWWMoaHTML.send_tag_open("div", {"style" : "padding-left:40px"})

WWWMoaHTMLEngine.place_code("&bull; You might be able to enable JavaScript on your browser.  Sometimes, you (or someone with access to your computer) may have turned off JavaScript support for various reasons.  Enabling in this case is usually quite simple.  If you use Firefox, ")
WWWMoaHTML.send_tag_open("a", {"href" : "http://support.mozilla.com/en-US/kb/JavaScript"})
WWWMoaHTMLEngine.place_text("click here for detailed instructions")
WWWMoaHTML.send_tag_close("a")
WWWMoaHTMLEngine.place_code(". If you use MS Internet Explorer, ")
WWWMoaHTML.send_tag_open("a", {"href" : "http://support.microsoft.com/gp/howtoscript"})
WWWMoaHTMLEngine.place_text("click here for detailed instructions")
WWWMoaHTML.send_tag_close("a")
WWWMoaHTMLEngine.place_code(".")
WWWMoaHTML.send_linefeed_tag()

WWWMoaHTMLEngine.place_code("&bull; You can install a browser that supports JavaScript.  We recommend using a browser called ")
WWWMoaHTML.send_tag_open("a", {"href" : "http://www.mozilla.com/firefox"})
WWWMoaHTMLEngine.place_text("Firefox")
WWWMoaHTML.send_tag_close("a")
WWWMoaHTMLEngine.place_code(".")

WWWMoaHTML.send_tag_close("div")
WWWMoaHTMLEngine.end_section()
WWWMoaHTML.send_simple_tag_close("noscript")

id_hidden_section=WWWMoaHTMLEngine.get_unique_id()
# begin JavaScript "display section" to be made visible if JavaScript support exists
WWWMoaHTML.send_tag_open("div", {"id" : id_hidden_section, "style" : "visibility:hidden"})



## Main Content ##


id_temp_section=WWWMoaHTMLEngine.get_unique_id()

# main script body
WWWMoaHTML.send_tag_open("script", {"type" : "text/javascript"})
WWWMoaHTMLEngine.place_code("\n<!--\n")
WWWMoaHTMLEngine.place_code("""



wwwmoa.hm.create(\"moa/fs/browsehm\", function(obj){

    if(obj===null)
    {
        document.getElementById(\""""+WWWMoaJS.fix_text_for_html(id_temp_section)+"""\").innerHTML=\"Something went wrong: the directory browser you requested could not be supplied.\";
        return;
    }

    obj.setVisualElementById(\"""" + WWWMoaJS.fix_text_for_html(id_temp_section)+"""\");
});



""")
WWWMoaHTMLEngine.place_code("\n//-->\n")
WWWMoaHTML.send_tag_close("script")



WWWMoaHTML.send_tag_open("div", {"id" : id_temp_section})
WWWMoaHTML.send_tag_open("span", {"style" : "font-weight:bold"})
WWWMoaRW.send("Loading...")
WWWMoaHTML.send_tag_close("span")
WWWMoaHTML.send_tag_close("div")


## JavaScript Display Section Logic ##

WWWMoaHTML.send_tag_close("div") # close the JavaScript "display section"

# script to make "display section" visible
WWWMoaHTML.send_tag_open("script", {"type" : "text/javascript"})
WWWMoaHTMLEngine.place_code("\n<!--\n")
WWWMoaHTMLEngine.place_code("document.getElementById(\""+WWWMoaJS.fix_text_for_html(id_hidden_section)+"\").style.visibility=\"visible\";")
WWWMoaHTMLEngine.place_code("\n//-->\n")
WWWMoaHTML.send_tag_close("script")



WWWMoaHTMLEngine.end_output()
