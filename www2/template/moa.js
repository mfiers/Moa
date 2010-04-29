function moaSuccess(message) {
   moaMessage(message, '#1DA343');   
   }

function moaError(message) {
   moaMessage(message, '#A31E39');
   }

function moaMessage(message, color) {
   //take over the breadcrumbbar
   var bcb = $('.moaBreadCrumbs');
   var mm = $('.moaMessage');

   var pos = bcb.offset();
   var width = bcb.width();

   //show the menu directly over the placeholder
   mm.css( { 'background-color' : color} );
   mm.html(message);
   mm.fadeIn(100).delay(1500).fadeOut(400);
   }

function moaAjaxCall(method, data) {
    $.ajax({ url: "/moa/api.cgi/" + method,
             dataType: "json",
             data: data,
             success: function(data, status, req){
                 if (data.success) {
                     moaSuccess(data.message);
                 } else {
                     moaError(data.message);
                 }
             },
             error: function(req, status, error){
                 moaError(error);
             }
           });
}

function moaSet(wd, key, val) {
    moaAjaxCall('set', {wd: wd, key: key, val: val});
}
 
function saveEditBox(event) {
   var box = $(this);
   if ( event.data.oldValue !==  box.val()) {
       console.log("storing new val " + box.val());
       event.data.oldElem.html(box.val());
       moaSet("${moacwd}",
              event.data.oldElem.attr('id'),
              box.val());
   }
   //restore the old box
   event.data.oldElem.show();
   box.remove();
   
   }

function editTitle() {
   var mt=$('.moaTitle');
   var val = mt.html().trim()
   mt.after('<input type="text" class="moaEditString" id="title" value="'+val+'" />');
   mt.hide();
   $('.moaEditString')
       .keydown(function(event) {
               if (event.keyCode == 13) {
                   console.debug('lost focus');
                   $(event.target).blur();
               }
           })
       .bind('blur', {oldValue:val, oldElem:mt}, saveEditBox)
       .focus();
}