$(document).ready(function() {

    // enable popover info box
    $('.info-button').popover({trigger: "hover", html: "true"});

    // check form input, before submit
    $("form#upload-feature-matrix").submit(function(){

        var isFormValid = true;

        var object_ids_file = $("div.controls#object_ids span.fileupload-preview").html();
        if(object_ids_file == '') {
            form_alert("upload-feature-matrix", "No object ids file selected");
            isFormValid = false;
        }
        var feature_matrix_file = $("div.controls#feature_matrix span.fileupload-preview").html();
        if(object_ids_file == '') {
            form_alert("upload-feature-matrix", "No feature matrix file selected");
            isFormValid = false;
        }
        if(isFormValid) {
            $("form#create-new-project>button").button('loading');
        }

        return isFormValid;
    });
});

// hide alerts
function hide_alerts() {
    $("form > div.alert").remove()
}

// show alert msg above the submit button of the form with form_id
function form_alert(form_id, msg) {
    hide_alerts();
    $("form#" + form_id + "> :submit").before(
    '<div class="alert alert-block alert-error fade in"><p>' + msg + '</p></div>'
    );
}

