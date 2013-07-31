
$(document).ready(function() { 

    // bind ajax download call to Download button
    $('a.btn.download').bind('click', function(event) {
        var url = get_url_root() + '/download?cl_id=' + clid_from_url();
        event.preventDefault();
        window.location.href = url;
    });

    // bind ajax download call to download prediction file links
    $('a.pred-file.download').bind('click', function(event) {
        var data_set = $(this).attr('id');
        var url = get_url_root() + '/download?cl_id=' + clid_from_url() + 
                '&data_set=' + data_set;
        event.preventDefault();
        window.location.href = url;
    });

});

function clid_from_url() {
    var path = window.location;
    var path_orig = path.origin;
    var path_name = path.pathname;
    var path_list = path_name.split('/');
    return path_list.pop();
}

function get_url_root() {
    var path = window.location;
    var path_orig = path.origin;
    var path_name = path.pathname;
    var path_list = path_name.split('/');
    path_list.pop();
    path_list.pop();
    var root_url = path_orig + path_list.join('/');
    return root_url;
}
