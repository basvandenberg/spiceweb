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

});

