### WWWMoa ###############################
### index.py / Main User Agent Program


## Imports ##
import sys

# get ready for next set of imports
sys.path.append("../private/")

import WWWMoaRW
import WWWMoaRL
import WWWMoaInfo
import WWWMoaHTML
import WWWMoaJS
import os


WWWMoaRW.send_header("Content-Type", "text/html; charset=UTF-8")
WWWMoaRW.send_header("Cache-Control", "no-cache")
WWWMoaRW.send_header("Expires", "0")
WWWMoaRW.end_header_mode()


WWWMoaRW.send("""<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">

<html>

<head>

<title>"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+""" Help</title>

<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normal"))+"""\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normalbuttons"))+"""\">
<link rel=\"shortcut icon\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_image("MOAfavA"))+"""\">

<meta name=\"Generator\" content=\"""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+"""\">

</head>

""")


WWWMoaRW.send("""
<body>

<div id=\"wrapper\">

<span class=\"title\">"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+""" Help</span><br><br>

<a href=\"javascript:window.close();\" class=\"navbutton\">Close Help</a><br><br>

<div class=\"section\">
<span class=\"title\">Coming Soon</span><br>
Help for WWWMoa is coming soon.  Please check back later.
</div>

""")


WWWMoaRW.send("""


</div>

<div id=\"smallnotices\">

This is the pre-release version of """+WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""". <br>""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""" is powered by <a href=\"http://www.python.org/\">Python</a>. Best viewed in <a href=\"http://www.mozilla.com/firefox\">Firefox Web Browser</a>.

</div>

</body>

</html>

""")
