$(document).ready(function() {
    
    // if jobs are waiting or running, start automatic reload
    if($('h3#waiting').length > 0 || ($('h3#running').length > 0)) {
      setTimeout("location.reload(true);", 10000);
    }

    $("div.delete-features").on('shown', function() {

        $(this).find("button.delete-features").click(function() {
            var featcat_id = $(this).attr("id");
            var postdata = {featcat_id: featcat_id};
            $.post('delete', postdata, function() {
                location.reload();
            });
        });

    });

});

