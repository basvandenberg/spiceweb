var refreshIntervalId;

$(document).ready(function() { 

    update_progress();
    refreshIntervalId = setInterval('update_progress()', 3000);

});

function update_progress() {
    var ta = $("textarea.progress");
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
