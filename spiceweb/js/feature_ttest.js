$(document).ready(function() {
    $("table#ttest").tablesorter();
});


function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length == 0) {
        $("div#feat_error").remove()
        $("table.ttest").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select one ore more features using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">feature filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length != 2) {
        emptyTable();
        $("div#class_error").remove()
        $("table.ttest").before(
            '<div id="class_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Two class labels should be selected. Use the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar"> label filter</a> on the right panel to select two labels. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
        
    }
    else {
        $("div#class_error").remove()
        if(changed_classes) {
            class_ids = class_ids.join(',')
            var postdata = {labeling_name: labeling_name, class_ids: class_ids};
            $.post('attest', postdata, 
                function(data) {
                    $("tbody#ttest_table").html(data.ttest_table);
                    updateTable();
                    $("table#ttest").trigger("update");
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
