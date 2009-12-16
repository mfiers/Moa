

if(typeof dojo=="undefined") {
    alert("Some aspects of the current page may not function, as a core library could not be loaded.");
}
else {
    

    if(!dojo.isObject(wwwmoa)) {
	var wwwmoa=new Object();
    };

    wwwmoa.dhm={
	DHM_MSG_WDNAV : 17,
	DHM_MSG_DISPLAY_LOCK : 9,
	DHM_MSG_DISPLAY_UNLOCK : 10,
	DHM_MSG_SHUTDOWN : 2,
        DHM_MSG_DATA : 1,
	DHM_MSG_MODAL_GAIN_CTRL : 5478,
	DHM_MSG_MODAL_LOOSE_CTRL : 5479,

	DHM_REQ_WDNAV : 1,
	DHM_REQ_MODAL : 2,

	DHM_PLL_WDNAV : 1,
	DHM_PLL_SHUTDOWN : 2
    }
}
