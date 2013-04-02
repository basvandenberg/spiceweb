// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // fetch (TODO check if needed... only when class selection changes..)
    if(class_ids.length != 2) {
        $("tbody#ttest_table").html('<td colspan="4">Two classes (labels) should be selected.</td>')
    }
    else {
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
