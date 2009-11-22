/// WWWMoa ///////////////////////////////
/// wwwmoaui.js / UI Addon
/// Version: 0.1
/// Date: November 20, 2009


if(typeof wwwmoa == "undefined")
{
    alert("Some aspects of this page will not function, because a core JavaScript library could not be found.");
}
else
{
    wwwmoa.ui={
	alert : function(msg) { alert(msg); }
    }
}