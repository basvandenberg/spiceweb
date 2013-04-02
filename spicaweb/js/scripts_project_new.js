
// hide all errors first
// generate a job id based on time stamp
$(document).ready(function() {

    $("div.error").hide();

    // used to create job id
    var pad = function(num, size) {
        var s = "000" + num;
        return s.substr(s.length-size);
    };

    // create a date object.
    var dt = new Date();

    // get the month, day, and year.
    var month = (dt.getMonth() + 1);
    var day = dt.getDate();
    var year = dt.getFullYear();
    var hour = dt.getHours();
    var min = dt.getMinutes();

    // create job id based on time stamp
    var projectId = pad(year,4) + pad(month,2) + pad(day,2) + '_' +
            pad(hour,2) + pad(min,2)

    // put the project id in the project id input field
    $("input#project_id").val(projectId)
    //changeActionNew(projectId)
    
    // jquery ui toggle button
    //$( "#sequence_type" ).buttonset();

    // check new projectid on change
    $("input#project_id").live("change", function() {
        if(isValidprojectid($(this).val())) {
            correctNewProjectId = true;
            $("div#new_projectid_error").hide();
        }
        else {
            correctNewProjectId = false;
            $("div#new_projectid_error").show();
        }
        //changeActionNew($(this).val());
        // TODO show or hide msg
        //activateSubmitNew();
    });


});

$("input#faste_file").live("change", function() {
    fileFsa = $(this).val();
    //activateSubmitNew();
});

// change feats url based on current projectid
//function changeActionNew(act) {
//    //$(this).attr("value", act);
//    $("form#upload_new").attr("action", "/app/home/" + act + "/project_new");
//};

// check project id
function isValidprojectid(projectid) {
    return /^[0-9a-zA-Z_]+$/.test(projectid);
}

