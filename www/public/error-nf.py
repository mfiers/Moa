### WWWMoa ###############################
### error-nf.py / 404 Error Interface

## Imports ##

import sys

sys.path.append("../private/")

import WWWMoaRW
import WWWMoaRL
import WWWMoaInfo
import WWWMoaHTML

import os
 


WWWMoaRW.send_header("Content-Type", "text/html; charset=UTF-8")
WWWMoaRW.send_header("Cache-Control", "no-cache")
WWWMoaRW.send_header("Expires", "0")
WWWMoaRW.send_status(404)
WWWMoaRW.end_header_mode()


WWWMoaRW.send("""<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">

<html>

<head>

<title>"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+""" Error: Not Found</title>

<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normal"))+"""\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normalbuttons"))+"""\">
<link rel=\"shortcut icon\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_image("MOAfavA"))+"""\">

<meta name=\"Generator\" content=\"""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+"""\">

</head>

""")


WWWMoaRW.send("""
<body>

<div id=\"wrapper\">

<span class=\"title\">"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+""" Error: Not Found</span>



""")



WWWMoaRW.send("""


<br><br>
<a href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_help()) + """\" target=\"_blank\" class=\"navbutton\">Help</a>
<a href=\"#jma-ahook\" class=\"navbutton\" onclick=\"window.location.reload(false);\">Try Again</a><br><br>


<div class=\"section\">

<span class=\"title\">Error Details</span><br>

The page or other resource you attempted to access could not be served to you, because we could not find it.  This might be because of a spelling mistake on your part, or a coding mistake on our part.<br><br>

It probably makes sense for you to return to the home page of Moa, which can be navigated to by <a href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_home())+"""\" title=\"Click here to continue using """+WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""".\">clicking here</a>.


</div>


</div>

<div id=\"smallnotices\">

This is the pre-release version of """+WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""". <br>""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""" is powered by <a href=\"http://www.python.org/\">Python</a>. Best viewed in <a href=\"http://www.mozilla.com/firefox\">Firefox Web Browser</a>.

</div>

</body>

</html>

""")
