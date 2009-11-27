### WWWMoa ###############################
### error-nf.py / 404 Error Interface

## Imports ##

import sys

sys.path.append("../lib/python/")

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import info
from wwwmoa.formats import html

import os
 


rw.send_header("Content-Type", "text/html; charset=UTF-8")
rw.send_header("Cache-Control", "no-cache")
rw.send_header("Expires", "0")
rw.send_status(404)
rw.end_header_mode()


rw.send("""<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">

<html>

<head>

<title>"""+html.fix_text(info.get_string())+""" Error: Not Found</title>

<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + html.fix_text(rl.get_style("normal"))+"""\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + html.fix_text(rl.get_style("normalbuttons"))+"""\">
<link rel=\"shortcut icon\" href=\"""" + html.fix_text(rl.get_image("MOAfavA"))+"""\">

<meta name=\"Generator\" content=\"""" + html.fix_text(info.get_string())+"""\">

</head>

""")


rw.send("""
<body>

<div id=\"wrapper\">

<span class=\"title\">"""+html.fix_text(info.get_string())+""" Error: Not Found</span>



""")



rw.send("""


<br><br>
<a href=\"""" + html.fix_text(rl.get_help()) + """\" target=\"_blank\" class=\"navbutton\">Help</a>
<a href=\"#jma-ahook\" class=\"navbutton\" onclick=\"window.location.reload(false);\">Try Again</a><br><br>


<div class=\"section\">

<span class=\"title\">Error Details</span><br>

The page or other resource you attempted to access could not be served to you, because we could not find it.  This might be because of a spelling mistake on your part, or a coding mistake on our part.<br><br>

It probably makes sense for you to return to the home page of Moa, which can be navigated to by <a href=\"""" + html.fix_text(rl.get_home())+"""\" title=\"Click here to continue using """+html.fix_text(info.get_name())+""".\">clicking here</a>.


</div>


</div>

<div id=\"smallnotices\">

This is the pre-release version of """+html.fix_text(info.get_name())+""". <br>""" + html.fix_text(info.get_name())+""" is powered by <a href=\"http://www.python.org/\">Python</a>. Best viewed in <a href=\"http://www.mozilla.com/firefox\">Firefox Web Browser</a>.

</div>

</body>

</html>

""")
