dojo.provide("wwwmoa.client.Client");
dojo.require("dijit.Dialog");
dojo.require("dijit._Widget");

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.layout.TabContainer");

dojo.require("wwwmoa.client.dhm.FSBrowser");
dojo.require("wwwmoa.client.dhm.PBrowser");
dojo.require("wwwmoa.client.dhm.JobParamEditor");
dojo.require("wwwmoa.client.dhm.FileViewer");
dojo.require("wwwmoa.client.dhm.JobStatusViewer");
dojo.require("wwwmoa.client.dhm.NavPanel");

dojo.addOnLoad(function() {
	dojo.declare("wwwmoa.client.Client", dijit._Widget, {

		uiComp : {},
		uiCompDHM : [],
		_isCurrentlyModal : false,

		startup : function() {
		    if(this.uiComp.parent==null)
			return;

		    this.uiComp.parent.startup();
		    
		},

		// Builds the client out of other widgets.
		buildRendering : function() {
		    // create main structure
		    this.uiComp.parent=new dijit.layout.BorderContainer({style : "width:100%; height:700px", gutters : "true", liveSplitters: true});

		    this.domNode=dojo.create("div", null);
		    this.domNode.appendChild(this.uiComp.parent.domNode);




		    // create nav bar
		    this.uiComp.nav=new dijit.layout.ContentPane({region : "top", splitter : false, style : "height:40px"});

		    this.uiComp.parent.addChild(this.uiComp.nav);

		    this.uiComp.navpanel=new wwwmoa.client.dhm.NavPanel({style : {display : "inline"}});
		    this.uiCompDHM.push(this.uiComp.navpanel);

		    this.uiComp.nav.containerNode.appendChild(this.uiComp.navpanel.domNode);

		    this.uiComp.nav.containerNode.appendChild(dojo.create("span", {innerHTML : " | "}));

		    this.uiComp.navbreadcrumb=dojo.create("span", {style : {marginRight : "20px"}});

		    this.uiComp.nav.containerNode.appendChild(this.uiComp.navbreadcrumb);




		    // create fs browser
		    this.uiComp.fsbrowserpane=new dijit.layout.ContentPane({region : "leading", style : "width:300px", splitter : true});

		    this.uiComp.parent.addChild(this.uiComp.fsbrowserpane);

		    this.uiComp.fsbrowser=new wwwmoa.client.dhm.FSBrowser({style : "padding:6px"});
		    this.uiCompDHM.push(this.uiComp.fsbrowser);

		    dojo.place(this.uiComp.fsbrowser.domNode, this.uiComp.fsbrowserpane.domNode);




		    // create tab structure
		    this.uiComp.tab=new dijit.layout.TabContainer({region : "center", splitter : true});

		    this.uiComp.parent.addChild(this.uiComp.tab);




		    // create job status viewer
		    this.uiComp.jobstatusviewerpane=new dijit.layout.ContentPane({title : "Job Status",
										  region : "leading"
			});

		    this.uiComp.tab.addChild(this.uiComp.jobstatusviewerpane);

		    this.uiComp.jobstatusviewer=new wwwmoa.client.dhm.JobStatusViewer({});
		    this.uiCompDHM.push(this.uiComp.jobstatusviewer);

		    dojo.place(this.uiComp.jobstatusviewer.domNode, this.uiComp.jobstatusviewerpane.domNode);




		    // create job view
		    this.uiComp.pbrowserpane=new dijit.layout.ContentPane({title : "Job View", region : "leading", style : "width:300px", splitter : true});

		    this.uiComp.tab.addChild(this.uiComp.pbrowserpane);

		    this.uiComp.pbrowser=new wwwmoa.client.dhm.PBrowser({});
		    this.uiCompDHM.push(this.uiComp.pbrowser);

		    dojo.place(this.uiComp.pbrowser.domNode, this.uiComp.pbrowserpane.domNode);




		    // create job parameter editor
		    this.uiComp.jobparameditorpane=new dijit.layout.ContentPane({title : "Job Parameters", region : "leading", style : "width:300px", splitter : true});

		    this.uiComp.tab.addChild(this.uiComp.jobparameditorpane);

		    this.uiComp.jobparameditor=new wwwmoa.client.dhm.JobParamEditor({});

		    this.uiCompDHM.push(this.uiComp.jobparameditor);

		    dojo.place(this.uiComp.jobparameditor.domNode, this.uiComp.jobparameditorpane.domNode);




		    // create notices
		    this.uiComp.bottom=new dijit.layout.ContentPane({region : "bottom", splitter : false, id : "smallnotices", content : "This is the pre-release version of WWWMoa.<br>WWWMoa is powered by <a href=\"/go/python\">Python</a> and <a href=\"/go/dojo\">Dojo Toolkit</a>. Best viewed in <a href=\"/go/firefox\">Firefox Web Browser</a>."});

		    this.uiComp.parent.addChild(this.uiComp.bottom);




		    // perform some additional init
		    for(var x=0; x<this.uiCompDHM.length; x++) 
			this.uiCompDHM[x].dhmPoint(this);

		    this._toggleExpand();




		    // perform initial navigation
		    this._initNav();
		},

		// Toggles whether the client is in expanded view.
		_toggleExpand : function() {
		    var width, cols, indexCount;

		    var setLabel=dojo.hitch(this, function() {
			    var label=(this._expanded ? "[Normal View]" : "[Expanded View]");

			    this.uiComp.navexpand.innerHTML=label;
			});

		    if(this._expanded==null) {
			this.uiComp.navexpand=dojo.create("span", {onclick : dojo.hitch(this, this._toggleExpand),
								   style : {fontWeight : "bold",
									    color : "#0000FF",
									    cursor : "pointer"
				}});

			this.uiComp.nav.containerNode.appendChild(this.uiComp.navexpand);

			this._expanded=false;

			setLabel();

			return;
		    }

		    this._expanded=!this._expanded;

		    setLabel();

		    if(this._expanded) {
			width=800;
			cols=4;
			indexCount=100;
		    }
		    else {
			width=350;
			cols=1;
			indexCount=15;
		    }

		    this.uiComp.fsbrowserpane.resize({w : width});
		    this.uiComp.parent.resize();
		    this.uiComp.fsbrowser.attr("cols", cols);
		    this.uiComp.fsbrowser.attr("indexCount", indexCount);
		},

		// Starts initial navigation.
		_initNav : function() {
		    this._initNavWD=wwwmoa.io.cookie.get("WWWMOA_WD");

		    this._initNavWD=(this._initNavWD==null ? "" : this._initNavWD);

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("s", this._initNavWD),
				       dojo.hitch(this, this._initNavCallback),
				       3000);
		},

		// Completes initial navigation.
		_initNavCallback : function(data) {
		    if(data==null)
			this._initNavWD="";
		    else {
			var response=wwwmoa.formats.json.parse(data);

			if(response.size!=-1)
			    this._initNavWD="";
		    }

		    this.dhmRequest({
			    type : wwwmoa.dhm.DHM_REQ_WDNAV,
			    args : {path : this._initNavWD}
			});
		},

                dhmRequest : function(request, dhm) {
		    var poll_good;
		    var poll_ret;

		    if(request.type==wwwmoa.dhm.DHM_REQ_WDNAV) {
			if(request.args.path==null)
			    return null;
			
			poll_good=true;

			for(var x=0; x<this.uiCompDHM.length; x++) {
			    poll_ret=this.uiCompDHM[x].dhmPoll({type : wwwmoa.dhm.DHM_PLL_WDNAV, args : { path : request.args.path }});

			    if(poll_ret==null)
				poll_good=false;
			    else
				poll_good=poll_good&&poll_ret;
			}

			if(poll_good) {
			    for(var x=0; x<this.uiCompDHM.length; x++)
				this.uiCompDHM[x].dhmNotify({type : wwwmoa.dhm.DHM_MSG_WDNAV, args : { path : request.args.path }});

			    wwwmoa.io.cookie.set("WWWMOA_WD", request.args.path, true);
			}

			return poll_good;
		    }
		    else if(request.type=wwwmoa.dhm.DHM_REQ_FILEACTION) {
			var container;
			var fileviewer;
			var title;

			if(request.args.path==null)
			    return null;

			fileviewer=new wwwmoa.client.dhm.FileViewer({});

			title=request.args.path;

			if(title.length>24)
			    title="..."+title.substr(title.length-21, 21);

			title=wwwmoa.formats.html.fix_text(title);

			container=new dijit.layout.ContentPane({title : title,
								closable : true,
								onClose : function() {
								    fileviewer.destroy();
								    return true;
								}
			    });

			this.uiComp.tab.addChild(container);
			this.uiComp.tab.selectChild(container);

			dojo.place(fileviewer.domNode, container.domNode);

			fileviewer.attr("location", request.args.path);

			return true;
		    }
		    else {
			return null;
		    }
		},

		dhmNotify : function(message, dhm) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_DATA) {
			if(dhm==this.uiComp.fsbrowser) {
			    if(message.args.key=="locationBreadcrumbNode") {
				dojo.empty(this.uiComp.navbreadcrumb);
				this.uiComp.navbreadcrumb.appendChild(message.args.data);
			    }
			}
		    }
		}		


	    })});





