$(document).ready(function() {

    // set spice session id, if not allready present.
    var sessid_key = 'spice.session';
    var sessid = $.cookie(sessid_key);
    if(sessid == null) {
        sessid = '';
        var possible = 'abcdefghijklmnopqrstuvwxyz0123456789';
        for(var i=0; i < 40; i++) {
            sessid += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        var cookie_params = {expires: 14, path: '/'};
        $.cookie(sessid_key, sessid, cookie_params);
    }

    // enable popover info box
    $('.info-button').popover({trigger: "hover", html: "true"});
});
