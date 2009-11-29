### WWWMoa ###############################
### index.py / Main User Agent Program


## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../lib/python")

from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import info
from wwwmoa.formats import html
from wwwmoa.formats import js

import os


rw.send_header("Content-Type", "text/html; charset=UTF-8")
rw.send_header("Cache-Control", "no-cache")
rw.send_header("Expires", "0")
rw.end_header_mode()


rw.send("""<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">

<html>

<head>

<title>"""+html.fix_text(info.get_string())+""" Help</title>

<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + html.fix_text(rl.get_style("normal"))+"""\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + html.fix_text(rl.get_style("normalbuttons"))+"""\">
<link rel=\"shortcut icon\" href=\"""" + html.fix_text(rl.get_image("MOAfavA"))+"""\">

<meta name=\"Generator\" content=\"""" + html.fix_text(info.get_string())+"""\">

</head>

""")


rw.send("""
<body>

<div id=\"wrapper\">

<span class=\"title\">"""+html.fix_text(info.get_string())+""" Help</span><br><br>

<a href=\"javascript:window.close();\" class=\"navbutton\">Close Help</a><br><br>

<div class=\"section\">
<span class=\"title\">Coming Soon</span><br>
Help for WWWMoa is coming soon.  Please check back later.
</div>

""")


rw.send("""


</div>

<div id=\"smallnotices\">

This is the pre-release version of """+html.fix_text(info.get_name())+""". <br>""" + html.fix_text(info.get_name())+""" is powered by <a href=\"http://www.python.org/\">Python</a>. Best viewed in <a href=\"http://www.mozilla.com/firefox\">Firefox Web Browser</a>.

</div>

</body>

</html>

""")
