
dojo.provide("wwwmoa.client.dhm.PBrowser");

dojo.require("wwwmoa.client.store.Params");
dojo.require("wwwmoa.client.dhm._DHM");

dojo.require("dojo.string");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.PBrowser", wwwmoa.client.dhm._DHM, {

		_location : "",

		_setLocationAttr : function(val) {
		    this._location=val;
		    this._navToLocation();
		},

		_getLocationAttr : function() {
		    return this._location;
		},

		_navToLocation : function() {
		    this._dhmSetVisualByCode("Loading job information...");

		    this.dhmLock();

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-job", this.attr("location")),dojo.hitch(this,this._dataCallback) , 8192); // be somewhat patient about receiving the listing
		},

                // Receives data from the API request.  Then, it creates the HTML code that
                // will be used to display the job view contents.
                _dataCallback : function(data) {
		    if(data==null) { // if null was passed, we have an error
			this._dhmSetVisualByCode("No job information is available."); // create an error message
			this.dhmUnlock();
			return;
		    }

		    var response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data
		    var dom_final=null; // holds the DOM that all of the final visual elements get attached to
		    var dom_table=null; var dom_tbody=null; var dom_curtr; var dom_curtd;
		    var title=wwwmoa.formats.html.fix_text(dojo.string.trim(response["moa_title"]));
		    var summary=wwwmoa.formats.html.fix_text(dojo.string.trim(response["moa_description"]));
		    var title_exists=(title!="");
		    var summary_exists=(summary!="");
		    var targets=response["moa_targets"];

		    // create parent DOM node
		    dom_final=dojo.create("div", null);

		    // create DOM structure for general information section
		    dom_final.appendChild(dojo.create("span", {
				style : {
		                        fontWeight : "bold",
				        textDecoration : "underline"
				},
				innerHTML : "Template"
		    })); // create section heading

		    dom_table=dojo.create("table", null);
		    dom_tbody=dojo.create("tbody", null);
		    dom_table.appendChild(dom_tbody);

		    dom_curtr=dojo.create("tr", null);
		    dom_tbody.appendChild(dom_curtr);
		    dom_curtd=dojo.create("td", {innerHTML : "Title", style : {fontWeight : "bold"}});
		    dom_curtr.appendChild(dom_curtd);
		    dom_curtd=dojo.create("td", {
			    innerHTML : (title_exists ? title : "Untitled"),
			    style : (title_exists ? {} : {fontStyle : "italic"})
		    });
		    dom_curtr.appendChild(dom_curtd);

		    dom_curtr=dojo.create("tr", null);
		    dom_tbody.appendChild(dom_curtr);
		    dom_curtd=dojo.create("td", {innerHTML : "Description", style : {fontWeight : "bold"}});
		    dom_curtr.appendChild(dom_curtd);
		    dom_curtd=dojo.create("td", {
			    innerHTML : (summary_exists ? summary : "No Summary"),
			    style : (summary_exists ? {} : {fontStyle : "italic"})
		    });
		    dom_curtr.appendChild(dom_curtd);

		    dom_curtr=dojo.create("tr", null);
		    dom_tbody.appendChild(dom_curtr);
		    dom_curtd=dojo.create("td", {innerHTML : "Targets", style : {fontWeight : "bold"}});
		    dom_curtr.appendChild(dom_curtd);
		    dom_curtd=dojo.create("td", null);
		    dom_curtr.appendChild(dom_curtd);

		    for(var t in targets) {
			dom_curtd.innerHTML+=(dom_curtd.innerHTML=="" ? "" : ", ");
			dom_curtd.innerHTML+=wwwmoa.formats.html.fix_text(targets[t]);
		    }

		    dom_final.appendChild(dom_table);

		    this._dhmSetVisualByNode(dom_final); // make main code "public"

		    this.dhmUnlock();
		},

		dhmNotify : function(message) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_WDNAV)
			this.attr("location", message.args.path);
		},

		dhmPoll : function(poll) {
		    if(poll.type==wwwmoa.dhm.DHM_PLL_SHUTDOWN)
			return true;
		    else if(poll.type==wwwmoa.dhm.DHM_PLL_WDNAV)
			return !this.dhmIsLocked();
		}

	    })});
