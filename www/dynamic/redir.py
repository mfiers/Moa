import sys

sys.path.append("../lib/python")

from wwwmoa import rw


target=rw.get_request_param("target")

target_dict={"python" : "http://www.python.org/",
             "firefox" : "http://www.mozilla.com/firefox",
             "about" : "http://mfiers.github.com/Moa",
             "moa" : "http://mfiers.github.com/Moa",
             "dojo" : "http://www.dojotoolkit.org/"
             }

if target in target_dict:
    final=target_dict[target]
else:
    final=None


rw.send_header("Cache-Control", "no-cache")
rw.send_header("Expires", "0")


if final!=None:
    rw.send_header("Location", final)
    rw.send_status(302)
    rw.end_header_mode()
    rw.terminate()
else:
    rw.send_status(404)
    rw.end_header_mode()
