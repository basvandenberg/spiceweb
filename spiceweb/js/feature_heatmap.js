// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // TODO should also work for one feature...
    if(feat_ids.length < 2) {
        $("div#heatmap img").replaceWith($('<img>'))
        $("div#feat_error").remove()
        $("div#heatmap").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select two or more features using the feature filter in the right panel.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < 1) {
        $("div#heatmap img").replaceWith($('<img>'));
        $("div#class_error").remove();
        $("div#heatmap").before(
            '<div id="class_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select one or more labels using the label filter in the right panel</p></div>'
        );
    }
    else {
        $("div#class_error").remove()
    }

    if(feat_ids.length > 1 && class_ids.length > 0){

        // first remove... this is a HACK, updateContent is requested too often... check this.
        $("div#class_info").remove()
        $("div#heatmap").before(
            '<div id="class_info" class="alert alert-info alert-error fade in"><p><strong>Be patient... </strong>Clustering in progress. Depending on the feature matrix size, this can take a minute or two.</p></div>'
        );

        var check_data = {labeling_name: labeling_name, class_ids: class_ids};
        var msg = "";
        $.post("acheck_heatmap_size", check_data, function(data) {
            msg = data.msg;
            if(msg != "") {
                $("div#heatmap img").replaceWith($('<img>'));
                $("div#class_info").remove();
                $("div#heatmap").before('<div id="class_info" class="alert alert-info fade in"><p><strong>Info: </strong>' + msg + '</p></div>');
            }
            else  {
                $("div#heatmap img").replaceWith($('<img>')
                    .attr({
                        'src':'aheatmap?feat_ids=' + feat_ids + 
                                      '&labeling_name=' + labeling_name + 
                                      '&class_ids=' + class_ids + 
                                      '&figtype=png'
                    })
                    .load(function(data) {
                        $("div#class_info").remove();
                    })
                )
            }
        });

    }
}
