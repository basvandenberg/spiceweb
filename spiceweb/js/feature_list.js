$(document).ready(function() {
    
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

