$(document).ready(function() {

    // enable popover info box
    $('.info-button').popover({trigger: "hover", html: "true"});

    // calculate buttons
    $('button[type="submit"]').click(function(event) {

        // remove alerts if they are still displayed
        hide_alerts();

        // prevent default click behavior
        event.preventDefault();
 
        // fetch the featcat id from the form id
        var catid = $(this).parent().attr('id');

        // assuming we only use dropdown to select parameters!!!

        var params = [];

        // fetch parameter values
        $(this).parent().find('select.param').find(':selected').map(
            function() {
                params.push($(this).attr('value'));
            }
        );

        // build url and send
        var u = $(location).attr('href');
        var u_without_get = u.substring(0, u.indexOf('&'));
        var url = u_without_get + '?featcat_id=' + catid;
        if(params.length > 0) {
            url = url + '_' + params.join('-');
        }
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
