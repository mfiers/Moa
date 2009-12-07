

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {
    dojo.provide("wwwmoa");
    dojo.require("wwwmoa.info");
    dojo.require("wwwmoa.io");
    dojo.require("wwwmoa.formats");

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
	};
}

