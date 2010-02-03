

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
    };



    wwwmoa.formats={

        // HTML utilities
        html : {
            // Escapes text to make it safe for insertion into an HTML document.
            fix_text : function(txt) {
                return txt.replace(/&/g,"&amp;").replace(/\"/g, "&quot;").replace(/\'/g, "&#039;").replace(/>/g, "&gt;").replace(/</g, "&lt;");
            },

	    // Escapes text to make it safe for insertion into an HTML document.
	    // Also ensures linefeeds are changed to BR nodes.
	    translate_text : function(txt) {
		return this.fix_text(txt).replace(/\n/g, "<br>");
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
                return wwwmoa.formats.html.fix_text(wwwmoa.formats.js.fix_text(txt));
            }
        },

        // JSON utilities
        json : {
              // Wrapper for Dojo JSON parser.
              parse : function(str) {
                  return dojo.fromJson(str);
	      },

	      // Wrapper for Dojo JSON encoder.
	      encode : function(obj) {
		  return dojo.toJson(obj);
	      }
        }
    }
}
