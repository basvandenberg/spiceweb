// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length != 2) {
        $("div#scatter img").replaceWith($('<img>'))
        $("div#feat_error").remove()
        $("div#scatter").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select exactly two features using the feature filter in the right panel.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < 1) {
        $("div#scatter img").replaceWith($('<img>'))
        $("div#class_error").remove()
        $("div#scatter").before(
            '<div id="class_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select one or more labels using the label filter in the right panel</p></div>'
        );
    }
    else {
        $("div#class_error").remove()
    }

    if(feat_ids.length == 2 && class_ids.length > 0) {
        $("div#scatter img").replaceWith(
            $('<img>')
                .attr({'src':'ascatter?feat_ids=' + feat_ids + 
                                     '&labeling_name=' + labeling_name + 
                                     '&class_ids=' + class_ids + 
                                     '&figtype=png'})
                .load(function() {
                })
            )
        return false;
    }
}
