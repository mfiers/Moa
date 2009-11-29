/// WWWMoa ///////////////////////////////
/// wwwmoaui.js / UI Addon

if(typeof wwwmoa == "undefined")
{
    alert("Some aspects of this page will not function, because a core JavaScript library could not be found.");
}
else
{
    wwwmoa.ui={
	alert : function(msg)
        {
            alert(msg);
        },

	nms : {
	    _offset : 0,
	    _divs : [],
	    add : function(title, msg, timeout)
	    {
		var a=this;
		var div=document.createElement("div");
		div.style.width="30%";
		div.style.border="1px solid #000000";
		div.style.padding="2px";
		div.style.margin="0px";
		div.style.backgroundColor="#FFFFE0";
		div.style.position="fixed";

		div.style.top=this._offset+"px";
		
		div.innerHTML="<span style=\"font-weight:bold\">"+title+"</span><br>"+msg
		document.body.appendChild(div);
		div.style.left=document.body.clientWidth;
		a._offset+=div.offsetHeight;
		a._divs.push({div : div, offset : a._offset});

		setTimeout(function() { a._offset-=div.offsetHeight; document.body.removeChild(div); a._refresh_positions(); }, timeout);
	    },
	    _refresh_positions : function()
	    {
		
	    }
	}
    }
}