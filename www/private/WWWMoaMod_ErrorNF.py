### WWWMoa ###############################
### Mod_ErrorNF
### Version: 0.1
### Date: November 18, 2009


## Imports ##
import WWWMoaHTMLEngine
import WWWMoaHTML
import WWWMoaRL
import WWWMoaRW

## Page Logic ##

def run(args = None, env = None):

    # [!] Note: We do not care whether args or env was passed.

    WWWMoaRW.send_status(404)

    WWWMoaHTMLEngine.set_title("Error: Not Found")

    WWWMoaHTMLEngine.start_output() # start page

    WWWMoaHTMLEngine.start_section()

    WWWMoaHTMLEngine.place_section_title("Error Details")

    WWWMoaHTMLEngine.place_text("""The page or other resource you attempted to access could not be served to you, because we could not find it.  This might be because of a spelling mistake on your part, or a coding mistake on our part.

It probably makes sense for you to return to the home page of Moa, which can be navigated to by """)

    WWWMoaHTML.send_tag_open("a", {"href" : WWWMoaRL.get_home(), "title" : "Click here to continue using Moa."})
    WWWMoaHTMLEngine.place_text("clicking here")
    WWWMoaHTML.send_tag_close("a")

    WWWMoaHTMLEngine.place_text(".")

    WWWMoaHTMLEngine.end_section()

    WWWMoaHTMLEngine.end_output() # finish page
