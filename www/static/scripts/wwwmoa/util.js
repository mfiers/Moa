

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
    };



    wwwmoa.util={

        // string utilities
        str : {
	    // Formats a string like a title.
	    title_case : function (str) {
		var str_parts=str.split(" ");
		var str_ret="";

		for(var x=0; x<str_parts.length; x++)
		    str_ret+=(str_ret=="" ? "" : " ")+str_parts[x].substr(0,1).toUpperCase()+str_parts[x].substr(1);

		return str_ret;
	    }
        }


    }
}
