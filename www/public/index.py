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

<title>"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+"""</title>

<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normal"))+"""\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_style("normalbuttons"))+"""\">
<link rel=\"shortcut icon\" href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_image("MOAfavA"))+"""\">

<script src=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_script("dojo"))+"""\" type=\"text/javascript\"></script>
<script src=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_script("wwwmoa"))+"""\" type=\"text/javascript\"></script>
<script src=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_script("wwwmoaui"))+"""\" type=\"text/javascript\"></script>

<meta name=\"Generator\" content=\"""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+"""\">

</head>

""")


WWWMoaRW.send("""
<body>

<div id=\"wrapper\">

<span class=\"title\">"""+WWWMoaHTML.fix_text(WWWMoaInfo.get_string())+"""</span>



""")


WWWMoaRW.send("""


<noscript>

<div class=\"section\">

<span class=\"title\">JavaScript Interpreter Required</span><br>

Your browser does not seem to have JavaScript support.  Unfortunatly, since this web application is highly interactive, it requires that your browser support JavaScript.

<br><br>

However, do not panic!  There are several ways that you can remedy this problem:

<div style=\"padding-left:40px\">

&bull; You might be able to enable JavaScript on your browser.  Sometimes, you (or someone with access to your computer) may have turned off JavaScript support for various reasons.  Enabling in this case is usually quite simple.  If you use Firefox, <a href=\"http://support.mozilla.com/en-US/kb/JavaScript\">click here for detailed instructions</a>. If you use MS Internet Explorer, <a href=\"http://support.microsoft.com/gp/howtoscript\">click here for detailed instructions</a>.<br>

&bull; You can install a browser that supports JavaScript.  We recommend using a browser called <a href=\"http://www.mozilla.com/firefox\">Firefox</a>.

</div>

</div>

</noscript>


""")


WWWMoaRW.send("""

<div id=\"jma-jsprotect\" style=\"visibility:hidden\">










<script type=\"text/javascript\">
<!--

wwwmoa.hm.create(\"""" + WWWMoaJS.fix_text_for_html(WWWMoaRL.get_hm("fsbrowser",[])) + """\", function(obj){

    if(obj===null)
    {
        document.getElementById(\"jma-fsbrowser\").innerHTML=\"Something went wrong: the directory browser you requested could not be supplied.\";
        return;
    }

    obj.setVisualElementById(\"jma-fsbrowser\");
});


//-->
</script>



<br>
<a href=\"""" + WWWMoaHTML.fix_text(WWWMoaRL.get_help()) + """\" target=\"_blank\" class=\"navbutton\">Help</a>
<a href=\"#jma-ahook\" class=\"navbutton\" onclick=\"window.location.reload(false);\">Restart</a><br><br>



<div style=\"border:1px solid #808080; padding:5px; width:98%; margin-bottom:40px\">

<table>

<tr>

<td id=\"jma-fsbrowser\" style=\"vertical-align:top; font-weight:bold; padding-left:12px\">

<div style=\"font-weight:bold; text-align:center\">
Loading...
</div>

</td>

<td id=\"jma-main\" style=\"border-left:3px solid #606060; vertical-align:top; font-weight:bold; padding-left:12px\">

<div style=\"font-weight:bold; text-align:center\">
Loading...
</div>

</td>

</tr>

</table>

</div>








</div>

""")

WWWMoaRW.send("""
<script type=\"text/javascript\">
<!--
document.getElementById(\"jma-jsprotect\").style.visibility=\"visible\";
//-->
</script>

</div>

<div id=\"smallnotices\">

This is the pre-release version of """+WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""". <br>""" + WWWMoaHTML.fix_text(WWWMoaInfo.get_name())+""" is powered by <a href=\"http://www.python.org/\">Python</a>. Best viewed in <a href=\"http://www.mozilla.com/firefox\">Firefox Web Browser</a>.

</div>

</body>

</html>

""")
