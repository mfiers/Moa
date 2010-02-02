
dojo.provide("wwwmoa.client.dhm.JobStatusViewer");

dojo.require("wwwmoa.client.dhm._DHM");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.JobStatusViewer", wwwmoa.client.dhm._DHM, {

		_location : "",
		_displayNode : null,
		_outputDisplayNode : null,
		_timeout : null,
		_request : null,
		_outputRequest : null,

		_setLocationAttr : function(val) {
		    if(this.dhmIsLocked())
			return;

		    this._location=val;

		    this._resetOutputDisplay();

		    this._navToLocation();
		},

		_getLocationAttr : function() {
		    return this._location;
		},

		_navToLocation : function() {
		    if(this._request!=null)
			this._request.cancel();

		    clearTimeout(this._timeout);

		    this._request=wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-jobsession", this.attr("location")),
				                     dojo.hitch(this,this._dataCallback),
				                     3000);
		},

		_dataCallback : function(data) {
		    var response;
		    
		    this._request=null;

		    if(data==null)
			this._showStatus("");
		    else {
			response=wwwmoa.formats.json.parse(data);
			this._showStatus(response["status"]);
		    }

		    this._timeout=setTimeout(dojo.hitch(this,this._navToLocation), 4000);
		},

		_dataOutputCallback : function(data) {
		    var response, nodes;
		    	    
		    this._outputRequest=null;

		    this._createDisplay();

		    nodes=dojo.query("> div", this._outputDisplayNode);

		    if(data==null) {
			this._resetOutputDisplay();
			
			nodes[0].innerHTML="The outputs for the Moa job could not be loaded.<br>";
			nodes[0].innerHTML+="Click here to try again.";
		    }
		    else {
			response=wwwmoa.formats.json.parse(data);

			nodes[0].innerHTML="The outputs may have changed since you last loaded them.<br>";
			nodes[0].innerHTML+="Click here to refresh them.";

			nodes[1].style.visibility="visible";
			nodes=dojo.query("> div", nodes[1]);

			this._setOutputBoxNode(nodes[1], response["output"], "There is no main output.");
			this._setOutputBoxNode(nodes[3], response["output-error"], "There are no error messages.");
		    }
		},

		_setOutputBoxNode : function(node, output, message) {
		    var content=(output=="" ? message : output);

		    node.style.fontStyle=(output=="" ? "italic" : "normal");

		    node.innerHTML=wwwmoa.formats.html.translate_text(content);
		},

		_createDisplay : function() {
		    var status_node, longstatus_node;
		    var outputrefresh_node;
		    var outputcont_node, outputbox_node, outputerrorbox_node;

		    var outputbox_style={border : "1px solid #000000",
					 padding : "4px",
					 color : "#000000",
					 backgroundColor : "#C0C0C0",
					 fontFamily : "monospace",
					 marginTop : "8px",
					 marginBottom : "4px"
		    };
		    var outputboxlabel_style={fontWeight : "bold",
					      textDecoration : "underline"
		    };


		    if(this._displayNode!=null)
			return;

		    this._displayNode=dojo.create("div", null);

		    status_node=dojo.create("div", {style : {fontSize : "14pt",
							     fontWeight : "bold"
			    }});

		    longstatus_node=dojo.create("div", null);

		    this._outputDisplayNode=dojo.create("div", {style : {border : "1px solid #000000",
									 padding : "4px",
									 marginTop : "8px"
			    }});

		    outputrefresh_node=dojo.create("div", {style : {fontWeight : "bold",
								    color : "#0000FF",
								    textDecoration : "underline",
								    cursor : "pointer"
			    }});

		    outputcont_node=dojo.create("div", {style : {marginTop : "20px"}});

		    outputbox_node=dojo.create("div", {style : outputbox_style});
		    outputerrorbox_node=dojo.create("div", {style : outputbox_style});

		    this._displayNode.appendChild(status_node);
		    this._displayNode.appendChild(longstatus_node);
		    this._displayNode.appendChild(this._outputDisplayNode);
		    this._outputDisplayNode.appendChild(outputrefresh_node);
		    this._outputDisplayNode.appendChild(outputcont_node);

		    outputcont_node.appendChild(dojo.create("div", {style : outputboxlabel_style,
				                                    innerHTML : "Main Output"
				    }));
		    outputcont_node.appendChild(outputbox_node);
		    outputcont_node.appendChild(dojo.create("div", {style : outputboxlabel_style,
				                                    innerHTML : "Error Messages"
				    }));
		    outputcont_node.appendChild(outputerrorbox_node);
		    
		    this._resetOutputDisplay();
		},

		_resetOutputDisplay : function() {
		    var nodes;

		    if(this._outputRequest!=null)
			this._outputRequest.cancel();

		    this._createDisplay();

		    nodes=dojo.query("> div", this._outputDisplayNode);

		    nodes[0].innerHTML="Click here to load the outputs for this Moa job.";
		    nodes[0].onclick=dojo.hitch(this, this._refreshOutputDisplay);
		    nodes[1].style.visibility="hidden";

		    nodes=dojo.query("> div", nodes[1]);
		    nodes[1].innerHTML="";
		    nodes[3].innerHTML="";
		},

		_refreshOutputDisplay : function() {
		    if(this._outputRequest!=null)
			return;

		    this._createDisplay();

		    this._outputRequest=wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-jobsession?output=1", this.attr("location")),
							   dojo.hitch(this,this._dataOutputCallback),
							   8000);

		    var nodes=dojo.query("> div", this._outputDisplayNode);
		    nodes[0].innerHTML="Attempting to load outputs...";
		},

		_showStatus : function(rawstatus) {
		    var status, status_colour, status_summary, status_ismoa=true;
		    var nodes;

		    this._createDisplay();

		    status=wwwmoa.util.str.title_case(rawstatus);

		    switch(rawstatus) {
			case "waiting":
			    status_colour="#0000A0";
			    status_summary="The Moa job is waiting to be run, or is waiting ";
			    status_summary+="for its children to finish running.\n\nAlthough the ";
			    status_summary+="Moa job may have been run in the past, no information ";
			    status_summary+="could be found to indicate whether it was successful ";
			    status_summary+="or not.  You may consider checking the outputs of the ";
			    status_summary+="Moa job using the option below.";
			    break;
			case "success":
			    status_colour="#00A000";
			    status_summary="The Moa job finished successfully!\n\nTo view the ";
			    status_summary+="details, you can check the outputs of the Moa job ";
			    status_summary+="using the option below.";
			    break;
			case "failed":
			    status_colour="#A00000";
			    status_summary="The Moa job failed.\n\nThe outputs of the Moa job ";
			    status_summary+="may indicate why.  You can view the outputs by using ";
			    status_summary+="the option below.";
			    break;
			case "running":
			    status_colour="#C06030";
			    status_summary="The Moa job is currently running.";
			    break;
			case "locked":
			    status_colour="#000000";
			    status_summary="The Moa job has been locked.";
			    break;
		        case "":
			    status_colour="#000000";
			    status_summary="The Moa job's status could not be loaded. However, ";
			    status_summary+="you may still attempt to load the outputs using the ";
			    status_summary+="option below.";
			    status="(Status Not Available)";
			    break;
		        default:
			    status_colour="#B0B0B0";
			    status_summary="A Moa job is not currently selected.";
			    status="(Not a Moa Job)";
			    status_ismoa=false;
		    }

		    status_summary+="\n\nThe status displayed here will be updated frequently ";
		    status_summary+="(if the server running WWWMoa can be reached). Therefore, ";
		    status_summary+="you may want to check back to see how things are going.";

		    nodes=dojo.query("> div", this._displayNode);

		    nodes[0].style.color=status_colour;
		    nodes[0].innerHTML=wwwmoa.formats.html.fix_text(status);
		    nodes[1].innerHTML=wwwmoa.formats.html.translate_text(status_summary);

		    nodes[2].style.visibility=(status_ismoa ? "visible" : "hidden");

		    if(!status_ismoa)
			this._resetOutputDisplay();

		    this._dhmSetVisualByNode(this._displayNode);
		},

		dhmNotify : function(message) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_WDNAV)
			this.attr("location", message.args.path);
		}

	    })});