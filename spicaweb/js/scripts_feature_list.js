$(document).ready(function() {

  $('a.calc').bind('click', function(event) {
    $.post('calcfeat', 
           {featvec: $(this).attr('id')}, 
           function() {
               location.reload();
           });
    return false;
  });

  setTimeout("location.reload();", 60000);

    // 
    $("form#upload-custom-features>button").button();
   
    // check form input, before submit
    $("form#upload-custom-features").submit(function(){

        var isFormValid = true;

        var object_ids_f = $("span.fileupload-preview").html();
        if(fasta_file == '') {
            form_alert("create-new-project", "No fasta file selected");
            isFormValid = false;
        }
        if(isFormValid) {
            $("form#create-new-project>button").button('loading');
        }

        return isFormValid;
    });
});

