
if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {
    dojo.provide("wwwmoa.client");
    dojo.require("wwwmoa");

    var obj=new Object();

    

    if(!dojo.isObject(wwwmoa)) {
	wwwmoa=new Object();
	};

    wwwmoa.client=obj;

    wwwmoa.client._ini_dojo=function() {
	dojo.require("dijit.Dialog");
	dojo.require("dijit._Widget");

    }

    wwwmoa.client._ini=function() {
	this._ini_graphics();
    }

    wwwmoa.client.getVRoot=function() {
	return window.document.getElementById("wwwmoa-vroot");
    }

    wwwmoa.client.getVProtect=function() {
	return window.document.getElementById("wwwmoa-vprotect");
    }

    wwwmoa.client._ini_graphics=function() {
	dojo.parser.parse();

	wwwmoa.client.getVProtect().style.visibility="visible";
    }

    wwwmoa.client.showAbout=function() {
	var dialog=new dijit.Dialog({title : "About WWWMoa", content : "<img src=\"/images/MOAfavA\" alt=\"\"> WWWMoa 0.1<br><br><a href=\"/about\" target=\"_blank\">Click here</a> to visit Moa's official website."});

	wwwmoa.client.getVRoot().appendChild(dialog.domNode);

	dialog.show();
    }

    wwwmoa.client._ini_dojo();
}