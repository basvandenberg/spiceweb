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
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select exactly two features using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">feature filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < 1) {
        $("div#scatter img").replaceWith($('<img>'))
        $("div#class_error").remove()
        $("div#scatter").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select one ore more labels using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">label filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
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
