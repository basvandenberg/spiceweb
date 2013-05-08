// global settings
//var min_num_classes = 1;
//var max_num_classes = 7;
//var min_num_features = 1;
//var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length == 0) {
        $("div#feat_error").remove()
        $("table.ttest").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Select one ore more features using the feature filter in the right panel.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length != 2) {
        emptyTable();
        $("div#class_error").remove()
        $("table.ttest").before(
            '<div id="class_error" class="alert alert-info alert-error fade in"><p><strong>Info: </strong>Two class labels should be selected. Use the label filter on the right panel to select two labels</p></div>'
        );
        
    }
    else {
        $("div#class_error").remove()
        if(changed_classes) {
            class_ids = class_ids.join(',')
            var postdata = {labeling_name: labeling_name, class_ids: class_ids};
            $.post('attest', postdata, 
                function(data) {
                    $("tbody#ttest_table").html(data['ttest_table'])
                    $("#sortTable").trigger("update");
                    updateTable();
                });
                return false;
        }
        if(changed_features) {
            updateTable();
        }
    }
}

function emptyTable() {
    $("tbody>tr").hide();
}

function updateTable() {
    $("li.ui-selectee").each(function () {
        var currentId = $(this).attr('id');
        var tr = $("tr#" + currentId);
        if($(this).hasClass("ui-selected")) {
            tr.show();
        }
        else {
            tr.hide();
        }
    });
}
