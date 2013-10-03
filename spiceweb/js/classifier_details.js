var refreshIntervalId;

$(document).ready(function() { 

    update_progress();
    refreshIntervalId = setInterval('update_progress()', 3000);

    // bind ajax download call to Download button
    $('a.btn.download').bind('click', function(event) {
        var url = get_url_root() + '/download?cl_id=' + clid_from_url();
        event.preventDefault();
        window.location.href = url;
    });

});

function update_progress() {
    var ta = $("textarea.job_progress");
    var tb = $("textarea.error_txt");
    var cl_id = ta.attr('id');
    var postdata = {cl_id: cl_id};
    $.post(get_url_root() + '/progress', postdata, 
        function(data) {
            var finished = data['finished']
            ta.html(data['progress'])
            ta.scrollTop(ta[0].scrollHeight - ta.height());
            tb.html(data['error'])
            tb.scrollTop(tb[0].scrollHeight - tb.height());
            var error = data['error'].length > 0
            if(finished || error) {
                clearInterval(refreshIntervalId);
            }
        });
        return false;
}

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
