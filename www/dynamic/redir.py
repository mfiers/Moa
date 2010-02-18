import sys

sys.path.append("../lib/python")

from wwwmoa import rw


## Target Lookup Table ##

target=rw.get_request_param("target")

target_dict={"python" : "http://www.python.org/",
             "firefox" : "http://www.mozilla.com/firefox",
             "about" : "http://mfiers.github.com/Moa",
             "moa" : "http://mfiers.github.com/Moa",
             "dojo" : "http://www.dojotoolkit.org/"
             }


## Main Logic ##

if target in target_dict:
    final=target_dict[target]
else:
    final=None


# instruct browser never to cache this response
rw.send_header("Cache-Control", "no-cache")
rw.send_header("Expires", "0")


if final!=None: # if destination could be found
    rw.send_header("Location", final) # send destination
    rw.send_status(302) # mark response as a redirect
    rw.end_header_mode()
    rw.terminate()
else: # if destination could not be found
    rw.send_status(404) # mark response as a 404 error
    rw.end_header_mode()
