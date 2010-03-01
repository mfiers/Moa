
dojo.provide("wwwmoa.client.dhm.FSBrowser");

dojo.require("wwwmoa.client.dhm._DHM");

dojo.require("dijit.form.Button");
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.form.DropDownButton");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.form.NumberTextBox");

dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm.FSBrowser", wwwmoa.client.dhm._DHM, {

		_location : "",

	        _filter : "",
		_filterOn : false,

		_creatingItem : false,

		_items : [],
		_parentItems : [],
		_available : 0,

		_cols : 1,
		_startIndex : 0,
		_indexCount : 15,

		_widgets : [],


		/* Attribute Handlers */
		_setLocationAttr : function(val) {
		    this._location=val;
		    this._goToFirstGroup();
		},

		_getLocationAttr : function() {
		    return this._location;
		},

		_setColsAttr : function(val) {
		    this._cols=Math.max(Math.floor(val), 1);
		    this._nav();
		},

		_getColsAttr : function() {
		    return this._cols;
		},

		_setStartIndexAttr : function(val) {
		    this._startIndex=Math.max(Math.floor(val), 0);
		    this._nav();
		},

		_getStartIndexAttr : function() {
		    return this._startIndex;
		},

		_setIndexCountAttr : function(val) {
		    this._indexCount=Math.max(Math.floor(val), 1);
		    this._nav();
		},

		_getIndexCountAttr : function() {
		    return this._indexCount;
		},

		// Loads the content specific to the current parameters.
		_nav : function() {
		    var args="?";

		    if(this._filterOn) {
			args+="filter="+wwwmoa.io.rl.url_encode(this._filter)+"&";
			args+="filter-type=contains&";
		    }

		    args+="start="+(this._startIndex+1)+"&";
		    args+="end="+(this._startIndex+this._indexCount)+"&";

		    this._cancelNav();

		    this.dhmLock();

		    this._navRequest=wwwmoa.io.ajax.get(wwwmoa.io.rl.get_api("ls"+args, this._location),
							dojo.hitch(this, this._navCallback),
							8000);
		},

		// Receives the data requested by _nav.
		_navCallback : function(data) {
		    this.dhmUnlock();

		    if(data==null)
			return;

		    var response=wwwmoa.formats.json.parse(data);

		    this._parentItems=response["dir"];
		    this._items=response["ls"];
		    this._available=response["ls-available"];

		    if(this._available<this._startIndex+1)
			if(this._available!=0) {
			    this._goToLastGroup();
			    return;
			}

		    this._parentItems=[{name : "[Root]", path : ""}].concat(this._parentItems);

		    this._updateDisplay();
		},

		// Cancels the request made by _nav.
		_cancelNav : function() {
		    if(this._navRequest!=null) {
			this._navRequest.cancel();
			this.dhmUnlock();

			return;
		    }

		    this._navRequest=null;
		},

		// Creates the display if it has not been already.
		_initDisplay : function() {
		    var widget, event, event_obj;
		    var create_dropdown, goto_dropdown;

		    if(this._display!=null)
			return;

		    this._display=dojo.create("div", {style : {fontSize : "10pt"}});

		    this._displayMessage=dojo.create("div", {style : {padding : "3px",
								      border : "1px solid #90D090",
								      backgroundColor : "#F0FFF0"
			    }});
		    this._clearMessages();

		    this._displayList=dojo.create("table", null);


		    this._widgets=[];

		    var helper={
			_widgets : this._widgets,
			_display : this._display,

			addCont : function(cont) {
			    this._display.appendChild(cont);
			    this.setCont(cont);
			},

			setCont : function(cont) {
			    this._cont=cont;
			},

			addWidget : function(widget) {
			    this._widgets.push(widget);
			    this._cont.appendChild(widget.domNode);
			},

			addLine : function() {
			    this._cont.appendChild(dojo.create("br", null));
			}
		    };



		    helper.addCont(dojo.create("div", {style : {textAlign : "center"}}));

		    var addListButton=dojo.hitch({obj : this, helper : helper}, function(type, event) {
			var widget=new dijit.form.Button({showLabel : false,
							  iconClass : "moa"+type+"Button",
							  onClick : dojo.hitch(this.obj, event)
			    });

			this.helper.addWidget(widget);
			});

		    addListButton("First", this._goToFirstGroup);
		    addListButton("Prev", this._goToPrevGroup);
		    addListButton("Next", this._goToNextGroup);
		    addListButton("Last", this._goToLastGroup);




		    create_dropdown=new dijit.TooltipDialog({});
		    goto_dropdown=new dijit.TooltipDialog({});

		    widget=new dijit.form.DropDownButton({showLabel : false,
							  iconClass : "moaAddButton",
							  dropDown : create_dropdown
			});
		    helper.addWidget(widget);

		    widget=new dijit.form.DropDownButton({showLabel : false,
							  iconClass : "moaSearchButton",
							  dropDown : goto_dropdown
			});
		    helper.addWidget(widget);




		    helper.setCont(create_dropdown.containerNode);

		    widget=new dijit.form.TextBox({style : {width : "250px"}});
		    helper.addWidget(widget);
		    helper.addLine();

		    event=function() {
			if(this.textbox.attr("value")=="")
			    return;

			this.obj._createItem(this.textbox.attr("value"), this.isdir);

			this.textbox.attr("value", "");

			dijit.popup.close(this.dropdown);
		    };

		    event_obj={obj : this,
			       textbox : widget,
			       dropdown : create_dropdown,
			       isdir : true
		    };

		    widget=new dijit.form.Button({label : "Create Directory",
						  onClick : dojo.hitch(event_obj, event)
			});
		    helper.addWidget(widget);

		    event_obj={obj : this,
			       textbox : event_obj.textbox,
			       dropdown : create_dropdown,
			       isdir : false
		    };

		    widget=new dijit.form.Button({label : "Create File",
						  onClick : dojo.hitch(event_obj, event)
			});
		    helper.addWidget(widget);





		    helper.setCont(goto_dropdown.containerNode);

		    widget=new dijit.form.NumberTextBox({style : {width : "100px"}});
		    helper.addWidget(widget);

		    widget=new dijit.form.Button({label : "Goto",
						  onClick : dojo.hitch({obj : this,
									textbox : widget,
									dropdown : goto_dropdown
						      }, function() {
							  if(!this.textbox.isValid())
							      return;

							  this.obj._goToGroup(this.textbox.attr("value")-1);

							  this.textbox.attr("value", "");

							  dijit.popup.close(this.dropdown);
						      })});
		    helper.addWidget(widget);
		    helper.addLine();

		    widget=new dijit.form.TextBox({style : {width : "250px"}});
		    helper.addWidget(widget);

		    widget=new dijit.form.Button({label : "Search",
						  onClick : dojo.hitch({obj : this,
									textbox : widget,
									dropdown : goto_dropdown
						      }, function() {
							  if(this.textbox.attr("value")=="")
							      return;

							  this.obj._turnOnFilter(this.textbox.attr("value"));

							  this.textbox.attr("value", "");

							  dijit.popup.close(this.dropdown);
						      })});
		    helper.addWidget(widget);



		    helper.addCont(this._displayMessage);
		    helper.addCont(this._displayList);

		    this._dhmSetVisualByNode(this._display);
		},

		// Updates the display, creating it first if nessesary.
		_updateDisplay : function() {
		    var tr, td, tbody, img, span;
		    var event;
		    var item;
		    var icon_alt, icon_name;

		    this._initDisplay();

		    this._clearMessages();

		    dojo.empty(this._displayList);

		    tbody=dojo.create("tbody", null);

		    this._displayList.appendChild(tbody);

		    if(this._items.length<1)
			this._addEmptyMessage();

		    for(var x=0; x<this._items.length; x++) {
			if(x%this._cols==0) {
			    tr=dojo.create("tr", null);
			    tbody.appendChild(tr);
			}
			
			item=this._items[x];

			if((!item["write-allowed"]) || (!item["read-allowed"]))
			    continue;

			event=dojo.hitch({obj : this, x : x}, function() {
				this.obj._openItem(this.x);
			    });

			td=dojo.create("td", {onclick : event,
					      style : {color : "#0000FF",
						       fontWeight : "bold",
						       cursor : "pointer"
				}});
			tr.appendChild(td);

			if(item.type=="dir") {
			    if(item["x-is-moa"]) {
				icon_name="FSdirclmoaA";
				icon_alt="Moa Job";
			    }
			    else {
				icon_name="FSdirclA";
				icon_alt="Directory";
			    }
			}
			else {
			    icon_name="FSfileA";
			    icon_alt="File";
			}

			img=dojo.create("img", {src : wwwmoa.io.rl.get_image(icon_name),
						alt : icon_alt,
						title : icon_alt,
						style : {verticalAlign : "middle",
							 paddingRight : "3px"
				}});

			td.appendChild(img);

			span=dojo.create("span", {innerHTML : this._fixItemTitle(item.name),
						  style : {textDecoration : "underline"},
						  title : item.name
			    });
			td.appendChild(span);




			td=dojo.create("td", null);
			tr.appendChild(td);

			event=dojo.hitch({obj : this, x : x}, function() {
				this.obj._deleteItem(this.x);
			    });

			img=dojo.create("img", {src : wwwmoa.io.rl.get_image("FSdeleteA"),
						onclick : event,
						alt : "Delete",
						title : "Delete",
						style : {verticalAlign : "middle",
							 paddingLeft : "3px",
							 paddingRight : "3px",
							 cursor : "pointer"
				}});

			td.appendChild(img);
		    }

		    this._sendBreadcrumb();
		    this._addIndexMessage();
		    this._addFilterMessage();
		},

		// Helper function that prepares an item title.
		_fixItemTitle : function(title) {
		    var title_fixed, title_max=24;

		    if(title.length>title_max)
			title_fixed=title.substr(0, title_max-3)+"...";
		    else
			title_fixed=title;

		    return wwwmoa.formats.html.fix_text(title_fixed);
		},

		/* Message Handlers */
		_addEmptyMessage : function() {
		    this._addSimpleMessage("No items were found.");
		},

		_addIndexMessage : function() {
		    if(this._available<=this._items.length)
			return;

		    var message="You are currently viewing "+(this._startIndex+1)+" to ";
		    message+=(this._startIndex+this._items.length) + " out of "+this._available+".";

		    this._addSimpleMessage(message);
		},

		_addFilterMessage : function() {
		    if(!this._filterOn)
			return;

		    var node=dojo.create("div", null);

		    var message="You are currently viewing the results of a filename search for \"";
		    message+=wwwmoa.formats.html.fix_text(this._filter);
		    message+="\".";

		    node.appendChild(dojo.create("div", {innerHTML : message}));

		    message="Click here to view all the contents of the directory.";

		    node.appendChild(dojo.create("span", {innerHTML : message,
				                          onclick : dojo.hitch(this, this._turnOffFilter),
				                          style : {color : "#0000FF",
					                           fontWeight : "bold",
					                           cursor : "pointer"
					}}));

		    this._addMessage(node);
		},

		_addCreateItemFailureMessage : function(text) {
		    var message="The item could not be created";

		    if(text!=null)
			message+=" for the following reason:\n\n"+text;
		    else
			message+=".";

		    this._addSimpleMessage(message, "Item Could Not Be Created");
		},

		_addSimpleMessage : function(text, title) {
		    var node=dojo.create("div", {innerHTML : wwwmoa.formats.html.translate_text(text)});

		    this._addMessage(node, title);
		},

		_addMessage : function(node, title) {
		    var main=dojo.create("div", {style : {padding : "2px",
							  marginBottom : "5px",
							  borderBottom : "1px solid #D0F0E0"
			    }});

		    this._initDisplay();

		    if(title!=null) {
			var title_node=dojo.create("div", {innerHTML : wwwmoa.formats.html.fix_text(title)+" ",
							   style : {fontWeight : "bold"}
			    });

			title_node.appendChild(dojo.create("span", {innerHTML : "[Close Message]",
					                            style : {fontWeight : "bold",
					                                     cursor : "pointer",
					                                     fontSize : "12px",
					                                     color : "#0000FF",
					                                     textDecoration : "underline"
					                                     },
					                            onclick : dojo.hitch(main, function() { dojo.destroy(this); })
					}));

			main.appendChild(title_node);
		    }

		    main.appendChild(node);

		    this._displayMessage.appendChild(main);

		    this._displayMessage.style.visibility="visible";
		},

		_clearMessages : function() {
		    this._initDisplay();

		    dojo.empty(this._displayMessage);

		    this._displayMessage.style.visibility="hidden";
		},

		// Creates a node containing the navigation breadcrumbs,
		// and sends it to DHM manager.
		_sendBreadcrumb : function() {
		    var main=dojo.create("span", {style : {fontWeight : "bold"}});
		    var span, span_event;
		    var img, icon_path;
		    var item;

		    for(var x=0; x<this._parentItems.length; x++) {
			item=this._parentItems[x];

			if(x!=0) {
			    span=dojo.create("span", {innerHTML : " / "});
			    main.appendChild(span);
			    icon_path=wwwmoa.io.rl.get_image("FSdiropA");
			}
			else
			    icon_path=wwwmoa.io.rl.get_image("FSdiroprtA");

			img=dojo.create("img", {src : icon_path,
						alt : "",
						style : {verticalAlign : "middle",
							 paddingRight : "3px"
				}});
			main.appendChild(img);

			span_event=dojo.hitch({obj : this, x : x}, function() {
				this.obj._openParentItem(this.x);
			    });

			span=dojo.create("span", {innerHTML : wwwmoa.formats.html.fix_text(item.name),
						  onclick : span_event,
						  style : {color : "#0000FF",
							   cursor : "pointer"
				}});
			main.appendChild(span);

		    }

		    this._dhmGetManager().dhmNotify({type : wwwmoa.dhm.DHM_MSG_DATA,
				                     args : {key : "locationBreadcrumbNode",
				                             data : main
				    }}, this);
		},

		// Inspects an item, and "opens" it.
		_openItem : function(index) {
		    var item=this._items[index];

		    if(item==null)
			return;

		    if(item.type=="dir")
			this._changeWD(item.path);
		    else
			this._openFile(item.path);
		},

		// "Opens" a parent directory.
		_openParentItem : function(index) {
		    var item=this._parentItems[index];

		    if(item==null)
			return;

		    this._changeWD(item.path);
		},

		// Attempts to change the WD.
		_changeWD : function(path) {
		    this._dhmGetManager().dhmRequest({type : wwwmoa.dhm.DHM_REQ_WDNAV,
				                      args : {path : path}
			});
		},

		// Attempts to "open" a file.
		_openFile : function(path) {
		    this._dhmGetManager().dhmRequest({type : wwwmoa.dhm.DHM_REQ_FILEACTION,
				                      args : {path : path}
			});
		},

		// Deletes an item and removes it from the display.
		_deleteItem : function(index) {
		    var item=this._items[index];

		    if(item==null)
			return;

		    var message="Are you sure you want to delete \""+item.name+"\" (\""+item.path+"\")?";

		    if(item.type=="dir")
			message+="\n\nDeleting \""+item.name+"\" will delete all of its contents as well.";

		    if(!confirm(message))
			return;

		    wwwmoa.io.ajax.del(wwwmoa.io.rl.get_api("s", item.path), null, 8000);

		    this._items.splice(index, 1);

		    this._available--;

		    if(this._items.length<1)
			this._goToFirstGroup();
		    else
			this._updateDisplay();
		},

		// Creates an item and refreshes the display.
		_createItem : function(name, isdir) {
		    var args="?";
		    if(isdir) args+="directory=1&";
		    args+="name="+wwwmoa.io.rl.url_encode(name);

		    if(this._creatingItem)
			return;

		    this._creatingItem=true;

		    wwwmoa.io.ajax.post(wwwmoa.io.rl.get_api("s"+args, this._location),
					dojo.hitch(this, this._createItemCallback),
					8000);
		},

		// Callback function used for _createItem.
		_createItemCallback : function(data) {
		    this._creatingItem=false;

		    if(data==null) {
			this._addCreateItemFailureMessage();
			return;
		    }

		    var response=wwwmoa.formats.json.parse(data);

		    if(!response["success"]) {
			this._addCreateItemFailureMessage(response["x-message"]);
			return;
		    }

		    this._nav();
		},

		/* Filter Action Handlers */
		_turnOnFilter : function(filter) {
		    this._filter=filter;
		    this._filterOn=true;
		    this._goToFirstGroup();
		},

		_turnOffFilter : function() {
		    this._filterOn=false;
		    this._goToFirstGroup();
		},

		/* Group Navigation Handlers */
		_goToFirstGroup : function() {
		    this.attr("startIndex", 0);
		},

		_goToLastGroup : function() {
		    this.attr("startIndex", this._getLastGroupStartIndex());
		},

		_goToNextGroup : function() {
		    this.attr("startIndex", Math.min(this._getLastGroupStartIndex(),
						     this._startIndex+this._indexCount));
		},

		_goToPrevGroup : function() {
		    this.attr("startIndex", Math.max(0, this._startIndex-this._indexCount));
		},

		_goToGroup : function(index) {
		    this.attr("startIndex", Math.min(this._getLastGroupStartIndex(),
						     this._indexCount*Math.max(0, index)));
		},

		_getLastGroupStartIndex : function() {
		    return (Math.ceil(this._available/this._indexCount)-1)*this._indexCount;
		},

		/* DHM Handlers */
		dhmNotify : function(message) {
		    if(message.type==wwwmoa.dhm.DHM_MSG_WDNAV)
			this.attr("location", message.args.path);
		},

		_dhmLockVisual : function() {
		    for(var x=0; x<this._widgets.length; x++)
			this._widgets[x].attr("disabled", true);
		},

		_dhmUnlockVisual : function() {
		    for(var x=0; x<this._widgets.length; x++)
			this._widgets[x].attr("disabled", false);
		}

	    })});
