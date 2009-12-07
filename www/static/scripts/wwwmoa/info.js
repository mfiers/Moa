

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {
    dojo.provide("wwwmoa.info");

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
	};

    wwwmoa.info={
	client : {major : 0, minor : 1, name : "WWWMoa Client", poweredby : "JS; Dojo Toolkit"},
	server : {major : 0, minor : 1, name : "WWWMoa Server Side API", poweredby : "Python"},
	moa : {major : 0, minor : 1, name : "Moa", poweredby : "GNU Make; Python"}
    }
}
