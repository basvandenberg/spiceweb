$(document).ready(function() {

    // button to show/hide the filter widget
    $("#filterbar").click(toggle_showhide);

    // obtain name of current project
    var pn = project_name();

    // read filter selection from cookie
    var sl = $.cookie(pn + ".labeling_name");
    var sc = $.cookie(pn + ".class_ids");
    var sf = $.cookie(pn + ".feat_ids");
    if(sc != null) {
        sc = sc.split(',');
    }
    if(sf != null) {
        sf = sf.split(',');
    }

    // init filters
    init_labeling_filter(sl, sc);
    init_feature_filter(sf);

    // button to show/hide feature category
    $(".filter_showcat").click(function() {
        var currentId = $(this).parent().attr('id');

        if(currentId == undefined) {
            $("div#labelfilter").animate({height:'toggle'});
        }
        else {
            $("div." + currentId + ".filter_select").animate({height:'toggle'});
        }
    });

    // hide feature categories by default
    $(".filter_select:gt(0)").animate({height:'toggle'});
});

function project_name() {
    return $("div#project_name>a").text();
}

function update(changed_classes, changed_features) {

    // obtain filter selections
    var sl = selected_labeling();
    var sc = selected_classes();
    var sf = selected_features();

    // update the content on screen accordingly
    updateContent(sl, sc, sf, changed_classes, changed_features);

    // obtain name of current project
    var pn = project_name();

    // store the selection in a cookie
    // TODO get url from settings or var??? now it only works for one link 'depth'
    var cookie_params = {expires: 14, path: '/'}
    $.cookie(pn + ".labeling_name", sl, cookie_params);
    $.cookie(pn + ".class_ids", sc, cookie_params);
    $.cookie(pn + ".feat_ids", sf, cookie_params);
}

function selected_features() {
    var feat_ids = []
    $('ol.feats').each(function(index) {
        var count = 0;
        var featcat_id = $(this).parent().parent().attr('id');
        $(this)
            .children(".ui-selected")
            .map(function(){ 
                feat_ids.push(this.id);
                count = count + 1;
            });
        $('div#' + featcat_id).find('span.numselected').html(' (' + count + ')')
        //$('span.numselected.' + featcat_id).html(' (' + count + ')')
    });
    return feat_ids
}

function selected_classes() {
    var class_ids = $("#labels_selected .class_label div")
        .map(function () {
            return $(this).html();
        });
    result = class_ids.get();
    return result;
}

function selected_labeling() {
    return $("select#labeling_select").val()
}

function init_labeling_filter(labeling_name, class_ids) {

    //update
    function update_classes(l, c) {
        var postdata = {labeling_name: l};
        $.post('class_names', postdata, 
            function(data) {
                $("#labels_selected").replaceWith(data['class_names_selected']);
                $("#labels_unselected").replaceWith(data['class_names_unselected']);
                init_class_filter(c);

                // update content in main window
                update(true, true);
            });
        return false ;

    }

    // select
    if(labeling_name != null) {
        $("select#labeling_select option").each(function() {
            $("select option").filter(function() {
                return $(this).text() == labeling_name; 
            }).attr('selected', true);
        });
    }
    update_classes($("select#labeling_select").val(), class_ids);

    // respond to selecting another labeling (fetch label names from server)
    $("select#labeling_select").on("change", function() {
        update_classes($(this).val(), null);
        update(true, false);
    });

}

function init_feature_filter(feat_ids) {
    
    // select
    if(feat_ids != null) {
        $('ol.feats>li.feat').each(function() {
            var cur_id = $(this).attr('id');
            if(jQuery.inArray(cur_id, feat_ids) > -1) {
                $(this).addClass("ui-selected");
            }
            else {
                $(this).removeClass("ui-selected");
            }
        });
    }

    // update content after feature selection change
    $( ".selectable" ).selectable({
        stop: function() {
            update(false, true);
        }
    });

    // select all features of category
    $(".filter_select_all").click(function() {
        $(this).parent().parent().find("li").addClass("ui-selected");
        update(false, true);
    });
  
    // deselect all features of category
    $(".filter_deselect_all").click(function() {
        $(this).parent().parent().find("li").removeClass("ui-selected");
        update(false, true);
    });
}

function init_class_filter(class_ids) {
  
    // labels and the selection
    var $labels = $( "#labels_unselected" ),
        $labels_select = $( "#labels_selected" );

    // make label item draggable
    $( "li", $labels ).draggable({
        cancel: "a.ui-icon",
        revert: "invalid",
        containment: "document",
        helper: "clone",
        cursor: "move"
    });

    // make label item draggable
    $( "li", $labels_select ).draggable({
        cancel: "a.ui-icon",
        revert: "invalid",
        containment: "document",
        helper: "clone",
        cursor: "move"
    });

    // make selection box droppable
    $labels_select.droppable({
        accept: "#labels_unselected li",
        activeClass: "ui-state_highlight",
        drop: function( event, ui ) {
            selectLabel(ui.draggable, true);
        }
    });

    // make the labels box droppable
    $labels.droppable({
        accept: "#labels_selected li",
        activeClass: "custom-state-active",
        drop: function( event, ui ) {
            deselectLabel(ui.draggable, true);
        }
    });

    // label selection function
    var deselect_icon = "<a href=# class='ui-icon ui-icon-triangle-1-e'>Deselect label</a>";
    function selectLabel($item, upd) {
        var upd = upd;
        $item.fadeOut(0, function() {
            $item.find( "a.ui-icon-triangle-1-w" ).remove();
            $item.append( deselect_icon ).appendTo( $labels_select ).fadeIn(0, function() {
                if(upd) {
                    update(true, false);
                }
            });
        });
    }

    // label deselect function
    var select_icon = "<a href=# class='ui-icon ui-icon-triangle-1-w'>Select label</a>";
    function deselectLabel($item, upd) {
        var upd = upd;
        $item.fadeOut(0, function() {
            $item
                .find( "a.ui-icon-triangle-1-e" )
                .remove()
                .end()
                .css("width", "120px")
                .append( select_icon )
                .appendTo( $labels )
                .fadeIn(0, function(){
                    if(upd) {
                        update(true, false);
                    }
                })
        });
    }

    // icons behavior
    $( "ul.label_list > li" ).click(function( event ) {
        var $item = $( this ),
            $target = $( event.target );
 
        if ( $target.is( "a.ui-icon-triangle-1-w" ) ) {
            selectLabel($item, true);
        } 
        else if ( $target.is( "a.ui-icon-triangle-1-e" ) ) {
            deselectLabel($item, true);
        }
        return false;
    });
    
    // select
    if(class_ids != null) {
        $("#labels_selected li").each(function () {
            cur_id = $(this).children("div").text();
            if(jQuery.inArray(cur_id, class_ids) == -1) {
                deselectLabel($(this), false);
            }
        });
        $("#labels_unselected li").each(function () {
            cur_id = $(this).children("div").text();
            if(jQuery.inArray(cur_id, class_ids) > -1) {
                selectLabel($(this), false);
            }
        });
    }
}

// show/hide the filter widget
function toggle_showhide() {

    var newright = '-300px';
    // TODO get url from settings or var
    var img = "#555753 url(../../img/show.png) top left no-repeat";

    if($('#filterwrapper').css('right') == '-300px'){
        newright = '0px';
        // TODO get url from settings or var
        img = "#555753 url(../../img/hide.png) top left no-repeat";
    }

    $("#filterwrapper").animate({
      right: newright
    }, 200, 
      function() {
        $("#filterwrapper #filterbar").css("background", img);
      });
}
