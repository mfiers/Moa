
dojo.provide("wwwmoa.client.dhm._DHM");

dojo.require("dijit._Widget");

dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.dhm._DHM", dijit._Widget, {

		// In the following member definitions, the numbers next to
		// comments means the following:
		//      0: Should not be overridden.
		//      1: Can be overridden, but do not have to be.
		//      2: Should not be overridden, called, or accessed by any
		//         function other than those provided in this file.

		// Various internal variables. (2)
		_dhmLock : 0,
	        _dhmManager : null,
		_dhmCleanOnSetVisual : true,

		// Called by the manager to deliver a message to the DHM. (1)
		dhmNotify : function(message) {
		    return;
		},

		// Called by the manager to ask the DHM a question. (1)
		dhmPoll : function(poll) {
		    return true;
		},

		// Called by the manager to give the DHM a pointer to the manager. (0)
		dhmPoint : function(manager) {
		    this._dhmManager=manager;
		},

	        // Can be called to instruct the DHM to ignore user input. (0)
	        // A subsequent call to dhmUnlock will undo the effect of this call.
	        // An internal count of the number of currently pending lock requests
	        // is kept.  This allows for multiple entities to lock the DHM without
		// interfering with each other.
		dhmLock : function() {
		    this._dhmLock++;

		    if(this._dhmLock==1)
			this._dhmLockVisual();

		    return this._dhmLock;
		},

		// Can be called to instruct the DHM to start accepting user input again. (0)
		// See dhmLock for more details.
		dhmUnlock : function() {
		    if(this._dhmLock<=0)
			this._dhmLock=0;
		    else
			this._dhmLock--;

		    if(this._dhmLock==0)
			this._dhmUnlockVisual();

		    return this._dhmLock;
		},

		// Can be called to find out whether the DHM is currently locked or not. (0)
		// See dhmLock for more details.
	        dhmIsLocked : function() {
		    return this._dhmLock>0;
		},

		// Can be called by the DHM to retrieve a reference to its manager. (0)
		_dhmGetManager : function() {
		    return this._dhmManager;
		},

		// Called automatically whenever the DHM might want to lock aspects of
		// its visual structure to ignore user input.  It is called after the
		// first lock request is lodged. (1)
		_dhmLockVisual : function() {},

		// Called automatically whenever the DHM might want to unlock aspects of
		// its visual structure. It is called after the last lock request is
		// undone. (1)
		_dhmUnlockVisual : function() {},

		// Builds the basic DHM structure. (0)
		buildRendering : function() {
		    this.domNode=dojo.create("div", null);
		    this.containerNode=this.domNode;
		},

		// The following two functions should be called instead of modifying //
		// the domNode property directly.                                    //

		// Can be called to set the DHMs content using a code fragment. (1)
	        _dhmSetVisualByCode : function(code) {
		    var child=dojo.create("div", {innerHTML : code});
		    
		    this._dhmSetVisualByNode(child);
		},

		// Can be called to set the DHMs content using a document node. (1)
		_dhmSetVisualByNode : function(node) {
		    if(this._dhmCleanOnSetVisual)
			this._dhmSafelyDestroyVisual();

		    var children=dojo.query("> *", this.domNode);

		    for(var x=0; x<children.length; x++)
			this.domNode.removeChild(children[x]);
		    
		    this.domNode.appendChild(node);
		},

		// Can be called to keep the widgets in the old contents of the DHM
		// from being destroyed when either of the two previous functions
		// are called.  The default behavior is to destroy the widgets.
		// This default behavior is usually desirable to avoid memory leaks.
		// However, there may be some times that this behavior should be
		// disabled (i.e. whenever you wish to reuse widgets). (0)
		_dhmDisableSetVisualCleaning : function() {
		    this._dhmCleanOnSetVisual=false;
		},

		// Can be called to reverse the effects of calling the previous function. (0)
		// See _dhmDisableSetVisualCleaning for more details.
		_dhmEnableSetVisualCleaning : function() {
		    this._dhmCleanOnSetVisual=true;
		},

		// An internal function that destroys widgets as described in (2)
		// _dhmDisableSetVisualCleaning.
		_dhmSafelyDestroyVisual : function() {
		    var children=this.getChildren();

		    for(var x=0; x<children.length; x++)
			children[x].destroyRecursive();
		}

	    })});
