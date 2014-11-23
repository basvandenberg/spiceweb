$(document).ready(function() {
    
    // if jobs are waiting or running, start automatic reload
    if($('h3#waiting').length > 0 || ($('h3#running').length > 0)) {
      setTimeout("location.reload(true);", 10000);
    }

    $('a.delete-features').on('click', function() {

        $('#delete-features-modal').modal();
        var fid = $(this).attr('id');

        $('button.delete', '#delete-features-modal').off('click').on('click', function() {
            var postdata = {featcat_id: fid};
            $.post('delete', postdata, function() {
                location.reload();
            });
        });
    });
});

