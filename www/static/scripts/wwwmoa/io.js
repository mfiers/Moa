

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
    };

    if(!dojo.isObject(wwwmoa.io)) {
	wwwmoa.io=new Object();
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

            return "/api/"+fragment+command;
        },

        get_hm : function (rrl) {
            return "/scripts/hm/"+rrl;
        }
    }

    // AJAX utilities
    wwwmoa.io.ajax={
	  _createBaseObject : function(relrl, callback, timeout) {
	      var bobj={};

	      bobj.cb=function(txt) {
                  callback(txt);
              };

              bobj.cbe=function(err) {
                  callback(null);
              };

	      bobj.args={
		  url : relrl,
		  handleAs : "text",
		  timeout : timeout,
		  load : bobj.cb,
		  error : bobj.cbe
	      };

	      bobj.returnobj={cancel : function() { bobj.req.cancel() }};

	      return bobj;
	  },


          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
          get : function (relrl, callback, timeout) {
	      var bobj=this._createBaseObject(relrl, callback, timeout);

              bobj.req=dojo.xhrGet(bobj.args);

              return bobj.returnobj;
	  },


          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
          del : function (relrl, callback, timeout) {
	      var bobj=this._createBaseObject(relrl, callback, timeout);

              bobj.req=dojo.xhrDelete(bobj.args);

              return bobj.returnobj;
	  },



          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
	  post : function (relrl, callback, timeout, data) {
              var bobj=this._createBaseObject(relrl, callback, timeout);

	      if(dojo.isString(data))
		  bobj.args.postData=data;

	      bobj.req=dojo.xhrPost(bobj.args);

	      return bobj.returnobj;
	  },

          // Wrapper for Dojo AJAX system call.  The callback function is passed
          // null on error, or a string object on success.
          put : function (relrl, callback, timeout, data) {
              var bobj=this._createBaseObject(relrl, callback, timeout);

	      if(dojo.isString(data))
		  bobj.args.postData=data;

	      bobj.req=dojo.xhrPut(bobj.args);

	      return bobj.returnobj;
	  }


    }

    // Cookie utilities
    wwwmoa.io.cookie={
	set : function(key, value, keep) {
	    if(keep==null)
		keep=false;

	    dojo.cookie(key, value, (keep ? {expires : 730} : {}));
	},

	get : function(key) {
	    return dojo.cookie(key);
	}
    }
}
