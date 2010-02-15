
dojo.provide("wwwmoa.client.dhm.NavPanel");

dojo.require("dijit.form.DropDownButton");
dojo.require("dijit.form.ComboButton");
dojo.require("dijit.form.Button");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.Menu");
dojo.require("dijit.MenuItem");

dojo.require("wwwmoa.client.dhm._DHM");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.NavPanel", wwwmoa.client.dhm._DHM, {

		_location : "",
		_displayNode : null,
		_createButton : null,
		_createDialog : null,
		_createDialogTemplate : null,
		_createDialogTitle : null,
		_createDialogLocation : null,
		_runButton : null,
		_refreshButton : null,
		_runMenu : null,
		_createTemplate : null,
		_targetRequest : null,

		_setLocationAttr : function(val) {		    
		    this._cancelLoadTargets();

		    if(this.dhmIsLocked())
			return;

		    this._location=val;

		    this._initDisplay();

		    this._loadTargets();

		    this._resetCreateDialog();
		},

		_getLocationAttr : function() {
		    return this._location;
		},

		_loadTargets : function() {
		    if(this._targetRequest!=null)
			return;

		    this._runMenu.destroyDescendants(false);

		    this.dhmLock();

		    this._targetRequest=wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-job", this.attr("location")),
							   dojo.hitch(this, this._loadTargetsCallback),
							   8000);
		},

		_cancelLoadTargets : function() {
		    if(this._targetRequest==null)
			return;
		    
		    this._targetRequest.cancel();

		    this._targetRequest=null;

		    this.dhmUnlock();
		},

		_loadTargetsCallback : function(data) {
		    this._targetRequest=null;

		    if(data==null) {
			this.dhmUnlock();
			return;
		    }

		    var response=wwwmoa.formats.json.parse(data);
		    var targets=response["moa_targets"];
		    var item, item_event;
		    
		    for(var x=0; x<targets.length; x++) {
			item_event=dojo.hitch({obj : this, target : targets[x]},
					      function() {
						  this.obj._runJob(this.target);
					      });

			item=new dijit.MenuItem({label : wwwmoa.formats.html.fix_text(targets[x]),
						 onClick : item_event
			    });

			this._runMenu.addChild(item);
		    }

		    this.dhmUnlock();
		},

		_initDisplay : function() {
		    if(this._displayNode!=null)
			return;

		    this._displayNode=dojo.create("div", {style : {display : "inline"}});

		    this._createDialog=new dijit.TooltipDialog({});

		    this._createButton=new dijit.form.DropDownButton({label : "Create Job",
								      dropDown : this._createDialog
			});

		    this._runMenu=new dijit.Menu({});

		    this._runButton=new dijit.form.ComboButton({label : "Run Job",
								dropDown : this._runMenu,
								onClick : dojo.hitch(this, this._runJob),
								style : {fontWeight : "bold"}
			});

		    this._refreshButton=new dijit.form.Button({label : "Refresh",
							       onClick : dojo.hitch(this, this._reloadWD)
			});

		    this._loadTemplates();

		    this._displayNode.appendChild(this._runButton.domNode);
		    this._displayNode.appendChild(this._createButton.domNode);
		    this._displayNode.appendChild(this._refreshButton.domNode);

		    this._dhmSetVisualByNode(this._displayNode);
		},

		_loadTemplates : function() {
		    this.dhmLock();

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-templates", ""),
				       dojo.hitch(this, this._loadTemplatesCallback),
				       8000);
		},

		_loadTemplatesCallback : function(data) {
		    if(data==null)
			return;

		    var response=wwwmoa.formats.json.parse(data);
		    var templates=response["templates"];
		    
		    var help_text;
		    help_text="Please choose a template from the list below.<br>";
		    help_text+="Then, enter a title and location for the job, and press \"Create\".";

		    var main=dojo.create("div", {style : {fontSize : "12pt"}});
		    var help=dojo.create("div", {innerHTML : help_text});
		    var table=dojo.create("table", null);
		    var tbody=dojo.create("tbody", null);
		    var tr, td, td_event;
		    var createbutton, createbutton_event;
		    var resetbutton;
		    var cancelbutton, cancelbutton_event;


		    createbutton_event=function() {
			if(this._createDialogTemplate.attr("value")=="") {
			    alert("You must choose a template before you can create the job.");
			    return;
			}

			this._createJob(this._createDialogTemplate.attr("value"),
					this._createDialogLocation.attr("value"),
					this._createDialogTitle.attr("value"));

			dijit.popup.close(this._createDialog);
		    };

		    createbutton_event=dojo.hitch(this, createbutton_event);

		    cancelbutton_event=dojo.hitch(this, function() {
			    dijit.popup.close(this._createDialog);
			});

		    this._createDialogTitle=new dijit.form.TextBox({style : {width : "80%"}});
		    this._createDialogLocation=new dijit.form.TextBox({style : {width : "80%"}});
		    this._createDialogTemplate=new dijit.form.TextBox({disabled : true});

		    createbutton=new dijit.form.Button({label : "Create",
							onClick : createbutton_event
			});

		    resetbutton=new dijit.form.Button({label : "Reset",
						       onClick : dojo.hitch(this, this._resetCreateDialog)
			});

		    cancelbutton=new dijit.form.Button({label : "Cancel",
							onClick : cancelbutton_event
			});


		    main.appendChild(help);
		    main.appendChild(dojo.create("div", {innerHTML : "Template", style : {fontWeight : "bold"}}));
		    main.appendChild(this._createDialogTemplate.domNode);
		    main.appendChild(table);
		    main.appendChild(dojo.create("div", {innerHTML : "Title", style : {fontWeight : "bold"}}));
		    main.appendChild(this._createDialogTitle.domNode);
		    main.appendChild(dojo.create("div", {innerHTML : "Location", style : {fontWeight : "bold"}}));
		    main.appendChild(this._createDialogLocation.domNode);
		    main.appendChild(dojo.create("br", null));
		    main.appendChild(createbutton.domNode);
		    main.appendChild(resetbutton.domNode);
		    main.appendChild(cancelbutton.domNode);
		    table.appendChild(tbody);


		    for(var x=0; x<templates.length; x++) {
			if(x%4==0) {
			    tr=dojo.create("tr", null);

			    tbody.appendChild(tr);
			}

			td_event=function() {
			    this.obj._createDialogTemplate.attr("value", this.template);
			};

			td_event=dojo.hitch({obj : this, template : templates[x]}, td_event);
			
			td=dojo.create("td", {innerHTML : wwwmoa.formats.html.fix_text(templates[x]),
					      onclick : td_event,
					      style : {fontWeight : "bold",
						       textDecoration : "underline",
						       color : "#008000",
						       cursor : "pointer",
						       fontSize : "10pt",
						       paddingRight : "15px"
				}});

			tr.appendChild(td);
		    }

		    this._resetCreateDialog();

		    this._createDialog.attr("content", main);

		    this.dhmUnlock();
		},

		_resetCreateDialog : function() {
		    if(this._createDialogTitle==null)
			return;

		    this._createDialogTitle.attr("value", "Untitled");
		    this._createDialogLocation.attr("value", this.attr("location"));
		    this._createDialogTemplate.attr("value", "");
		},

		_createJob : function(template, location, title) {
		    if(this.dhmIsLocked())
			return;

		    this._createTemplate=template;
		    this._createTitle=title;
		    this._createLocation=location;

		    this.dhmLock();

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("s", this._createLocation),
				       dojo.hitch(this, this._createJobLocationCallback),
				       4000);
		},

		_createJobLocationCallback : function(data) {

		    if(data==null) {
			alert("The location you choose does not exist.  Please try again.");
			this.dhmUnlock();
			return;
		    }

		    var response=wwwmoa.formats.json.parse(data);

		    if(response["size"]!=-1) {
			alert("The location you choose is not a directory.  Please try again.");
			this.dhmUnlock();
			return;
		    }

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("moa-job", this._createLocation),
				       dojo.hitch(this, this._createJobInfoCallback),
				       8000);

		},

		_createJobInfoCallback : function(data) {
		    var args;
		    var confirm_text;
		    confirm_text="Creating a new job will overwrite the existing one.  ";
		    confirm_text+="Please confirm that you wish to continue.";

		    if(data!=null)
			if(!confirm(confirm_text)) {
			    this.dhmUnlock();
			    return;
			}

		    args="?";
		    args+="&template="+wwwmoa.io.rl.url_encode(this._createTemplate);
		    args+="&title="+wwwmoa.io.rl.url_encode(this._createTitle);

		    wwwmoa.io.ajax.put(wwwmoa.io.rl.get_api("moa-job"+args, this._createLocation),
				       dojo.hitch(this, this._createJobCallback),
				       8000);
		},

		_createJobCallback : function(data) {
		    this._resetCreateDialog();

		    this.dhmUnlock();

		    this._reloadWD();
		},

		_runJob : function(target) {
		    var args;

		    args=(target==null ? "" : "?target="+wwwmoa.io.rl.url_encode(target));

		    wwwmoa.io.ajax.put(wwwmoa.io.rl.get_api("moa-jobsession"+args, this.attr("location")),
				       null,
				       8000);
		},

		_reloadWD : function() {
		    this._dhmGetManager().dhmRequest({type : wwwmoa.dhm.DHM_REQ_WDNAV,
				                      args : {path : this.attr("location")}
			});
		},

		_dhmLockVisual : function() {
		    this._createButton.attr("disabled", true);
		    this._runButton.attr("disabled", true);
		},

		_dhmUnlockVisual : function() {
		    this._createButton.attr("disabled", false);
		    this._runButton.attr("disabled", false);
		},

		dhmNotify : function(message) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_WDNAV)
			this.attr("location", message.args.path);
		}

	    })});