

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {
    dojo.provide("wwwmoa.io");

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
	};

    wwwmoa.io.rl={        
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
    }

    // AJAX utilities
    wwwmoa.io.ajax={
          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
          get : function (relrl, callback, timeout) {
              function cb(txt) {
                  callback(txt);
              }

              function cbe(err) {
                  callback(null);
              }

	      var args={
		  url : relrl,
		  handleAs : "text",
		  timeout : timeout,
		  load : cb,
		  error : cbe
	      }

              dojo.xhrGet(args);

              return {
		  cancel : function()
                  {
                      if(args.abort!==undefined)
		          args.abort();
                  }
              };
	}
    }
}
