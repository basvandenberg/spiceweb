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

    // run button
    $('button[type="submit"]').click(function(event) {
        
        // prevent default click behavior
        event.preventDefault();
        
        // check if more than one labels are selected
        var class_ids = selected_classes();
        if(class_ids.length < 2) {
            // TODO turn this into showing error message on page
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
        var n_fold_cv = $("input#n_fold_cv").val();
        var cl_type = $("select#cl_type").val();
        
        // build url and send
        var u = $(location).attr('href');
        var url = u + '?feat_ids=' + feat_ids + '&labeling_name=' + labeling +
            '&class_ids=' + class_ids + '&n_fold_cv=' + n_fold_cv +
            '&cl_type=' + cl_type;

        window.location.href=url;
    });
});
