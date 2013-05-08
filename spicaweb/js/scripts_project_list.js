$(document).ready(function() {

    $("div.delete-project").on('shown', function() {

        $(this).find("button.delete-project").click(function() {
            var pid = $(this).attr("id");
            var postdata = {project_id: pid};
            $.post('delete', postdata, function() {
                location.reload();
            });
        });

    });
});
