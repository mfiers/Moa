
dojo.provide("wwwmoa.client.dhm.PBrowser");
dojo.require("dijit._Widget");
dojo.require("dijit.Tooltip");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.PBrowser", dijit._Widget, {

	    _visualDOM : null,
	    _locked : false,
	    _response : null,
	    _location : "",
	    _assumeNoProject : false,
	    

	    _setVisualDOMAttr : function(val) {
		this._visualDOM=val;
		this.refreshVisualElement();
	    },

	    _getVisualDOMAttr : function() {
		return this._visualDOM;
	    },

	    _setVisualCodeAttr : function(val) {
		if(val==null) {
		    this.attr("visualDOM", null);
		    return;
		}
		this.attr("visualDOM", dojo.create("div", {innerHTML : val}));
	    },

	    _getVisualCodeAttr : function() {
	        if(this.attr("visualDOM")==null)
		    return null;

		return this.attr("visualDOM").innerHTML;
	    },

	    _setLockedAttr : function(val) {
		this._locked=val;
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


	    // Implementation for receiving instruction to find job information for current location.
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
		
		if(this.attr("visualDOM")==null) // if either the main code or the current directory item code is not present
		    this.domNode.innerHTML="Loading job information..."; // create loading message
		else { // if both the main code and the current directory item code is present
		    this.domNode.innerHTML="";
		    this.domNode.appendChild(this.attr("visualDOM"));
		}
	    },

	    
            // Receives data from the API request.  Then, it creates the HTML code that
            // will be used to display the job view contents.  Finally, it requests an
            // update of the visual element.
            dataCallback : function(data) {
		var response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data
		var buf_tmp=""; // temporary buffer for visual code
		var buf_final=""; // buffer for the final visual code
		var cur_param=""; // holds the current parameter dictionary
		var cur_value_esc=""; // holds the current parameter's value, after being HTML escaped
		var buf_cat={}; // dictionary for category visual code


		this.attr("response", response); // save the parsed response we have received for later use
		
		if(data==null) { // if null was passed, we have an error
		    this.attr("visualCode", "Sorry, but the project information could not be loaded."); // create an error message
		    return;
		}
		
		

		buf_final+="<span style=\"font-weight:bold; text-decoration:underline\">General Information</span>";
		buf_final+="<br>Title: "+(response["moa_title"]=="" ? "<span style=\"font-style:italic\">Untitled</span>" : wwwmoa.formats.html.fix_text(response["moa_title"]));
		buf_final+="<br>Description: "+(response["moa_description"]=="" ? "<span style=\"font-style:italic\">No Summary</span>" : wwwmoa.formats.html.fix_text(response["moa_description"]));


       		for(var x in response["parameters"]) {

		    cur_param=response["parameters"][x];

		    cur_value_esc=wwwmoa.formats.html.fix_text(cur_param.value);

		    buf_tmp="<div style=\"border:1px solid #A0A0A0; padding:1px; margin-bottom:2px; margin-top:1px\">";
		    buf_tmp+="<span style=\"font-weight:bold\">"+wwwmoa.formats.html.fix_text(x)+"</span>";
		    buf_tmp+=(cur_param.mandatory ? "<span style=\"font-weight:bold; color:#FF0000\">*</span>" : "")+"</span><br>";

		    if(cur_param.type=="string")
			buf_tmp+="<input type=\"text\" value=\""+cur_value_esc+"\" style=\"width:80%\">";
		    else
			buf_tmp+="<input type=\"text\" value=\"(format unknown)\" disabled=\"true\" style=\"width:80%\">";
		    
		    buf_tmp+="<br><span style=\"font-style:italic; font-size:12px; font-weight:bold; color:#008000; cursor:help\" onmouseout=\"this.innerHTML='[Mouse Over To View Description]';\" onmouseover=\"this.innerHTML='"+wwwmoa.formats.js.fix_text_for_html(cur_param.help)+"';\">[Mouse Over To View Description]</span>";

		    buf_tmp+="</div>";

		    if(buf_cat[cur_param.category]==null)
			buf_cat[cur_param.category]=[];
		    
		    buf_cat[cur_param.category].push(buf_tmp);

		    		    
		}
		
		buf_final+="<br><br><span style=\"font-weight:bold; text-decoration:underline\">General Parameters</span><br>";
		buf_final+=buf_cat[""];

		for(var x in buf_cat) {
		    if(x=="")
			continue;
		

		    buf_final+="<br><span style=\"font-weight:bold; text-decoration:underline\">"+wwwmoa.formats.html.fix_text(wwwmoa.util.str.title_case(x))+" Parameters</span><br>";

		    for(var y=0; y<buf_cat[x].length; y++)
			buf_final+=buf_cat[x][y];
		}



	        buf_final+="<br><span style=\"font-weight:bold; color:#FF0000\">*</span> denotes mandatory parameter";

		

		this.attr("visualCode", buf_final); // make main code "public"

	    }


	    })});

