$(document).ready(function() {

    // enable popover info box
    $('.info-button').popover({trigger: "hover", html: "true"});

    // calculate buttons
    $('button[type="submit"]').click(function(event) {

        // prevent default click behavior
        event.preventDefault();
 
        // fetch the featcat id from the form id
        var catid = $(this).closest('form').attr('id');

        // assuming we only use dropdown to select parameters!!!

        var params = [];

        $(this).closest('form').find('select.param').map(function() {
            params.push($(this).find(':selected').map(function() {
                return $(this).attr('value');
            }).get().join(''))
        });

        // build url and send
        //var u = $(location).attr('href');
        //var u_without_get = u.substring(0, u.indexOf('&'));
        var u_without_get = location.protocol + '//'
                + location.host
                + location.pathname;
        var url = u_without_get + '?featcat_id=' + catid;
        if(params.length > 0) {
            url = url + '_' + params.join('-');
        }

        // remove alerts if they are still displayed
        hide_alerts();

        window.location.href=url;
    });
});

// hide alerts
function hide_alerts() {
    $("div.alert-error").remove()
}

// show alert msg above the submit button of the form with form_id
//function form_alert(form_id, msg) {
//    hide_alerts();
//    $("form#" + form_id + "> :submit").before(
//    '<div class="alert alert-block alert-error fade in"><p>' + msg + '</p></div>'
//    );
//}
