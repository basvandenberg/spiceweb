var refreshIntervalId;

$(document).ready(function() { 

    update_progress();
    refreshIntervalId = setInterval('update_progress()', 3000);

});

function update_progress() {
    var ta = $("textarea.progress");
    var cl_id = ta.attr('id');
    var postdata = {cl_id: cl_id};
    $.post('progress', postdata, 
        function(data) {
            finished = data['finished']
            ta.html(data['progress'])
            ta.scrollTop(ta[0].scrollHeight - ta.height());
            if(finished) {
                clearInterval(refreshIntervalId);
            }
        });
        return false;
}
