root_url = 'http://localhost:8080/spica/app/projects/'

// call server side download function to obtain this data file.
$(document).ready(function() {
  $('a.download').bind('click', function(event) {
    var data_type = $(this).parent().attr('class');
    var data_name = $(this).attr('id');
    var url = root_url + 'download?data_type=' + data_type + '&data_name='
            + data_name;
    event.preventDefault();
    window.location.href=url;
  });
});

$(document).ready(function() {
    $('a.upload').bind('click', function() {
        
        var data_name = $(this).attr('id')
 
        $( ".dialog#" + data_name ).dialog({
            autoOpen: true,
            height: 200,
            width: 400,
            modal: true,
            buttons: {
                "Upload file": function() {
                    $(".upload#" + data_name).submit()
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

