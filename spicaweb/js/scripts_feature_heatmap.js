// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // show loading animation TODO doesn't work...
    // TODO get url from settings
    $("div#heatmap img").replaceWith($('<img>').attr({'id': 'loading','src': '/spica/img/load.gif'}))

    if(class_ids.length < 1 || feat_ids.length < 1) {
        $("div#heatmap img").replaceWith('<img>')
    }
    else {
        var class_str = class_ids.join(","); // use json?
        var feat_ids = feat_ids.join(","); // use json?
        
        $("div#heatmap img").replaceWith(
            $('<img>')
                .attr({'src':'aheatmap?feat_ids=' + feat_ids + 
                                    '&labeling_name=' + labeling_name + 
                                    '&class_ids=' + class_ids + 
                                    '&figtype=png'})
                .load(function() {
                    $("img#loading").remove()
                    $("button#save").remove()
                    $("div#heatmap")
                        .append (
                            $('<button>')
                                .html('svg')
                                .button({icons: {primary: "ui-icon-disk"}})
                                .attr('id', 'save')
                                .bind('click', function() {
                                    url = 'aheatmap?feature_id=' + feat_ids + 
                                                 '&labeling_name=' + labeling + 
                                                 '&labels=' + labels_str + 
                                                 '&figtype=svg';
                                    window.location.href=url;
                                })
                        )
                })
            )
        return false;
    }
}
