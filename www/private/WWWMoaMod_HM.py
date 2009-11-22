### WWWMoa ###############################
### Mod_HM / Helper Module Interface
### Version: 0.1
### Date: November 20, 2009

## Imports ##
import WWWMoaRW
import WWWMoaRL
import WWWMoaJS
import WWWMoaHTMLError


## Helper Functions ##
def output_error(err):
    WWWMoaHTMLError.throw_fatal_error("Helper Module Server-Side Failure", "The server-side code for a helper module has failed.  More details can be found below.\n\n" + err)


## Main Interface Logic ##

def run(args=None, env=None):
    
    WWWMoaRW.send_header("Cache-Control", "no-cache")

    if (args==None) or (env==None):
        output_error("An unexpected error has occurred.")

    request_method=env["method"]

    if (request_method=="POST") or (request_method=="PUT") or (request_method=="DELETE"):
        output_error("You can only read the contents of the helper module you requested.")

    if len(args)==1:
        hm_id=args[0]
        found_hm=False

        if not hm_id.isalnum():
            output_error("The helper module name you submitted is invalid.")

        if hm_id=="dbrowse":
            import WWWMoaHM_DBrowse as WWWMoaHM
            found_hm=True

        if not found_hm:
            output_error("The helper module you attempted to retreive a constructor for does not exist.")

        WWWMoaRW.send_header("Content-Type", "text/javascript")

        WWWMoaRW.end_header_mode()

        WWWMoaRW.send("""/*

Helper Module Constructor

*/

"""+WWWMoaHM.get_constructor())

        WWWMoaRW.terminate()

    output_error("The helper module request you made is not supported.")

