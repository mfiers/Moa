### WWWMoa ###############################
### JSCore / Core JS Library
### Version: 0.1
### Date: November 20, 2009

### Import Note ##
## Normally, scripts are kept static.  However,
## this script is dynamic to allow for the
## loading of various system information at
## request time.  To keep the external inteface
## uniform, it has been specially linked in
## WWWMoaMod_Resource.

## Imports ##

import WWWMoaRW
import WWWMoaRL
import WWWMoaInfo
import WWWMoaJS

## JS Library ##

def run(args=None, env=None):
    WWWMoaRW.send_header("Content-Type", "text/javascript")
    WWWMoaRW.end_header_mode()

    WWWMoaRW.send("""
/// WWWMoa ///////////////////////////////
/// Core JS Library
/// Version: 0.1
/// Date: November 20, 2009

/// NOTES ///
// The API defined by this library should be accessed
// instead of the Dojo API that this library is based
// on.

var wwwmoa={ // root object

    // JS library version information
    jsinfo : {
	version : {major : 0, minor : 1, str : \"0.1\"},
	name : \"WWWMoa JS\",
	str : \"WWWMoa JS 0.1\"
    },

    // WWWMoa version information
    info : {
	version : {major : """ + str(WWWMoaInfo.get_version_major()) + """, minor : """ + str(WWWMoaInfo.get_version_minor()) + """, str : \"""" + WWWMoaJS.fix_text(WWWMoaInfo.get_version_string()) + """\"},
	name : \"""" + WWWMoaJS.fix_text(WWWMoaInfo.get_name()) + """\",
	str : \"""" + WWWMoaJS.fix_text(WWWMoaInfo.get_string()) + """\"
    },

    // Helper module utilities
    hm : {
        create : function (hmname, callback) {
        
            function cb(data) {
                hmc=new Function (data);
                hm=hmc();
                callback(hm);
            }

            function cbe(err) {
                callback(null);
            }

            dojo.xhrGet( {
                      url : \"""" + WWWMoaJS.fix_text(WWWMoaRL.get_hm_base()) + """\"+wwwmoa.rl.url_encode_x(hmname),
                      handleAs : \"text\",
                      timeout : 8192,
                      load : cb,
                      error : cbe
                     } );

        }
    },

    // RL utilities
    rl : {
        // javascript version of WWWMoaRL.url_encode_x()
        url_encode_x : function (str) {
            return str.replace("@", "@@").replace("/", "@x");
        }
    }

}""")

    WWWMoaRW.terminate()
