$(document).ready(function() 
{
    //Remove the load-in-progress window
    $("#loadInProgress").detach();

    //Remove the header
    var fr = $("table:last > tbody > tr:first").detach();
	$("table:last > tbody > tr:first").detach();
	$("table:last tbody tr td:nth-child(5)").detach();
	//console.log($("table:last > tbody > tr > td:last").detach());
    //And insert it again as a proper thead
    $("table:last").prepend($('<thead></thead>').append(fr));
    //and now pick up the complete table and dump it in the correct div
    $("#fileBrowser").prepend($("table:last").css('width', '95%').detach());

    //add a few triggers 

    $(".moaTemplate")
        .click(
            function() { 
            }
        );
    //Init the menu
    $('#jsddm > li').bind('mouseover', jsddm_open);
	$('#jsddm > li').bind('mouseout',  jsddm_timer);
    document.onclick = jsddm_close;    

    // Turn the file table into a data table
    $("table:first").dataTable(
        {
		    "sPaginationType": "full_numbers",
            "iDisplayLength": 20,
            "sDom": '<fp<"clear">>rt<"bottom"lp<"clear">>'
	    });

    // initialize tabs
    $("#tabs").tabs({
			cookie : { expires : 3 } 
		});
    $(".moaTemplate")
        .click(
            function() { 
                $tabs.tabs('select', '#templateInfoTab');
            }
        );
});
