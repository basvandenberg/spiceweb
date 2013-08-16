function pad(num) {
    var s = "0" + num;
    return s.substr(s.length - 2);
}

function now_str(){
    var n = new Date(),
    h = n.getFullYear().toString();
    m = pad(n.getMonth());
    s = pad(n.getDate());
    return h+m+s;
}

$(document).ready(function() {

    // set spice session id, if not allready present.
    var sessid_key = 'spice.session';
    var sessid = $.cookie(sessid_key);

    if(sessid == null) {

        sessid = now_str() + '_';

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
