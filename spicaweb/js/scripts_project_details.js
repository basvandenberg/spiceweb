
function get_url_root() {
    var path = window.location;
    var path_orig = path.origin;
    var path_name = path.pathname;
    var path_list = path_name.split('/');
    path_list.pop();
    path_list.pop();
    var root_url = path_orig + path_list.join('/');
    return root_url;
}

$(document).ready(function() {

    $('a.download').bind('click', function(event) {
        var data_type = $(this).parent().attr('class');
        var data_name = $(this).attr('id');
        var url = get_url_root() + '/download?data_type=' + data_type +
                '&data_name=' + data_name;
        event.preventDefault();
        window.location.href=url;
    });

    $('.upload').bind('click', function() {
        
        var data_name = $(this).attr('id')
 
        $( ".dialog#" + data_name ).dialog({
            autoOpen: true,
            height: 200,
            width: 400,
            modal: true,
            buttons: {
                "Upload file": function() {
                    var url = get_url_root() + '/upload';
                    $(".upload#" + data_name).attr('action', url);
                    $(".upload#" + data_name).submit();
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            },
            close: function() {
            }
        });
 
        $( ".upload#" + data_name )
            .click(function() {
                $( ".dialog#" + data_name ).dialog( "open" );
            });

        $( "input#lname" )
            .change(function() {
                var lab_id = $("input#data_name").val();
                $("a.upload.labeling").attr("id", lab_id);
                $("form.upload.labeling").attr("id", lab_id);
            });
    });
});

