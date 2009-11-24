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
## (see WWWMoaMod_Resource).

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

            if(wwwmoa.hm.state.hms[hmid].doContactAction===undefined) return;
            
            wwwmoa.hm.state.hms[hmid].doContactAction(data);
        },

        unlink : function (hmid) {
            wwwmoa.hm.state.hms[hmid]=undefined;
            wwwmoa.hm.state.next_hmid=hmid;
        },

        create : function (hmrl, callback) {
            function cb(data) {
                hmc=new Function (data);
                var new_hm=hmc();

                while(wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]!==undefined)
                {
                    wwwmoa.hm.state.next_hmid++;
                }
                
                new_hm.__hmid=wwwmoa.hm.state.next_hmid;
                wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]=new_hm;
                
                if(new_hm.doContactAction===undefined) {
                    new_hm.doContactAction=function(data){};
                }

                if(new_hm.doIniAction===undefined) {
                    new_hm.doIniAction=function() {};
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

                new_hm.doIniAction();

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

    // RL utilities: JavaScript clone of WWWMoaRL
    rl : {
        
        url_encode : function (str) {
            var ret="";
            var c=0;
            

            for(var x=0; x<str.length; x++)
            {
                c=str.charCodeAt(x);
                
                if(c<33)
                    ret+="%"+dojo.string.pad(c.toString(16), 2, "0", false);
                else if(c==43) // plus
                    ret+="%2B";
                else if(c==63) // qm
                    ret+="%3F";
                else if(c==38) // amp
                    ret+="%26";
                else
                    ret+=str.substr(x,1);
            }

            return ret;
        },

        url_encode_x : function (str) {
            return this.url_encode(str.replace("@", "@@").replace("/", "@x"));
        },

        get_pre : function () {
            return \"""" + WWWMoaJS.fix_text(WWWMoaRL.get_pre())+"""\";
        },

        get_magic_pre : function () {
            return \"""" + WWWMoaJS.fix_text(WWWMoaRL.get_magic_pre())+"""\";
        },

        get_home : function () {
            return \"""" + WWWMoaJS.fix_text(WWWMoaRL.get_home())+"""\";
        },

        get_help : function () {
            return \"""" + WWWMoaJS.fix_text(WWWMoaRL.get_help())+"""\";
        },

        get_image : function (id) {
            return this.get_magic_pre()+\"resources/images/\"+this.url_encode_x(id);
        },

        get_style : function (id) {
            return this.get_magic_pre()+\"resources/styles/\"+this.url_encode_x(id);
        },

        get_script : function (id) {
            return this.get_magic_pre()+\"resources/scripts/\"+this.url_encode_x(id);
        },

        _trim_slashes : function (str) {
            var ret=str;
            var y;

            y=0;
            for(var x=y; x<ret.length;x++)
            {
                if(ret.substr(x,1)!=\"/\")
                    break;

                y=x+1;
            }

            ret=ret.substr(y);

            y=ret.length;
            for(var x=y; x>=0; x++)
            {
                if(ret.substr(x,1)!=\"/\")
                    break;

                y=x;
            }

            ret=ret.substr(0,y);

            return ret;
        },

        get_api : function (command, path) {
            if(path==null)
                var path_notnull=\"\";
            else
                var path_notnull=path;

            var fragment=this.url_encode(this._trim_slashes(path_notnull));

            if(fragment.length!=0)
                fragment+=\"/\";

            return this.get_magic_pre()+\"api/\"+fragment+this.url_encode_x(command);
        },

        get_hm : function (name, args) {
            if(args==null)
                var args_notnull=[];
            else
                var args_notnull=[];

            var args_fixed=[];

            for(x=0; x<args.length; x++)
                args_fixed[x]=this.url_encode_x(args[x]);

            var fragment=this.url_encode(args.join("/"));

            if(fragment.length!=0)
                fragment+=\"/\";

            return this.get_magic_pre()+\"hms/\"+fragment+this.url_encode_x(name);
        }






    },

    // HTML utilities
    html : {
        // escapes text to make it safe for insertion into an HTML document
        fix_text : function(txt) {
            return txt.replace(\"&\",\"&amp;\").replace(\"\\\"\", \"&quot;\").replace(\"\\'\", \"&#039;\").replace(\">\", \"&gt;\").replace(\"<\", \"&lt;\");
        }
    },

    // JSON utilities
    json : {
          // wrapper for Dojo JSON parser
          parse : function (str) {
              return dojo.fromJson(str);
          }
    },

    // AJAX utilities
    ajax : {
          // wrapper for Dojo AJAX system call
          get : function (relrl, callback, timeout) {
              function cb(txt) {
                  callback(txt);
              }

              function cbe(err) {
                  callback(null);
              }

              dojo.xhrGet( {
                        url : relrl,
                        handleAs : \"text\",
                        timeout : timeout,
                        load : cb,
                        error : cbe
              } );
          }
    }

}""")

    WWWMoaRW.terminate()
