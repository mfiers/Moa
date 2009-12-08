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

		    dojo.place(this.uiComp.fsbrowser.domNode, this.uiComp.fsbrowserpane.domNode);

		    this.uiComp.tab=new dijit.layout.TabContainer({region : "center", splitter : true});

		    this.uiComp.parent.addChild(this.uiComp.tab);

		    // just a placeholder item for the moment

		    this.uiComp.main=new dijit.layout.ContentPane({title : "Home", style : "padding:6px"});

		    this.uiComp.pbrowser=new wwwmoa.client.dhm.PBrowser({title : "Job View", style : "padding:6px"});

		    this.uiComp.tab.addChild(this.uiComp.pbrowser);
		   
		    this.uiComp.parent.addChild(new dijit.layout.ContentPane({region : "bottom", splitter : false, id : "smallnotices", content : "This is the pre-release version of WWWMoa.<br>WWWMoa is powered by <a href=\"/go/python\">Python</a> and <a href=\"/go/dojo\">Dojo Toolkit</a>. Best viewed in <a href=\"/go/firefox\">Firefox Web Browser</a>."}));


		   
		},

		postCreate : function() {

		    var fsbrowser=this.uiComp.fsbrowser;
		    var pbrowser=this.uiComp.pbrowser;
		    var main=this.uiComp.main;
		    var nav=this.uiComp.nav;

		    dojo.connect(this.uiComp.fsbrowser, "locationChanged", {refresh : function() {

				var buf;
				var isMoa=fsbrowser.attr("locationIsMoa");

				
				buf="You are" + (isMoa ? "" : " not") + " in a Moa directory.";

				main.domNode.innerHTML=buf;

				nav.domNode.innerHTML=fsbrowser.attr("locationBreadcrumbCode");

				if(isMoa)
				    pbrowser.attr("location", fsbrowser.attr("location"));
				else
				    pbrowser.doNoProjectAction();

			    }}, "refresh");
		},

		showAbout : function() {
		    
		    var dialog=new dijit.Dialog({title : "About WWWMoa", content : "<img src=\""+wwwmoa.formats.html.fix_text(wwwmoa.io.rl.get_image("MOAfavA"))+"\" alt=\"\"> WWWMoa 0.1<br><br><a href=\"/about\">Click here</a> to visit the official website for Moa."});
		    this.uiComp.parent.addChild(dialog);

		    dialog.show();
		}
		


	    })});





