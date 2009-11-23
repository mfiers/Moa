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
        state : {next_hmid : 0, hms : []},

        contact : function (hmid, data) {
            if(wwwmoa.hm.state.hms[hmid]===undefined) return;

            if(wwwmoa.hm.state.hms[hmid].doAction===undefined) return;

            wwwmoa.hm.state.hms[hmid].doAction(data);
        },

        unlink : function (hmid) {
            wwwmoa.hm.state.hms[hmid]=undefined;
            wwwmoa.hm.state.next_hmid=hmid;
        },

        create : function (hmrl, callback) {
            function cb(data) {
                hmc=new Function (data);
                new_hm=hmc();

                while(wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]!==undefined)
                {
                    wwwmoa.hm.state.next_hmid++;
                }
                
                new_hm.__hmid=wwwmoa.hm.state.next_hmid;
                wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]=new_hm;
                
                if(new_hm.doAction===undefined) {
                    new_hm.doAction=function(data){};
                }

                if(new_hm.doSetVisualElementAction===undefined) {
                    new_hm.doSetVisualElementAction=function(oldid){};
                }

                new_hm.visualElement=null;
                new_hm.getVisualElement=function() {
                    return this.visualElement;
                }

                new_hm.setVisualElementById=function(id) {
                    this.setVisualElement(document.getElementById(id));
                }

                new_hm.setVisualElement=function(ele) {
                    tmp=this.visualElement;
                    this.visualElement=ele;
                    this.doSetVisualElementAction(tmp);
                }

                new_hm.getHMId=function() {
                    return this.__hmid;
                }

                callback(new_hm);
            }

            function cbe(err) {
                callback(null);
            }

            dojo.xhrGet( {
                      url : hmrl,
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
