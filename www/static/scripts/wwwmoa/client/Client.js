dojo.provide("wwwmoa.client.Client");
dojo.require("dijit.Dialog");
dojo.require("dijit._Widget");

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.layout.TabContainer");

dojo.require("wwwmoa.client.dhm.FSBrowser");
dojo.require("wwwmoa.client.dhm.PBrowser");

dojo.addOnLoad(function() {
	dojo.declare("wwwmoa.client.Client", dijit._Widget, {

		uiComp : {},
		uiCompDHM : [],

		startup : function() {
		    if(this.uiComp.parent==null)
			return;

		    this.uiComp.parent.startup();
		    
		},

		buildRendering : function() {
		    this.uiComp.parent=new dijit.layout.BorderContainer({style : "width:100%; height:700px", gutters : "true", liveSplitters: true});

		    this.domNode=this.uiComp.parent.domNode;

		    this.uiComp.nav=new dijit.layout.ContentPane({region : "top", splitter : false, style : "height:32px"});

		    this.uiComp.parent.addChild(this.uiComp.nav);

		    this.uiComp.fsbrowserpane=new dijit.layout.ContentPane({region : "leading", style : "width:300px", splitter : true});

		    this.uiComp.parent.addChild(this.uiComp.fsbrowserpane);

		    this.uiComp.fsbrowser=new wwwmoa.client.dhm.FSBrowser({style : "padding:6px"});
		    this.uiCompDHM.push(this.uiComp.fsbrowser);

		    dojo.place(this.uiComp.fsbrowser.domNode, this.uiComp.fsbrowserpane.domNode);

		    this.uiComp.tab=new dijit.layout.TabContainer({region : "center", splitter : true});

		    this.uiComp.parent.addChild(this.uiComp.tab);

		    // just a placeholder item for the moment

		    this.uiComp.main=new dijit.layout.ContentPane({title : "Home", style : "padding:6px"});

		    this.uiComp.pbrowserpane=new dijit.layout.ContentPane({title : "Job View", region : "leading", style : "width:300px", splitter : true});

		    this.uiComp.tab.addChild(this.uiComp.pbrowserpane);

		    this.uiComp.pbrowser=new wwwmoa.client.dhm.PBrowser({});
		    this.uiCompDHM.push(this.uiComp.pbrowser);

		    dojo.place(this.uiComp.pbrowser.domNode, this.uiComp.pbrowserpane.domNode);

		   
		    this.uiComp.parent.addChild(new dijit.layout.ContentPane({region : "bottom", splitter : false, id : "smallnotices", content : "This is the pre-release version of WWWMoa.<br>WWWMoa is powered by <a href=\"/go/python\">Python</a> and <a href=\"/go/dojo\">Dojo Toolkit</a>. Best viewed in <a href=\"/go/firefox\">Firefox Web Browser</a>."}));


		    for(var x=0; x<this.uiCompDHM.length; x++) 
			this.uiCompDHM[x].dhmPoint(this);
		},

	        dhmRequest : function(request) {
		    var poll_good;
		    var poll_ret;

		    if(request.type==wwwmoa.dhm.DHM_REQ_MODAL) {
			return null;
		    }
		    else if(request.type==wwwmoa.dhm.DHM_REQ_WDNAV) {
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

			if(poll_good)
			    for(var x=0; x<this.uiCompDHM.length; x++)
				this.uiCompDHM[x].dhmNotify({type : wwwmoa.dhm.DHM_MSG_WDNAV, args : { path : request.args.path }});

			return poll_good;
		    }
		    else {
			return null;
		    }
		},

		dhmNotify : function(message, dhm) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_DATA) {
			if(dhm==this.uiComp.fsbrowser) {
			    if(message.args.key=="locationBreadcrumbCode")
				this.uiComp.nav.domNode.innerHTML=message.args.data;
			}
		    }
		},

		showAbout : function() {
		    
		    var dialog=new dijit.Dialog({title : "About WWWMoa", content : "<img src=\""+wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("MOAfavA"))+"\" alt=\"\"> WWWMoa 0.1<br><br><a href=\"/about\">Click here</a> to visit the official website for Moa."});
		    this.uiComp.parent.addChild(dialog);

		    dialog.show();
		}
		


	    })});





