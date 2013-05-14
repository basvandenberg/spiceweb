$(document).ready(function() {

    //$("table#feature").tablesorter();

    // bind feature calculation ajax calls to links
    $('a.calc').bind('click', function(event) {
        $.post('calcfeat', {featvec: $(this).attr('id')}, function() {
            location.reload();
        });
        return false;
    });

    setTimeout("location.reload();", 10000);
});

