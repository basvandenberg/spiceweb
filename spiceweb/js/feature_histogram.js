// global settings
var min_num_classes = 1;
var max_num_classes = 7;
var min_num_features = 1;
var max_num_features = Infinity;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length == 0) {
        $("div#feat_error").remove()
        $("ul.histograms").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select one ore more features using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">feature filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < 1) {
        $("div#class_error").remove()
        $("ul.histograms").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select one ore more labels using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">label filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#class_error").remove()
    }

    var count = 0;

    // count number of hist updates, for progress bar
    $("ol.feats li").each(function () {
        var currentId = $(this).attr('id');
        var hist_li = $("li.hist#" + currentId);
        if($(this).hasClass('ui-selected')) {
            if(hist_li.length == 0) {
                count += 1
            }
            else if(changed_classes) {
                count += 1
            }
        }
    });
    var step = 100 / count;

    // add/update/remove histograms based on feature and label selection
    $("ol.feats li").each(function () {
        var currentId = $(this).attr('id');
        var hist_li = $("li.hist#" + currentId);
        if($(this).hasClass('ui-selected')) {
            if(hist_li.length == 0) {
                show_hist(currentId, class_ids);
            }
            else if(changed_classes) {
                $("li.hist#" + currentId).remove();
                show_hist(currentId, class_ids);
            }
        }
        else {
            $("li.hist#" + currentId).hide('fast', function(){ $("li.hist#" + currentId).remove(); });
        }
    });

}

// obtain histogram and show
function show_hist(cid, class_ids) {

    // remove histograms if no class labels are selected
    if(class_ids.length < 1) {

        $("li.hist").hide('fast', function(){$("li.hist").remove();});
        $("li.loadhist").hide('fast', function(){$("li.loadhist").remove();});
    }
    else {

        $('#sortable').append(
            $('<li>').attr(
                {"id": cid, "class": "hist"}
            )
        );

        // construct post data
        var labels_str = class_ids.join(",");
        var labeling = $("select#labeling_select").val()
        //var postdata = {labeling_name: labeling, labels: labels_str};
        
        // append load box to sortable list
        /*$('<img>').attr(
            {'src':'ahistogram?feat_ids=' + cid + 
                                   '&labeling_name=' + labeling + 
                                   '&class_ids=' + labels_str + 
                                   '&figtype=png'}
        ).load(function() {
            
        }).appendTo($("li.hist#" + cid))*/

        url = 'ahistogram?feat_ids=' + cid
                      + '&labeling_name=' + labeling
                      + '&class_ids=' + labels_str;

        $.getJSON(url, function(data) {

            console.log(data);

            var feat_id = data['feature-id'];
            $('#' + feat_id).empty();

            var width = 840;
            var height = 280;

            var margin = 10;

            var num_hists = data['legend'].length;
            var num_bins = data[data['legend'][0]].length;

            var total_bin_width = Math.floor((840 - 2 * margin) / num_bins);
            var margin_between_bins = 3;

            var margin_between_bars = 1;
            if((total_bin_width - (2 * margin_between_bins)) % 2 == 0) {
                margin_between_bars = 2;
            }

            var bar_width = (total_bin_width
                    - (2 * margin_between_bins)
                    - ((num_hists - 1) * margin_between_bars)) / 2;

            var max_count = 0;
            for(var leg_i = 0; leg_i < data['legend'].length; leg_i++) {
                max_count = Math.max(
                        Math.max.apply(null, data[data['legend'][leg_i]]),
                        max_count
                );
            }
            var max_bar_height = height - 2 * margin;
            var y_step = max_bar_height / max_count;

            var svg = d3.select('#' + feat_id)
              .append('svg')
                .attr('width', width)
                .attr('height', height);

            var colors = ['#204a87', '#fce94f'];

            for(var leg_i = 0; leg_i < data['legend'].length; leg_i++) {

                var legend = data['legend'][leg_i];
                var hist_data = data[legend];

                var g = svg.append('g');
                g.selectAll('rect')
                    .data(hist_data)
                  .enter()
                    .append('rect')
                    .attr('stroke', '#2e3436')
                    .attr('stroke-width', 1)
                    .attr('fill', function(d, i) {

                        return colors[leg_i];
                    })
                    .attr('x', function(d, i) {

                        return margin
                                + (i * total_bin_width)
                                + margin_between_bins
                                + leg_i * (bar_width + margin_between_bars);
                    })
                    .attr('y', function(d) {

                        return (height - margin) - d * y_step;
                    })
                    .attr('width', bar_width)
                    .attr('height', function(d) {

                        return d * y_step;
                    });
            }

            svg.append('g')
                .append('text')
                .text(data['title'])
                .attr('x', 10)
                .attr('y', 10);
        });
        
        return false;
    }
}

$(document).ready(function() {

    // make histograms dragable
    //var sortable = $('#sortable');
    //$(sortable).sortable();
    //$(sortable).disableSelection();
});


