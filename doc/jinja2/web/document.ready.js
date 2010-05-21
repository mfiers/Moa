$(document).ready(function() 
{
    //Remove the load-in-progress window
    $("#loadInProgress").detach();

    //Define extra strip function for string
    if(typeof(String.prototype.trim) === "undefined")
    {
        String.prototype.trim = function() 
        {
            return String(this).replace(/^\s+|\s+$/g, '');
        };
    }

    //fix the table - widht 100 percent
    //$("table:first").css("width", "100%%");

    //Remove the header
    var fr = $("table:first > tbody > tr:first").detach();

    //Remove the first row (link to parent dir)
    //$("table:first > tbody > tr:first").remove();
    //$("table:first").prepend("<thead></thead>");
    //$("table:first > thead").append(fr);
    
    // remove the 4th column - some sort of a remains of the
    // description?? 
    //$("table:first > tbody > tr").each(function(index) {
    //    $(this).contents().eq(4).remove();
    //    });

    //Remove the icon links (why again??)
    //$("table:first > tbody > tr > td:first-child > a").removeAttr('href');
    //$("table:first > tbody > tr > td:nth-child(2) > a:not([href$='/'])").attr('target', '_blank');

    
        /*var t = $(this)
        var icon = t.contents('td:first > a').html();
        t.contents('td:first').html(icon);

        var secondCell = t.contents().eq(2);
        var href= secondCell.contents('a').attr('href');
        console.log(href);
        if (href.charAt(href.length-1) != '/') {
            $(this).attr('target', '_blank');
         }});*/

    //filter the table 
    var data = [];
    $("table:first > tbody > tr").not(':first').each(
        function(index) 
        {
            var fca = $(this).contents().eq(1).find('a');  
            o = { 'link' : fca.attr('href'),
                  'txt' : fca.html(),
                  'modified' : $(this).contents().eq(2).html(),
                  'size' : $(this).contents().eq(3).html(), };
            if (o.link[o.link.length-1] === '/') o.isdir = true;
            else o.isdir = false;

            data.push(o);
        });
    
    //remove the table
    $("table:first").remove();
     
    //Convert the file info table into a dataTable 
    // $("table:first").dataTable(
    //     {
    //         "sDom": '<"top"pi>rt<"bottom"fl<"clear">',
    //         "sPaginationType": "full_numbers",
    //         "iDisplayLength" : "5",
    //     });

    //Prepare the popup for template description
    $(".moaTemplateDescription").jqm({
        overlay: 0, trigger: false,})
    .jqmAddTrigger($(".moaTemplate"))
    .jqmAddClose(".moaTemplateDescription");

    //add a few triggers to the message div
    $(".moaMessage")
        .mouseenter(
            function() {$(".moaMessage").hide();});
                      

    //experiment with the file list
    var pgItemsPerPage = 60;
    var pgNoColumns = 4;
    var pgData;

    var fileToIcon = {
        'moa.failed' : 'moa.16.png',
        'moa.mk' : 'moa.16.png',
        'moa.success' : 'moa.16.png',
        'moa.runlock' : 'moa.16.png',
        'Makefile' : 'moa.16.png'
    };

    function paginateCallback(page_index, jq){
        var res = "<table class='moaPgFilelist'><tr>";
        var si = page_index * pgItemsPerPage;
        var max = Math.min((si+pgItemsPerPage, data.length));
        var noRows = Math.ceil(Math.min(data.length, pgItemsPerPage) / pgNoColumns);
        for (var i=0; i<noRows; i++)
        {
            for (var j=0; j<pgNoColumns; j++)
            {
                var q = (page_index * pgItemsPerPage) + (noRows * j) + i;
                if (q >= max) break;
                if ((i > 0) && (j == 0)) res += '</tr><tr>';
				if (j == 0) res += '<td class="moaPgLeft">';                
                else res += '<td class="moaPgNotLeft">';
                if (data[q].isdir) res += '<img class="moaPgIcon" src="/moa/images/folder-16.gif">';
                else 
                {
                    if (fileToIcon.hasOwnProperty(data[q].link)) 
                    {
                        res += '<img class="moaPgIcon" src="/moa/images/';
                        res += fileToIcon[data[q].link];
                        res += '">';
                    } else {
                        res += '<img class="moaPgIcon" src="/moa/images/';
                        res += 'document-lines-16.gif">';

                    }
                }
				var txt = data[q].txt;
				var nwTxt = "<span class='moaPgFilename'>";
				var brC = 0;
				while (txt.length > 0) {
					if (brC > 0) nwTxt += "<span class='moaPgFilename"+brC+"'>";
					nwTxt += txt.substring(0,10);
					if (brC > 0) nwTxt += "</span>";
					if (brC > 6) break;
					brC++;
					txt = txt.substring(10);
				}
				nwTxt += "</span>";
                res += '<a href="' + data[q].link + '"'
                if (! data[q].isdir) res += ' target="_blank" ';
                res +='>';
                res += nwTxt;
				res += '</a><br><span class="moaPgFileInfo">';
                res += data[q].modified;
                if (data[q].size.trim() !== '-') res += ', ' + data[q].size;
                res += '</small></td>';
            }
        }
        res += "</tr></table>";
        $('.paginatedResults').html(res);
    }

    $('.paginatedMenu').pagination(
        data.length,
        {
		    items_per_page: pgItemsPerPage, 
		    callback: paginateCallback
        }
    );
    
//Init the menu
    $('#jsddm > li').bind('mouseover', jsddm_open);
	$('#jsddm > li').bind('mouseout',  jsddm_timer);

    document.onclick = jsddm_close;    
});
