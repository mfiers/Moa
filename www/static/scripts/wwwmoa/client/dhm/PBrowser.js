
dojo.provide("wwwmoa.client.dhm.PBrowser");
dojo.require("dijit._Widget");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.PBrowser", dijit._Widget, {

	    _visualCode : null,
	    _locked : false,
	    _response : null,
	    _location : "",
	    _assumeNoProject : false,
	    

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

            _setResponseAttr : function(val) {
		this._response=val;
	    },

	    _getResponseAttr : function() {
		return this._response;
	    },

	    _setLocationAttr : function(val) {
		this._location=val;
		this.doNavAction();
	    },

	    _getLocationAttr : function() {
		return this._location;
	    },

	    _setAssumeNoProject : function(val) {
		this._assumeNoProject=val;
	    },

	    _getAssumeNoProject : function() {
		return this._assumeNoProject;
	    },

	    constructor : function() {
		this.doNoProjectAction();
	    },

	    buildRendering : function() {
		this.domNode=dojo.create("div", null);
		this.refreshVisualElement();
	    },


	    // Implementation for receiving instruction to find project information for current location.
	    doNavAction : function() {
		var a=this;
		
		if(this.attr("assumeNoProject")) {
		    this.doNoProjectAction();
		    return;
		}

		this.attr("visualCode", null);
    
		wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-jobinfo", this.attr("location")),function(data) {
			a.dataCallback.call(a, data); // use the callback function of this object
		    } , 8192); // be somewhat patient about receiving the listing
	    },

	    // Implementation for handling the case when a project has not be selected.
	    doNoProjectAction : function() {
		this.attr("visualCode", "No Moa job information is available.");
	    },

	    // Takes the previously generated HTML and packages it for viewing.  Then,
            // it pushes the HTML code into the visual element so that it is visible.
	    refreshVisualElement : function() {
		
		if(this.domNode==null) // if we do not have a visual element
		    return; // there is no reason to proceed

		if(this.attr("visualCode")==null) // if either the main code or the current directory item code is not present
		    this.domNode.innerHTML="Loading job information..."; // create loading message
		else // if both the main code and the current directory item code is present
		    this.domNode.innerHTML=this.attr("visualCode");
	    },

	    
            // Receives data from the API request.  Then, it creates the HTML code that
            // will be used to display the directory contents.  Finally, it request an
            // update of the visual element.
            dataCallback : function(data) {
		var response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data
		
		var buf_code=""; // buffer for visual code
		var cur_node=null; // holds a DOM node temporarily
		var is_dir=false; // holds whether the currently processed item is a directory or not
		var files_exist=false;  // holds whether or not the current directory has any items

		this.attr("response", response); // save the parsed response we have received for later use
		
		if(data==null) { // if null was passed, we have an error
		    this.attr("visualCode", "Sorry, but the project information could not be loaded."); // create an error message
		    return;
		}
		
		buf_code+="<span style=\"font-weight:bold; text-decoration:underline\">General Information</span>";
		buf_code+="<br>Title: "+(response["moa_title"]=="" ? "<span style=\"font-style:italic\">Untitled</span>" : wwwmoa.formats.html.fix_text(response["moa_title"]));
		buf_code+="<br>Description: "+(response["moa_description"]=="" ? "<span style=\"font-style:italic\">No Summary</span>" : wwwmoa.formats.html.fix_text(response["moa_description"]));
		buf_code+="<br><br><span style=\"font-weight:bold; text-decoration:underline\">Parameters</span><br>";

       		for(var x in response["parameters"]) {
		    buf_code+="<span title=\""+wwwmoa.formats.html.fix_text(response["parameters"][x]["description"])+"\">";
		    buf_code+=wwwmoa.formats.html.fix_text(x)+(response["parameters"].mandatory ? "<span style=\"font-weight:bold; color:#FF0000\">*</span>" : "")+"</span><br>";
		}

		buf_code+="<span style=\"font-weight:bold; color:#FF0000\">*</span> denotes mandatory parameter";

		this.attr("visualCode", buf_code); // make main code "public"
		

		this.attr("locked", false); // requests can now be sent again without a problem
	    }


	    })});

