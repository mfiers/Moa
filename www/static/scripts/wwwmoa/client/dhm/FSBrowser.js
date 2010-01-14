
dojo.provide("wwwmoa.client.dhm.FSBrowser");
dojo.require("dijit._Widget");

dojo.addOnLoad(function() { dojo.declare("wwwmoa.client.dhm.FSBrowser", dijit._Widget, {



            /* * * * * * * * * * * * * * * */
	    /* * * * * * Storage * * * * * */
	    /* * * * * * * * * * * * * * * */


       	    _visualDOM : null, // holds the visual node to publish (Node)
	    _locked : false, // holds whether or not the input to the widget should be suppressed (boolean)
	    _response : null, // holds the last response received from the API (parsed JSON)
	    _location : "", // holds the current location (string)
	    _locationComponents : [], // holds the location components from the last response received from the API (Array of String)
	    _startIndex : 1, // holds the current start index, which is a 1-based index that represents the first item to be shown (number)
	    _indexCount : 15, // holds the current index count, which represents how many items (max) to show at once (number)
	    _expandedIndexCount : 100, // holds the current expanded index count, which represents how many items (max) to show at once when expanded (number)
	    _colCount : 5, // holds how many columns to display the results in when expanded (number)
	    _dhmManager : null, // holds the current DHM Manager, which should be contacted for certain operations (Object)
	    _filter : "", // holds the filter search phrase (string)
	    _filterType : "contains", // holds the filter search criteria (string)
	    _filterOn : false, // holds whether or not the filter should be used (boolean)
	    _expanded : false, // holds whether or not the widget is expanded (boolean)
	    _expandedNode : null, // holds the node to publish to while in expanded mode (Node)



	    /* * * * * * * * * * *  * * * * * * * * * * * */
	    /* * * * * * Initializing Functions * * * * * */
	    /* * * * * * * * * * *  * * * * * * * * * * * */


	    buildRendering : function() {
		this.domNode=dojo.create("div", null);
		this._refreshVisual();
	    },



	    /* * * * * * * * * * * * * * * * * * * * * * * * * * */
	    /* * * * * * Attribute Setters and Getters * * * * * */
	    /* * * * * * * * * * * * * * * * * * * * * * * * * * */


	    _setVisualDOMAttr : function(val) {
	        this._visualDOM=val;
		this._refreshVisual();
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

	    _getColCountAttr : function() {
		if(this._expanded)
		    return this._colCount;
		else
		    return 1;
	    },

	    _setColCountAttr : function(val) {
		try {
		   fix_val=Math.floor(new Number(val));

		   if(fix_val<1)
		       this._colCount=1;
		   else
		       this._colCount=fix_val;
		}
		catch(err) {}
	    },

	    _setLocationAttr : function(val) {
		this._location=val;
		this.attr("startIndex", 0);
		this._navToLocation();
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
		if(val<1)
		    this._startIndex=1;
		else
		    this._startIndex=val;
	    },

	    _getStartIndexAttr : function() {
		return this._startIndex;
	    },

	    _setFilterAttr : function(val) {
		this._filter=val;
	    },

	    _getFilterAttr : function() {
		return this._filter;
	    },

	    _setFilterTypeAttr : function(val) {
	        this._filterType=val;
	    },

	    _getFilterTypeAttr : function() {
		return this._filterType;
	    },

	    _setFilterOnAttr : function(val) {
		this._filterOn=val;
	    },

	    _getFilterOnAttr : function() {
		return this._filterOn;
	    },

	    _setIndexCountAttr : function(val) {
		var val_fixed;

		if(val<1)
		    val_fixed=1;
		else if(val>500)
		    val_fixed=500;
		else
		    val_fixed=val;

		if(this._expanded)
		    this._expandedIndexCount=val_fixed;
		else
		    this._indexCount=val_fixed;
	    },

	    _getIndexCountAttr : function() {
		if(this._expanded)
		    return this._expandedIndexCount;
		else
		    return this._indexCount;
	    },

	    // A psuedo-property that returns HTML code that can be used to create a "breadcrumb" representation of the current location.
	    _getLocationBreadcrumbCodeAttr : function() {
		var locationComponents=this.attr("locationComponents");
		var code="<span style=\"font-weight:bold\"><img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdiroprtA")) + "\" alt=\"Directory\"> <span style=\"color:#0000FF; text-decoration:underline; cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._contact('rtx');\">Root</span>";
		
		for(var x=0; x<locationComponents.length; x++) {
		    code+=" / <span style=\"color:#0000FF; text-decoration:underline; cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._contact('par-"+x+"');\">"+wwwmoa.formats.js.fix_text_for_html(locationComponents[x]["name"])+"</span>";
		}

		code+="</span>";
		
		return code;

	    },




            /* * * * * * * * * * * * * * * * * * * * * */
	    /* * * * * * Navigation Routines * * * * * */
            /* * * * * * * * * * * * * * * * * * * * * */
	    
	    // Starts a navigation to the location specified in the "location" attribute.
	    _navToLocation : function() {
		var location="";
		var api_command="ls?start="+this.attr("startIndex")+"&end="+(this.attr("startIndex")+this.attr("indexCount")-1);
		
		if(this.attr("filterOn"))
		    api_command+="&filter="+wwwmoa.io.rl.url_encode(this.attr("filter"))+"&filter-type="+wwwmoa.io.rl.url_encode(this.attr("filterType"));

		if(this.attr("location")!==undefined)
		    location=this.attr("location");
		    
		this.attr("locked", true);
		
		wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api(api_command, location),dojo.hitch(this, function(data) {
			this._processAPIResponse(data); // use the callback function of this object
		    }), 8192); // be somewhat patient about receiving the listing
	    },

	    // Checks whether or not navigating to the given start index can be done successfully.
	    _isStartIndexOpValid : function(newsi) {
		if((typeof newsi != "number")&& (typeof newsi != "Number"))
		    return false;

		if(newsi==Number.NaN)
		    return false;

		if(newsi>this.attr("response")["ls-available"])
		    return false;

		if(newsi<1) 
		    return false;
		
		return true;
	    },

	    // Updates the "startIndex" attribute, if navigating to the given start index can be done successfully.
	    _startIndexOp : function(newsi) {
	        if(this._isStartIndexOpValid(newsi))
		    this.attr("startIndex", newsi);
	    },

	    // Checks whether or not navigating to the given index count can be done successfully.
	    _isIndexCountOpValid : function(newic) {
		if((typeof newic != "number")&& (typeof newic != "Number"))
		    return false;

		if(newic==Number.NaN)
		    return false;

		if(newic<1) 
		    return false;
		
		return true;
	    },

	    // Updates the "indexCount" attribute, if navigating to the given index count can be done successfully.
	    _indexCountOp : function(newic) {
	        if(this._isIndexCountOpValid(newic))
		    this.attr("indexCount", newic);
	    },

	    // Checks whether or not navigating to the given column count can be done successfully.
	    _isColCountOpValid : function(newic) {
		if((typeof newic != "number")&& (typeof newic != "Number"))
		    return false;

		if(newic==Number.NaN)
		    return false;

		if(newic<1) 
		    return false;
		
		return true;
	    },

	    // Updates the "colCount" attribute, if navigating to the given column count can be done successfully.
	    _colCountOp : function(newcc) {
	        if(this._isColCountOpValid(newcc))
		    this.attr("colCount", newcc);
	    },

    	    // Starts a navigation to the start index specified, preserving the other parameters set earlier.  If the start index cannot be navigated to successfully, the start index is not changed, but the navigation is still carried out.
	    _navToIndex : function(newsi) {
		var newsi_fixed=Math.floor(new Number(newsi));

		if(this.attr("locked"))
		    return;

		this._startIndexOp(newsi_fixed);
		this._navToLocation();
	    },

    	    // Starts a navigation to the index count specified, preserving the other parameters set earlier.  If the index count cannot be navigated to successfully, the index count is not changed, but the navigation is still carried out.
	    _navToIndexCount : function(newic) {
		var newic_fixed=Math.floor(new Number(newic));

		if(this.attr("locked"))
		    return;

		this._indexCountOp(newic_fixed);
		this._navToLocation();
	    },

    	    // Starts a navigation to the column count specified, preserving the other parameters set earlier.  If the column count cannot be navigated to successfully, the column count is not changed, but the navigation is still carried out.
	    _navToColCount : function(newcc) {
		var newcc_fixed=Math.floor(new Number(newcc));

		if(this.attr("locked"))
		    return;

		this._colCountOp(newcc_fixed);
		this._navToLocation();
	    },

    	    // Starts a navigation to the previous index group, preserving the other parameters set earlier.  If the current index group is already the first, the navigation is still carried out without changing the start index.
	    _navToIndexPrevGroup : function() {
		if(this.attr("locked"))
		    return;

		this._startIndexOp(this.attr("startIndex")-this.attr("indexCount"));
		this._navToLocation();
	    },

    	    // Starts a navigation to the next index group, preserving the other parameters set earlier.  If the current index group is already the last, the navigation is still carried out without changing the start index.
	    _navToIndexNextGroup : function() {
		if(this.attr("locked"))
		    return;

		this._startIndexOp(this.attr("startIndex")+this.attr("indexCount"));
		this._navToLocation();
	    },

    	    // Starts a navigation to the first index group, preserving the other parameters set earlier.  The navigation is carried out even if the current index group is already the first.
	    _navToIndexFirstGroup : function() {
		if(this.attr("locked"))
		    return;

		this._startIndexOp(1);
		this._navToLocation();
	    },

    	    // Starts a navigation to the last index group, preserving the other parameters set earlier.  The navigation is carried out even if the current index group is already the last.
	    _navToIndexLastGroup : function() {
		if(this.attr("locked"))
		    return;

		this._startIndexOp(Math.max(1, this.attr("response")["ls-available"]-this.attr("indexCount")+1));
		this._navToLocation();
	    },

	    // Starts a navigation to the first index group using a given filter, preserving the other parameters set earlier.
	    _navToFilter : function(filter) {
		if(this.attr("locked"))
		    return;

		if(filter=="")
		    return;

		this.attr("filterOn", true);
		this.attr("filter", filter);
		this._startIndexOp(1);
		this._navToLocation();
	    },

	    // Starts a navigation to the first index group after removing a filter if it is present, preserving the other parameters set earlier.
	    _navToNoFilter : function() {
		if(this.attr("locked"))
		    return;

		this.attr("filterOn", false);
		this._startIndexOp(1);
		this._navToLocation();
	    },

	    // Takes the previously generated HTML and packages it for viewing.  Then, it pushes the HTML code into the visual node so that it is visible.
	    _refreshVisual : function() {
                var node;

		if(this.domNode==null) // if we do not have a visual node
		    return; // there is no reason to proceed

		if(this.attr("visualCode")==null) // if either the main code or the current directory item code is not present
		    node=dojo.create("div", null); // create blank section
		else // if both the main code and the current directory item code is present
		    node=this.attr("visualDOM");

		dojo.forEach(dijit.findWidgets(this.domNode), function(item) {item.destroyRecursive(false);});
		dojo.empty(this.domNode);

		if(this._expanded) {
		    dojo.forEach(dijit.findWidgets(this._expandedNode), function(item) {item.destroyRecursive(false);});

		    dojo.empty(this._expandedNode);
		    
		    this._expandedNode.appendChild(node);
		}
		else {
		    this.domNode.appendChild(node);
		}
	    },


	    /* * * * * * * * * *  * * * * * * * * * * */
	    /* * * * * * Callback Functions * * * * * */
	    /* * * * * * * * * *  * * * * * * * * * * */


            // Receives data from the API request.  Then, it creates the HTML code that will be used to display the directory contents.  Finally, it requests an update of the visual node.
            _processAPIResponse : function(data) {
		
                // Helper function that properly truncates a name.
		var truncName=function(str) {
                    var strtrunc=str.substr(0,24); // cap characters at 24

		    if(str.length!=strtrunc.length) { // if caping characters made a difference
			strtrunc=strtrunc.substr(0,21); // cap characters at 13, so there will be 24  characters in total
			strtrunc+="..."; // add on ...
		    }

		    return strtrunc;
		};
		
		var ls_response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data
		var no_read=0;
		var buf_code=""; // buffer for visual code

		var is_dir=false; // holds whether the currently processed item is a directory or not
		var files_exist=false;  // holds whether or not the current directory has any items
		var col_count=this.attr("colCount");

		this.attr("response", ls_response); // save the parsed response we have received for later use
		

		if(data!=null) {

		    this.attr("locationComponents", ls_response["dir"]);

		    if(this._expanded)
			buf_code+=this.attr("locationBreadcrumbCode");


		    buf_code+="<div style=\"font-size:10pt; text-align:center\">currently showing <span style=\"font-weight:bold;\">"+ this.attr("startIndex") +"</span> to <span style=\"font-weight:bold\">"+ Math.min((this.attr("startIndex")+this.attr("indexCount")-1), ls_response["ls-available"]) +"</span> out of <span style=\"font-weight:bold\">"+ls_response["ls-available"]+"</span>";


		    buf_code+="<br>in a group of <select style=\"font-weight:bold\" onchange=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndexCount(this.value);\">";

		    for(var x=(this._expanded ? 50 : 5); x<=(this._expanded ? 500 : 50); x+=(this._expanded ? 50 : 5)) {
			buf_code+="<option value=\""+x+"\""+ (x==this.attr("indexCount") ? " selected=\"selected\"" : "") +">"+x+"</option>";
		    }

		    buf_code+="</select>";


		    if(this._expanded) {
			buf_code+=" in <select style=\"font-weight:bold\" onchange=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToColCount(this.value);\">";

			for(var x=1; x<=10; x++) {
			    buf_code+="<option value=\""+x+"\""+ (x==this.attr("colCount") ? " selected=\"selected\"" : "") +">"+x+"</option>";
			}

			buf_code+="</select> columns";
		    }

		    
		    buf_code+="</div>";
		}


		// add navigation options
		buf_code+="<div style=\"font-weight:bold; font-size:14pt; color:#0000FF; text-align:center\">";
		
		buf_code+="<span style=\"cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndexFirstGroup();\" title=\"Go to the beginning of the list.\">&lArr;</span>";

		buf_code+=" <span style=\"cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndexPrevGroup();\" title=\"Go to the previous group of the list.\">&larr;</span> <span style=\"color:#000000\">|</span>";

		if(!this._expanded) {
		    buf_code+=" <span style=\"cursor:pointer\" title=\"Show expanded view.\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._expand();\">E</span> ";

		    buf_code+="<span style=\"color:#000000\">|</span>";
		}

		buf_code+=" <span style=\"cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndexNextGroup();\" title=\"Go to the next group of the list.\">&rarr;</span>";

		buf_code+=" <span style=\"cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndexLastGroup();\" title=\"Go to the end of the list.\">&rArr;</span>";

		buf_code+="</div>";

		buf_code+="<div style=\"text-align:center\"><input type=\"text\" style=\"width:15%\"><button onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToIndex(this.previousSibling.value);\">Goto</button> <input type=\"text\" style=\"width:30%\"><button onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToFilter(this.previousSibling.value);\">Search</button></div>";

		if(this.attr("filterOn")) {
		    buf_code+="<div style=\"font-size:10pt; border:1px solid #008000; background-color:#F0FFF0; padding:2px\">You are currently viewing the results of a search for &quot;"+ wwwmoa.formats.html.fix_text(this.attr("filter")) +"&quot;.  To view all of the contents of the directory, <span style=\"color:#0000FF; text-decoration:underline; cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToNoFilter();\">click here</span>.</div><br>";
		}

		if(data==null) { // if null was passed, we have an error
		    buf_code+="<div style=\"font-size:10pt; border:1px solid #800000; background-color:#FFF0F0; padding:2px\">Sorry, but the directory contents could not be loaded.<span style=\"color:#0000FF; text-decoration:underline; cursor:pointer\" onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._navToLocation();\">Click here</span> to try again.</div>"; // create an error message
		    this.attr("locked", false);
		    
		    this.attr("visualCode", buf_code); // make main code "public"
		    return;
		}


		// start structural table
		buf_code+="<table style=\"font-weight:bold; font-size:10pt\">";


		var_colour="";

		var y;

		for(var x=0; x<ls_response["ls"].length; x++) { // for each item in the current directory
		    if(!ls_response["ls"][x]["read-allowed"]) { // if we cannot read a file
			no_read++; // make a note of it
			continue; // do not bother even showing it
		    }

		    is_dir=(ls_response["ls"][x]["type"]=="dir"); // find whether the item is a dir or not
		    
		    files_exist|=!is_dir; // if this item is a file, remember that we have encountered files
		    
		    name_colour=(ls_response["ls"][x]["write-allowed"] ? "#0000FF" : "#C0C0C0");



		    if(!this._expanded || (x%col_count==0))
			buf_code+="<tr style=\"margin:0px\">";

		    buf_code+="<td>";

		    
		    
		    if(!is_dir) { // if the item is a file
			// create code for start of entry for a file
			buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSfileA")) + "\" alt=\"File\" style=\"vertical-align:middle\"> ";
		    }
		    else { // if the item is a directory
			// create code for start of entry for a directory
			
			if(ls_response["ls"][x]["x-is-moa"]) // if the item is a moa directory
			    buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdirclmoaA")) + "\" alt=\"Moa\" title=\"This item is a Moa directory.\" style=\"vertical-align:middle\"> "; // give it special annotation
			else // if the item is not a moa directory
			    buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSdirclA")) + "\" alt=\"Directory\" style=\"vertical-align:middle\"> "; // give it normal annotation
			    }

		    buf_code+="<span style=\"font-weight:bold; color:"+name_colour+"; text-decoration:underline; cursor:pointer\" ";
		        
		    // add code to allow for item selection
		    buf_code+="onclick=\"dijit.byId('" + wwwmoa.formats.js.fix_text_for_html(this.id) + "')._contact('itm-" + x + "');\" onmouseover=\"this.style.textDecoration='none';\" onmouseout=\"this.style.textDecoration='underline';\"";
		   
		    
		    // start creating basic entry code (which is the same for files and directories)
		    buf_code+=" title=\""+wwwmoa.formats.html.fix_text(ls_response["ls"][x]["name"])+"\">";
		    buf_code+=wwwmoa.formats.html.fix_text(truncName(ls_response["ls"][x]["name"])); // add the name of the file
		    buf_code+="</span>";

		    buf_code+="</td><td>";

		    if(ls_response["ls"][x]["link"]) // if the item is a link
			buf_code+="<img src=\"" + wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("FSlinkA")) + "\" alt=\"Link\" title=\"This item is actually a link.\">"; // give it the proper annotation


		    buf_code+="</td>";


		    if(!this._expanded || (x%col_count==col_count-1))
			buf_code+="</tr>";


		    y=x;
                }

		if(y%col_count!=col_count-1)
		    buf_code+="</tr>";

		// end structural table
		buf_code+="</table>";

		// print the number of unreadable files, if any were encountered
		if(no_read>0)
		    buf_code+="<span style=\"font-size:10pt\">("+no_read+" unreadable items, not displayed)</span><br>"


		this.attr("visualCode", buf_code); // make main code "public"
		
		
		this.attr("locationIsMoa", ls_response["x-dir-is-moa"]);
	    

		this.attr("locked", false); // requests can now be sent again without a problem

		this._dhmManager.dhmNotify({type : wwwmoa.dhm.DHM_MSG_DATA, args : { key : "locationBreadcrumbCode", data : this.attr("locationBreadcrumbCode") }}, this);
	    },


           // Callback for receiving "contact messages".
           _contact : function(data) {
		var path;
		var item_index;


		if(this.attr("locked")) // if we are locked
		    return; // we should not do anything, so exit

		if(this.attr("response")==null) // if we do not have a response from api call
		    return; // we cannot do anything, so exit

		// everything seems to be good, so convert the item index if it exists
		try {
		    item_index=new Number(data.substr(4)); // item index always starts at 5th character, if it exists at all
		}
		catch(err) { // on conversion failure
		    item_index=0; // assume an index of 0
		}
		
		if(data.substr(0,3)=="rtx") // if the message sent requested a change to the root directory
		    path=""; // use a blank string for the path
		else if(data.substr(0,4)=="par-") // if the message sent requested a parent directory
		    path=this.attr("response")["dir"][item_index]["path"]; // retrieve the pathname associated with the parent directory
		else if(data.substr(0,4)=="itm-") { // if the message sent requested an item in the current directory
		    path=this.attr("response")["ls"][item_index]["path"]; // retrieve the pathname associated with the item

		    if(this.attr("response")["ls"][item_index]["type"]=="file")
			return;
		}
		else // if the message has not yet been recognized
		    return; // we should just exit
		
		this._changeWD(path); // pass the pathname to be handled properly
	    },


	    /* * * * * * * * * * * * * * * * * * * * * * */
	    /* * * * * * Misc Helper Functions * * * * * */
	    /* * * * * * * * * * * * * * * * * * * * * * */


	    // Attempts to change the current working directory.
	    _changeWD : function(path) {
		this.attr("filterOn", false);

		this._dhmManager.dhmRequest({type : wwwmoa.dhm.DHM_REQ_WDNAV, args : { path : path}}, this);
	    },

	    // Attempts to open the widget in "expanded mode".
	    _expand : function() {
		this._expanded=true;
		if(!this._dhmManager.dhmRequest({type : wwwmoa.dhm.DHM_REQ_MODAL, args : { title : "File Browser", body : "Test Body" }}, this)) {
		    this._expanded=false;
		    return;
		}

		if(!this._expanded)
		    return;

		this.attr("visualCode", null);
	    },



	    /* * * * * * * * * * * *  * * * * * * * * * * * * */
	    /* * * * * * DHM Communication Handlers * * * * * */
	    /* * * * * * * * * * * *  * * * * * * * * * * * * */

	    dhmNotify : function(message) {
		if(message.type == wwwmoa.dhm.DHM_MSG_WDNAV) {
		    this.attr("locked", true);
		    this.attr("location", message.args.path); // set the new location
		}

		if(message.type == wwwmoa.dhm.DHM_MSG_MODAL_GAIN_CTRL) {
		    this._expandedNode=message.args.node;
		    this._navToLocation();
		}

		if(message.type == wwwmoa.dhm.DHM_MSG_MODAL_LOOSE_CTRL) {
		    if(this._expandedNode==message.args.node) {
			this._expandedNode==null;
			this._expanded=false;
			this._navToLocation();
		    }
		}
	    },

	    dhmPoll : function(poll) {
		if(poll.type == wwwmoa.dhm.DHM_PLL_SHUTDOWN)
		    return true;
		else if(poll.type == wwwmoa.dhm.DHM_PLL_WDNAV)
		    return !this.attr("locked");
 	    },

	    dhmPoint : function(manager) {
		this._dhmManager=manager;
	    }

	})});

