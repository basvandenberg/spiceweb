$(document).ready(function() {

    $("table#project").tablesorter();

    $('a.delete-project').on('click', function() {

        $('#delete-project-modal').modal();
        var pid = $(this).attr('id');

        $('button.delete', '#delete-project-modal').off('click').on('click', function() {
            var postdata = {project_id: pid};
            $.post('delete', postdata, function() {
                location.reload();
            });
        });
    });
});
