// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length == 0) {
        $("div#feat_error").remove()
        $("ul.histograms").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select one ore more features using the feature filter in the right panel.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < 1) {
        $("div#class_error").remove()
        $("ul.histograms").before(
            '<div id="class_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select one or more labels using the label filter in the right panel</p></div>'
        );
    }
    else {
        $("div#class_error").remove()
    }

    // TODO change this... update? using function parameters?
    $("ol.feats li").each(function () {
        var currentId = $(this).attr('id');
        var hist_li = $("li.hist#" + currentId);
        if($(this).hasClass('ui-selected')) {
            if(hist_li.length == 0) {
                show_hist(currentId);
            }
            else if(changed_classes) {
                $("li.hist#" + currentId).remove();
                show_hist(currentId);
            }
        }
        else {
            $("li.hist#" + currentId).hide('fast', function(){ $("li.hist#" + currentId).remove(); });
        }
    });

}

// obtain histogram and show
function show_hist(cid) {

    // obtain labels selected
    var labels = $("#labels_selected .label div").map(function () {
        return $(this).html();
    });

    // remove histograms if no class labels are selected
    if(labels.length < 1) {
        $("li.hist").hide('fast', function(){$("li.hist").remove();});
        $("li.loadhist").hide('fast', function(){$("li.loadhist").remove();});
    }
    else {

        $('#sortable').append(
            $('<li>').attr(
                {"id": cid, "class": "hist"}
            )
        );

        // construct post data
        var labels_str = labels.get().join(",");
        var labeling = $("select#labeling_select").val()
        var postdata = {labeling_name: labeling, labels: labels_str};
        
        // append load box to sortable list
        $('<img>').attr(
            {'src':'ahistogram?feat_ids=' + cid + 
                                   '&labeling_name=' + labeling + 
                                   '&class_ids=' + labels_str + 
                                   '&figtype=png'}
        ).load(function() {
            
        }).appendTo($("li.hist#" + cid))

        
        return false;
    }
}

$(document).ready(function() {
    // make histograms dragable
    $("#sortable").sortable();
    $("#sortable").disableSelection();
});


