/*
$("button.close").live("change", function() {
  $(this).button({
    icons: {
      primary: "ui-icon-locked"
    },
    text: false
  })
});
*/

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

