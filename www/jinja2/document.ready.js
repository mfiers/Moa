$(document).ready(function() 
{
    //Remove the load-in-progress window
    $("#loadInProgress").detach();

    //find the table with the file informationv
    var ftable=$("th:contains('Last modified')").parent().parent().parent().detach();
    //Remove the header
    var fr = ftable.find("tbody > tr:first").detach();
	ftable.find("tbody > tr:first").detach();
	ftable.find("tbody tr td:nth-child(5)").detach();
    //And insert it again as a proper thead
    ftable.prepend($('<thead></thead>').append(fr));
    //and now pick up the complete table and put it in the correct div
    //ftable.detach();
    $("#fileBrowser").prepend(ftable.css('width', '95%'));

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
    $("#fileBrowser table").dataTable(
         {
	 	    "sPaginationType": "full_numbers",
             "iDisplayLength": 36,
             "sDom": '<fp<"clear">>rt<"bottom"lp<"clear">>'
	     });

    // initialize tabs
    // $("#tabs").tabs();
	$("#tabs").tabs(
        { cookie : { expires : 1 } 
	    });
    $(".moaTemplate")
        .click(
            function() { 
                $tabs.tabs('select', '#templateInfoTab');
            }
        );
});
