$(document).ready(function() { 

    update_results(true);
    update_status();

    setInterval('update_status();update_results(false);', 5000);

    $("div#classifier_list").on("click", "button.delete-classifier", function() {
        var cl_id = $(this).attr("id");
        var postdata = {cl_id: cl_id};
        $.post('delete', postdata, function() {
            location.reload();
        });
    });
    
    //$("div.delete-classifier").on('shown', function() {
    //
    //    $(this).find("button.delete-classifier").click(function() {
    //        var cl_id = $(this).attr("id");
    //        var postdata = {cl_id: cl_id};
    //        $.post('delete', postdata, function() {
    //            location.reload();
    //        });
    //    });

    //});

}); 

function select_score() {
    var sel = $("select#score").val();
    $("td.score").hide();
    $("th.score").hide();
    $("td.score#" + sel).show();
    $("th.score#" + sel).show();
}

function update_results(select_also) {
    var postdata = {};

    $.post('result_tables', postdata, 
        function(data) {
            $("div#classifier_results").html(data['result_tables']);
            $("table#classResults").tablesorter();
        });
        return false;

}

function update_status() {
    var postdata = {};
    $.post('status_table', postdata, 
        function(data) {
            $("div#job_status").html(data['status_table']);
        });
        return false;

}
