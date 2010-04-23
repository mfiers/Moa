$(document).ready(function() {
    //Remove the load-in-progress window
    $("#loadInProgress").detach();

    //fix the table - widht 100 percent
    $("table:first").css("width", "100%%");

    //Extract the header & move it to thead
    var fr = $("table:first > tbody > tr:first").detach();

    //Remove the first row (link to parent dir)
    $("table:first > tbody > tr:first").remove();
    $("table:first").prepend("<thead></thead>");
    $("table:first > thead").append(fr);
    
    // remove the 4th column - some sort of a remains of the
    // description?? 
    $("table:first > tbody > tr").each(function(index) {
        $(this).contents().eq(4).remove();
        });

    //Remove the icon links (why again??)
    $("table:first > tbody > tr > td:first-child > a").removeAttr('href');
    $("table:first > tbody > tr > td:nth-child(2) > a:not([href$='/'])").attr('target', '_blank');

    
        /*var t = $(this)
        var icon = t.contents('td:first > a').html();
        t.contents('td:first').html(icon);

        var secondCell = t.contents().eq(2);
        var href= secondCell.contents('a').attr('href');
        console.log(href);
        if (href.charAt(href.length-1) != '/') {
            $(this).attr('target', '_blank');
        }});*/

    //Convert the file info table into a dataTable 
    $("table:first").dataTable({
          "sDom": '<"top"pi>rt<"bottom"fl<"clear">',
          "sPaginationType": "full_numbers",
          "bStateSave": true,
        });

    //Prepare the 
    $(".moaTemplateDescription").jqm({
        overlay: 0, trigger: false,})
    .jqmAddTrigger($(".moaTemplate"))
    .jqmAddClose(".moaTemplateDescription")

    
});
