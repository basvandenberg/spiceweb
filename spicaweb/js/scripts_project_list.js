$(document).ready(function() {
    $("button.delete")
    .button({
        icons: {
            primary: "ui-icon-trash"
        },
        text: false
    })
    .click(function() {
        var pid = $(this).attr("id");
        $( "#dialog-confirm" ).dialog({
            resizable: false,
            height:160,
            modal: true,
            buttons: {
                "Delete project": function() {
                    var postdata = {project_id: pid};
                    $.post('delete', postdata, function() {
                        location.reload();
                    });
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
});
