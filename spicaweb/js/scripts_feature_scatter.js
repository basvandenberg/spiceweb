// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // show loading animation 
    // TODO get url from setting
    $("div#scatter img").replaceWith($('<img>').attr({'id': 'loading','src': '/spica/img/load.gif'}))

    if(feat_ids.length != 2) {
        $("div#scatter img").replaceWith('<img>') // TODO print msg
    }
    else if(class_ids.length < 1) {
        $("div#scatter img").replaceWith('<img>') // TODO print msg
    }
    else {
        $("div#scatter img").replaceWith(
            $('<img>')
                .attr({'src':'ascatter?feat_ids=' + feat_ids + 
                                    '&labeling_name=' + labeling_name + 
                                    '&class_ids=' + class_ids + 
                                    '&figtype=png'})
                .load(function() {
                    $("img#loading").remove()
                    $("button#save").remove()
                    $("div#scatter")
                        .append (
                            $('<button>')
                                .html('svg')
                                .button({icons: {primary: "ui-icon-disk"}})
                                .attr('id', 'save')
                                .bind('click', function() {
                                    url = 'ascatter?feature_id=' + feat_ids + 
                                                 '&labeling_name=' + labeling_name + 
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
