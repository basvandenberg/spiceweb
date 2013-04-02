// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {
    // do nothing here, check for correct selection if run button is clicked
}

$(document).ready(function() {

    // cross-validation n input spinner
    $( "#nfold" ).spinner({
        min: 3,
        max: 10,
        step: 1,
    });

    // show suitable options per classifier
    var cl = $("#classifier").val()
    $(".classifier_specific").hide(200)
    $("#" + cl).show('fast')
    $("#classifier").change(function(){
        var cl = $(this).val()
        $(".classifier_specific").hide(200)
        $("#" + cl).show('fast')
    });

    // run button
    $('input[type="submit"]').click(function(event) {
        
        // prevent default click behavior
        event.preventDefault();
        
        // check if more than one labels are selected
        var class_ids = selected_classes();
        if(class_ids.length < 2) {
            alert('More then one label should be selected.');
            return false;
        }
        
        // check if one or more features are selected
        var feat_ids = selected_features();
        if(feat_ids.length < 1) {
            alert('At least one feature should be selected.');
            return false;
        }

        // obtain filter selection
        var labeling =  selected_labeling();
        feat_ids = feat_ids.join(',');
        class_ids = class_ids.join(',');

        // obtain form values
        var fs = $("select#featsel").val();
        var n = $("input#nfold").val();
        var cl = $("select#classifier").val();
        if(cl == "knn") {
            var w = $("select#knn_weights").val();
            cl = cl + "_" + w;
        }
        if(cl == "nr") {
            cl = cl + "_" + $("select#nr_weights").val();
        }
        
        // build url and send
        var u = $(location).attr('href'); 
        var url = u + '?feat_ids=' + feat_ids + '&labeling_name=' + 
              labeling + '&class_ids=' + class_ids + '&featsel=' + fs + 
              '&n_fold_cv=' + n + '&cl_type=' + cl;
        window.location.href=url;
    });
});
