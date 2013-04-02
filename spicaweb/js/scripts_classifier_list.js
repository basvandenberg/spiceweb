$(document).ready(function() { 

    update_results(true);
    update_status();

    setInterval('update_status();update_results(false);', 60000);

    // call the tablesorter plugin TODO does not work
    $("table#classResults").tablesorter({
        
    });

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
            if(select_also) {
                //$("div#score_select").html(data['score_select']);
                //$("select#score").change(function() {
                //    select_score();
                //});
            }
            $("div#classifier_results").html(data['result_tables']);
            $("table#classResults").trigger("update");
            //select_score();
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
