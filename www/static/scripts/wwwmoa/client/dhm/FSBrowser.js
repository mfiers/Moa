
dojo.provide("wwwmoa.client.dhm.FSBrowser");
dojo.require("dijit._Widget");
dojo.require("wwwmoa");


dojo.addOnLoad(dojo.declare("wwwmoa.client.dhm.FSBrowser", dijit._Widget, {

	    _visualCode : null,
	    _locked : false,
	    _lsResponse : null,
	    _location : "",
	    _locationComponents : [],
	    _locationIsMoa : false,
	    _startIndex : 0,

	    _setVisualCodeAttr : function(val) {
		this._visualCode=val;
		this.refreshVisualElement();
	    },

	    _getVisualCodeAttr : function() {
		return this._visualCode;
	    },

	    _setLockedAttr : function(val) {
		this._locked=val;
		this.refreshVisualElement();
	    },

	    _getLockedAttr : function() {
		return this._locked;
	    },

            _setLsResponseAttr : function(val) {
		this._lsResponse=val;
	    },

	    _getLsResponseAttr : function() {
		return this._lsResponse;
	    },

	    _setLocationAttr : function(val) {
		this._location=val;
		this.doNavAction();
	    },

	    _getLocationAttr : function() {
		return this._location;
	    },

	    _setLocationComponents : function(val) {
		this._locationComponents=val;
	    },

	    _getLocationComponents : function() {
		return this._locationComponents;
	    },

	    _setLocationIsMoaAttr : function(val) {
		this._locationIsMoa=val;
	    },

	    _getLocationIsMoaAttr : function() {
		return this._locationIsMoa;
	    },

		_setStartIndexAttr : function(val) {
	    },

            _get

	    _getLocationBreadcrumbCodeAttr : function() {
		var locationComponents=this.attr("locationComponents");
		var code="<span style=\"font-weight:bold\"><img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdiroprtA")) + "\" alt=\"Directory\"> <a href=\"#wwwmoa-z\" style=\"color:#0000FF\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "').attr('location', '');\">Root</a>";
		
		for(var x=0; x<locationComponents.length; x++) {
		    code+=" / <a href=\"#wwwmoa-z\" style=\"color:#0000FF\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "').attr('location', '"+wwwmoa.formats.js.fix_text_for_html(locationComponents[x]["path"]) +"');\">"+locationComponents[x]["name"]+"</a>";
		}

		code+="</span>";
		
		return code;

	    },

	    constructor : function() {
		this.doNavAction();
	    },

	    buildRendering : function() {
		this.domNode=dojo.create("div", null);
		this.refreshVisualElement();
	    },



	    // Implementation for receiving startup event.  args may have a "location" member, which specifies where the file browser should start.
	    doNavAction : function() {
		var a=this;
		var location="";
 
		if(this.attr("location")!==undefined)
		    location=this.attr("location");
		    
		wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("ls", location),function(data) {
			a.dataCallback.call(a, data); // use the callback function of this object
		    } , 8192); // be somewhat patient about receiving the listing
	    },

	    // Takes the previously generated HTML and packages it for viewing.  Then,
            // it pushes the HTML code into the visual element so that it is visible.
	    refreshVisualElement : function() {
		
		if(this.domNode==null) // if we do not have a visual element
		    return; // there is no reason to proceed

		if(this.attr("visualCode")==null) // if either the main code or the current directory item code is not present
		    this.domNode.innerHTML="Loading directory contents...<br>One moment..."; // create loading message
		else // if both the main code and the current directory item code is present
		    this.domNode.innerHTML=this.attr("visualCode");
	    },

	    
            // Receives data from the API request.  Then, it creates the HTML code that
            // will be used to display the directory contents.  Finally, it request an
            // update of the visual element.
            dataCallback : function(data) {
		
                // Helper function that properly truncates a name.
		var truncName=function(str) {
                    var strtrunc=str.substr(0,16); // cap characters at 16

		    if(str.length!=strtrunc.length) { // if caping characters made a difference
			strtrunc=strtrunc.substr(0,13); // cap characters at 13, so there will be  characters in total
			strtrunc+="..."; // add on ...
		    }

		    return strtrunc;
		};
		
		var ls_response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data
		
		var buf_code=""; // buffer for visual code

		var is_dir=false; // holds whether the currently processed item is a directory or not
		var files_exist=false;  // holds whether or not the current directory has any items

		this.attr("lsResponse", ls_response); // save the parsed response we have received for later use
		
		
		if(data==null) { // if null was passed, we have an error
		    this.attr("visualCode", "Sorry, but the directory contents could not be loaded."); // create an error message
		    return;
		}
		

		// start structural table
		buf_code+="<table>";


		var_colour="";

		for(var x=0; x<ls_response["ls"].length; x++) { // for each item in the current directory
		    if(!ls_response["ls"][x]["read-allowed"]) // if we cannot read a file
			continue; // do not bother even showing it

		    is_dir=(ls_response["ls"][x]["type"]=="dir"); // find whether the item is a dir or not
		    
		    files_exist|=!is_dir; // if this item is a file, remember that we have encountered files
		    
		    name_colour=(ls_response["ls"][x]["write-allowed"] ? "#0000FF" : "#C0C0C0");

		    buf_code+="<tr><td>";

		    if(!is_dir) { // if the item is a file
			// create code for start of entry for a file
			buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSfileA")) + "\" alt=\"File\"> ";
		    }
		    else { // if the item is a directory
			// create code for start of entry for a directory
			
			if(ls_response["ls"][x]["x-is-moa"]) // if the item is a moa directory
			    buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdirclmoaA")) + "\" alt=\"Moa\" title=\"This item is a Moa directory.\"> "; // give it special annotation
			else // if the item is not a moa directory
			    buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdirclA")) + "\" alt=\"Directory\"> "; // give it normal annotation
		    }

		    buf_code+="<span style=\"font-weight:bold; color:"+name_colour+"; text-decoration:underline; cursor:pointer\" ";
		        
		    if(ls_response["ls"][x]["read-allowed"]) // if reading the item is allowed
			if(is_dir) // if the item is a directory
			    buf_code+="onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "').doContactAction('itm-" + x + "');\""; // add code to allow for directory changing
			else // if the item is a file
			    buf_code+="onclick=\"wwwmoa.ui.alert('Sorry, but you cannot view a listing for a file.');\""; // add code to alert user about the fact that they cannot list a file
		    else // if reading the item is not allowed
			if(is_dir) // if the item is a directory
			    buf_code+="onclick=\"wwwmoa.ui.alert('Sorry, but you cannot view the listing for this directory, because you do not have permission to do so.');\""; // add code to alert user that the directory cannot be read
			else // if the item is a file
			    buf_code+="onclick=\"wwwmoa.ui.alert('Sorry, but you cannot select this file, because you do not have permission to do so.');\""; // add code to alert user that the file cannot be read


		    
		    // start creating basic entry code (which is the same for files and directories)
		    buf_code+=" title=\""+wwwmoa.formats.html.fix_text(ls_response["ls"][x]["name"])+"\">";
		    buf_code+=wwwmoa.formats.html.fix_text(truncName(ls_response["ls"][x]["name"])); // add the name of the file
		    buf_code+="</span>";

		    buf_code+="</td><td style=\"font-weight:normal; padding-left:4px\">";

		    if(ls_response["ls"][x]["size"]>=0) // if the size has a meaning
			buf_code+=ls_response["ls"][x]["size"] + " b"; // add the size

		    buf_code+="</td><td>";



		    if(ls_response["ls"][x]["link"]) // if the item is a link
			buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSlinkA")) + "\" alt=\"Link\" title=\"This item is actually a link.\">"; // give it the proper annotation

		    buf_code+="</td></tr>";

		    }

		// end both structural tables
		buf_code+="</table>";

		
		this.attr("visualCode", buf_code); // make main code "public"
		
		this.attr("locationComponents", ls_response["dir"]);
		
		this.attr("locationIsMoa", ls_response["x-dir-is-moa"]);
	    

		this.attr("locked", false); // requests can now be sent again without a problem

		this.locationChanged(); // fire the event for other methods to use
	    },


           // Implementation for receiving contact messages.  This function
           // is nessesary for directory changing.
           doContactAction : function(data) {
		var path;
		var a=this;

		if(this.attr("locked")) // if we are locked
		    return; // we should not do anything, so exit

		if(this.attr("lsResponse")==null) // if we do not have a response from api call
		    return; // we cannot do anything, so exit
		
		if(data.substr(0,3)=="rtx") // if the message sent requested a change to the root directory
		    path=""; // use a blank string for the path
		else if(data.substr(0,4)=="par-") // if the message sent requested a parent directory
		    path=this.attr("lsResponse")["dir"][new Number(data.substr(4))]["path"]; // retrieve the pathname associated with the parent directory
		else if(data.substr(0,4)=="itm-") // if the message sent requested an item in the current directory
		    path=this.attr("lsResponse")["ls"][new Number(data.substr(4))]["path"]; // retrieve the pathname associated with the item
		else // if the message has not yet been recognized
		    return; // we should just exit

		this.attr("locked", true); // ensure that requests do not "pile up"

		this.attr("location", path); // set the new location

	    },

	    // Event entrypoint for other objects to attach to.
	    locationChanged : function() { }


}));

