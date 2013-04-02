// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // TODO change this...
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

    $('#sortable')
        .append($('<li>').attr({"id": cid, "class": "hist"})
        .append($('<img>').attr({"id": "load_" + cid, 'src': '/spica/img/load.gif'}))) // TODO get url from setting

    var labels = $("#labels_selected .label div").map(function () {
        return $(this).html();
    });
    if(labels.length < 1) {
        // TODO
        $("li.hist").hide('fast', function(){$("li.hist").remove();});
        $("li.loadhist").hide('fast', function(){$("li.loadhist").remove();});
    }
    else {
        var labels_str = labels.get().join(",");
        var labeling = $("select#labeling_select").val()
        var postdata = {labeling_name: labeling, labels: labels_str};
        
        $('<img>')
            .attr({'src':'ahistogram?feat_ids=' + cid + '&labeling_name=' + labeling + '&class_ids=' + labels_str + '&figtype=png'})
            .load(function() {
                $("img#load_" + cid).remove()
                $("li.hist#" + cid)
                    .attr("class", "hist")
                    .append (
                        $('<button>')
                            .button({icons: {primary: "ui-icon-circle-close"},text: false})
                            .attr('id', 'close')
                            .bind('click', function() {
                                $("li.hist#" + cid).hide('fast', function(){ $("#" + cid).remove(); });
                                $("select.feats option#" + cid).attr("selected", false)
                            })
                    )
                    .append (
                        $('<button>')
                            .html('svg')
                            .button({icons: {primary: "ui-icon-disk"}})
                            .attr('id', 'save')
                            .bind('click', function() {
                                url = 'ahistogram?feat_ids=' + cid + '&labeling_name=' + labeling + '&class_ids=' + labels_str + '&figtype=svg';
                                alert(url)
                                window.location.href=url;
                            })
                    )
            })
            .appendTo($("li.hist#" + cid))

        
        return false;
    }
}

$(document).ready(function() {
    // make histograms dragable
    $("#sortable").sortable();
    $("#sortable").disableSelection();
});


