
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
	version : {major : 0, minor : 1, str : "0.1"},
	name : "WWWMoa JS",
	str : "WWWMoa JS 0.1"
    },

    // WWWMoa version information
    info : {
	version : {major : 0, minor : 1, str : "0.1"},
	name : "WWWMoa",
	str : "WWWMoa 0.1"
    },

    // Helper module utilities
    hm : {
        // information about what helper modules have been created
        state : {next_hmid : 0, hms : []},

        // Sends a given message to a helper module, addressed by its ID.
        // The message is delivered by calling the helper module's "doContactAction"
        // method.
        // This method returns true on success, and false on failure.
        contact : function (hmid, data) {
            if(wwwmoa.hm.state.hms[hmid]===undefined) return false;

            if(wwwmoa.hm.state.hms[hmid].doContactAction===undefined) return false;
            
            wwwmoa.hm.state.hms[hmid].doContactAction(data);

            return true;
        },

        // Unlinks a given helper module.  In practice, this means that
        // the helper modules ID will be reused.  It does NOT attempt to
        // delete the object.
        unlink : function (hmid) {
            wwwmoa.hm.state.hms[hmid]=undefined; // remove the helper module from the list of helper modules
            wwwmoa.hm.state.next_hmid=hmid; // remember to use this id next, since it is now free
        },

        // Creates a helper module object from code at a given relative
        // RL.  This function accepts a callback function that is called
        // on success or failure.  On success, the callback function is
        // passed a single argument, which is the object of the helper
        // module.  On failure, the callback function is passed null.
        //
        // [!] Implementation Note: This function creates API calls to
        // the Dojo Toolkit.
        create : function (hmrl, args, callback) {

            // Callback function that creates the helper module object from
            // code that is passed to it.  This callback function also
            // provides default definitions for certain required functions,
            // as well as overwriting certain functions so that they have
            // the required behavior.
            function cb(data) {
                hmc=new Function (data); // create a function that contains the passed code
                var new_hm=hmc(); // the code should return a helper module, so execute it

                while(wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]!==undefined) // while we have not found an unused id
                {
                    wwwmoa.hm.state.next_hmid++; // try the next one
                }
                
                new_hm.__hmid=wwwmoa.hm.state.next_hmid; // set the helper module's id internally
                wwwmoa.hm.state.hms[wwwmoa.hm.state.next_hmid]=new_hm; // add the helper module to the list of helper modules
                
                if(new_hm.doContactAction===undefined) { // if doContactAction() has not been defined
                    new_hm.doContactAction=function(data){}; // create it with a default implementation
                }

                if(new_hm.doIniAction===undefined) { // if doIniAction() has not been defined 
                    new_hm.doIniAction=function() {}; // create it with a default implementation
                }

                if(new_hm.doSetVisualElementAction===undefined) { // if doSetVisualElementAction() has not been defined
                    new_hm.doSetVisualElementAction=function(oldid){}; // create it with a default implementation
                }

                new_hm.visualElement=null; // set visualElement to null (whether it has been defined or not)
                new_hm.getVisualElement=function() { // create getVisualElement() (whether it has been defined or not)
                    return this.visualElement; // simply return the internal variable
                }

                new_hm.setVisualElementById=function(id) { // create setVisualElementById() (whether it has been defined or not)
                    this.setVisualElement(document.getElementById(id)); // set the visual element after making a call to getElementById()
                }

                new_hm.setVisualElement=function(ele) { // create setVisualElement() (whether it has been defined or not)
                    tmp=this.visualElement; // save the current element (as we will pass it later)
                    this.visualElement=ele; // set the new element
                    this.doSetVisualElementAction(tmp); // the visual element has been changed, so trigger event
                }

                new_hm.getHMId=function() { // create getHMId() (whether it has been defined or not)
                    return this.__hmid; // simply return the internal state variable
                }

		if(args===undefined)
		    args=new Object();

                new_hm.doIniAction(args); // trigger startup event / send args (args should be an object)

                callback(new_hm); // pass the new helper module object to the callback function
            }

            // Callback function that receives errors.
            function cbe(err) { 
                callback(null); // on error, pass null to callback function
            }

            // ask Dojo to start an AJAX request
            dojo.xhrGet( {
                      url : hmrl,
                      handleAs : "text",
                      timeout : 8192,
                      load : cb,
                      error : cbe
                     } );

        }

        
    },

    // RL utilities
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
            return "/";
        },

        get_magic_pre : function () {
            return "/api/";
        },

        get_home : function () {
            return "/index";
        },

        get_help : function () {
            return "/about";
        },

        get_image : function (rrl) {
            return "/images/"+rrl;
        },

        get_style : function (rrl) {
            return "/styles/"+rrl;
        },

        get_script : function (rrl) {
            return "/scripts/"+rrl;
        },

        _trim_slashes : function (str) {
            var ret=str;
            var y;

            y=0;
            for(var x=y; x<ret.length;x++)
            {
                if(ret.substr(x,1)!="/")
                    break;

                y=x+1;
            }

            ret=ret.substr(y);

            y=ret.length;
            for(var x=y; x>=0; x++)
            {
                if(ret.substr(x,1)!="/")
                    break;

                y=x;
            }

            ret=ret.substr(0,y);

            return ret;
        },

        get_api : function (command, path) {
            if(path==null)
                var path_notnull="";
            else
                var path_notnull=path;

            var fragment=this.url_encode(this._trim_slashes(path_notnull));

            if(fragment.length!=0)
                fragment+="/";

            return "/api/"+fragment+this.url_encode_x(command);
        },

        get_hm : function (rrl) {
            return "/scripts/hm/"+rrl;
        }






    },

    // HTML utilities
    html : {
        // Escapes text to make it safe for insertion into an HTML document.
        fix_text : function(txt) {
            return txt.replace("&","&amp;").replace("\"", "&quot;").replace("'", "&#039;").replace(">", "&gt;").replace("<", "&lt;");
        }
    },

    // JavaScript utilities
    js : {
        // Escapes text to make it safe for insertion into a JavaScript literal.
        fix_text : function(txt) {
            return txt.replace("\\", "\\\\").replace("\"", "\\\"").replace("'", "\\'");
	},

        // Escapes text to make it safe for insertion into a JavaScript literal, if the JavaScript is embeded in a HTML document.
	fix_text_for_html : function(txt) {
            return wwwmoa.html.fix_text(wwwmoa.js.fix_text(txt));
        }
    },

    // JSON utilities
    json : {
          // Wrapper for Dojo JSON parser.
          parse : function (str) {
              return dojo.fromJson(str);
          }
    },

    // AJAX utilities
    ajax : {
          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
          get : function (relrl, callback, timeout) {
              function cb(txt) {
                  callback(txt);
              }

              function cbe(err) {
                  callback(null);
              }

              dojo.xhrGet( {
                        url : relrl,
                        handleAs : "text",
                        timeout : timeout,
                        load : cb,
                        error : cbe
              } );
          }
    }

}
