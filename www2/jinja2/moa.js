function moaSuccess(message) {
   moaMessage(message, '#1DA343');   
   }

function moaError(message) {
   moaMessage(message, '#A31E39');
   }

function moaMessage(message, color) {
   //take over the breadcrumbbar
   var mm = $('.moaMessage');

   mm.css( { 'background-color' : color} );
   mm.html(message);

   mm.fadeIn(100).delay(1200).fadeOut(400);
   }

function moaUpdateStatus() {
    moaAjaxCall(
        'status',
        { 'wd' : '{{ moacwd }}' },
        function(data) {
            console.log(data);
            $('#moaLogoImage').attr("src", "/moa/html/images/moa_logo_" + data['status'] + ".png")
        }        
    );
}

function moaLock() {
    moaAjaxCall(
        'lock', 
        { 'wd': '{{ moacwd }}' },
        function(data, status, req) {
            moaUpdateStatus();
            moaSuccess("Locked this job");
        } ); }

function moaUnlock() {
    moaAjaxCall(
        'unlock', 
        { 'wd': '{{ moacwd }}' },
        function(data, status, req) {
            moaUpdateStatus();
            moaSuccess("Unlocked this job");
        } ); }

function moaAjaxCall(method, data, onSuccess, onError) {
    if (onSuccess === undefined) {
        onSuccess = function(data, status, req)
        { if (data.success) moaSuccess(data.message);
          else moaError(data.message);
        }; };
    if (onError === undefined) {
        onError = function(req, status, error) { moaError(error); };
    };
    $.ajax({ url: "/moa/cgi/api.cgi/" + method,
             dataType: "json",
             data: data,
             success: onSuccess ,
             error: onError
           });
}

function moaSet(wd, key, val) {
    moaAjaxCall('set', {wd: wd, key: key, val: val});
}
 
function saveEditBox(event) {
   var box = $(this);
   if ( event.data.oldValue !==  box.val()) {
       event.data.oldElem.html(box.val());
       moaSet("{{ moacwd }}",
              event.data.oldElem.attr('id'),
              box.val());
   }
   //restore the old box
   event.data.oldElem.show();
   box.remove();   
   }

function editTitle() {
   var mt=$('.moaTitle');
   var val = $.trim(mt.html());
   mt.after('<input type="text" class="moaEditTitle" id="title" value="'+val+'" />');
   mt.hide();
   $('.moaEditTitle')
       .keydown(function(event) {
               if (event.keyCode == 13) {
                   $(event.target).blur();
               }
           })
       .bind('blur', {oldValue:val, oldElem:mt}, saveEditBox)
       .focus();
}