
dojo.provide("wwwmoa.client.dhm._DHM");

dojo.require("dijit._Widget");

dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm._DHM", dijit._Widget, {

		_dhmLock : 0,
	        _dhmManager : null,
		_dhmCleanOnSetVisual : true,

		dhmNotify : function(message) {
		    return;
		},

		dhmPoll : function(poll) {
		    return true;
		},

		dhmPoint : function(manager) {
		    this._dhmManager=manager;
		},

		dhmLock : function() {
		    this._dhmLock++;

		    if(this._dhmLock==1)
			this._dhmLockVisual();

		    return this._dhmLock;
		},

		dhmUnlock : function() {
		    if(this._dhmLock<=0)
			this._dhmLock=0;
		    else
			this._dhmLock--;

		    if(this._dhmLock==0)
			this._dhmUnlockVisual();

		    return this._dhmLock;
		},

	        dhmIsLocked : function() {
		    return this._dhmLock>0;
		},

		_dhmGetManager : function() {
		    return this._dhmManager;
		},

		_dhmLockVisual : function() {},

		_dhmUnlockVisual : function() {},

		buildRendering : function() {
		    this.domNode=dojo.create("div", null);
		    this.containerNode=this.domNode;
		},

	        _dhmSetVisualByCode : function(code) {
		    var child_elements;

		    if(this._dhmCleanOnSetVisual)
			this._dhmSafelyDestroyVisual();
		    
		    child_elements=dojo.query("> *", this.domNode);

		    for(var x=0; x<child_elements.length; x++)
			this.domNode.removeChild(child_elements[x]);

		    this.domNode.innerHTML=code;
		},

		_dhmSetVisualByNode : function(node) {
		    if(this._dhmCleanOnSetVisual)
			this._dhmSafelyDestroyVisual();
		    
		    this.domNode.appendChild(node);
		},

		_dhmDisableSetVisualCleaning : function() {
		    this._dhmCleanOnSetVisual=false;
		},

		_dhmEnableSetVisualCleaning : function() {
		    this._dhmCleanOnSetVisual=true;
		},

		_dhmSafelyDestroyVisual : function() {
		    var children=this.getChildren();

		    for(var x=0; x<children.length; x++)
			children[x].destroyRecursive();

		    dojo.empty(this.domNode);
		}

	    })});
