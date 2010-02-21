
dojo.provide("wwwmoa.client.dhm.FileViewer");

dojo.require("wwwmoa.client.dhm._DHM");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.FileViewer", wwwmoa.client.dhm._DHM, {

		_location : "",
		_downloadLocation : null,

		/* Attribute Handlers */
		_setLocationAttr : function(val) {
		    if(this.dhmIsLocked())
			return;

		    this._location=val;
		    this._navToLocation();
		},

		_getLocationAttr : function() {
		    return this._location;
		},

		_setDownloadLocationAttr : function(val) {
		    this._downloadLocation=val;
		},

		_getDownloadLocationAttr : function() {
		    return this._downloadLocation;
		},

		// Loads information about the current location.
		_navToLocation : function() {
		    this._dhmSetVisualByCode("Loading file...");

		    this.dhmLock();

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("s", this.attr("location")),
				       dojo.hitch(this,this._dataLocationCallback),
				       8192);
		},

		// Receives data about what type of file is being loaded. Then,
		// it makes an decision about how to proceed with loading.
		_dataLocationCallback : function(data) {
		    var response;
		    var node;

		    if(data==null) {
			this._dhmSetVisualByCode("An error occured while loading the file.");
			this.dhmUnlock();
			return;
		    }

		    response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data

		    this.attr("downloadLocation", null);

		    if(response["size"]==-1) { // if we are loading a directory
			node=dojo.create("div", {innerHTML : "The file you attempted to load was a directory."});
			this._setPreviewNode(node);

			this.dhmUnlock();
			return;
		    }

		    this.attr("downloadLocation", response["location"]);

		    // at this point, we must be loading a file

		    if(this._isImageType(response["mimetype"])) { // if we have an image
			if(response["size"]>10485760) {
			    this._dhmSetVisualByCode("The image you attempted to load is too large to be shown.");
			    this.dhmUnlock();
			    return;
			}

			node=dojo.create("img", {src : response["location"],
						 alt : this.attr("location")
			                        });

			this._setPreviewNode(this.attr("location"), node);
			this.dhmUnlock();
			return;
		    }

		    this._dhmSetVisualByCode("Loading preview...");

		    wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("preview?size=4096", this.attr("location")),
				       dojo.hitch(this,this._dataCallback),
				       8192);
		},

                // Receives a preview of the file that is being loaded.
                _dataCallback : function(data) {
		    var response;
		    var node;
		    var contents;

		    if(data==null) {
			this._dhmSetVisualByCode("An error occured while loading a preview of the file.");
			this.dhmUnlock();
			return;
		    }

		    response=wwwmoa.formats.json.parse(data); // attempt a parse of the received data

		    contents=response["contents"];

		    if(contents=="")
			contents="<span style=\"font-style:italic\">File is empty.</span>";
		    else
			contents=wwwmoa.formats.html.translate_text(contents);

		    node=dojo.create("div", {style : {fontFamily : "monospace"},
					     innerHTML : contents
			});

		    this._setPreviewNode(this.attr("location"), node);

		    this.dhmUnlock();
		},

		_isImageType : function(mimetype) {
		    return (mimetype=="image/png")||(mimetype=="image/jpeg")||(mimetype=="image/gif");
		},

		// Sets the display to a preview of a file.
		_setPreviewNode : function(path, contentnode) {
		    var node;

		    node=dojo.create("div", null);

		    node.appendChild(dojo.create("div", {style : {fontWeight : "bold"},
				                         innerHTML : "Preview of "+wwwmoa.formats.html.fix_text(path)+":"
				                        }));

		    node.appendChild(contentnode);

		    if(this.attr("downloadLocation")!=null) {
			node.appendChild(dojo.create("br", null));
			node.appendChild(dojo.create("a", {style : {fontWeight : "bold", color : "#0000FF"},
					                   innerHTML : "Click here to download this file.",
					                   href : this.attr("downloadLocation"),
					                   target : "_blank"
					                  }));
		    }

		    this._dhmSetVisualByNode(node);
		}


	    })});
