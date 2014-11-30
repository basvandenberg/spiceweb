"use strict";

// global settings
var min_num_classes = 1;
var max_num_classes = 10;
var min_num_features = 2; // TODO should be 1...
var max_num_features = 20;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    // TODO should also work for one feature...
    if(feat_ids.length < min_num_features) {
        $("div#heatmap img").replaceWith($('<img>'))
        $("div#feat_error").remove()
        $("div#heatmap").before(
            '<div id="feat_error" class="alert alert-info"><p><strong>Info:</strong><br />Select ' + min_num_features + ' or more features using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">feature filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < min_num_classes) {
        $("div#heatmap img").replaceWith($('<img>'));
        $("div#class_error").remove();
        $("div#heatmap").before(
            '<div id="feat_error" class="alert alert-info"><p><strong>Info:</strong><br />Select ' + min_num_classes + ' or more labels using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">label filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
    }
    else {
        $("div#class_error").remove()
    }

    if(feat_ids.length >= min_num_features && class_ids.length >= min_num_classes){

        // inform that it can take a while for the heatmap to be shown
        $("div#class_info").remove()
        $("div#heatmap").before(
            '<div id="class_info" class="alert alert-info"><p><strong>Please be patient, </strong>clustering in progress. Depending on the feature matrix size, this can take a minute or two.</p></div>'
        );

        // check if data set size is not to large for generating a heatmap
        var check_data = {labeling_name: labeling_name, class_ids: class_ids};
        var msg = "";
        $.post("acheck_heatmap_size", check_data, function(data) {
            msg = data.msg;
            if(msg != "") {
                $("#heatmap").empty();
                $("div#class_info").remove();
                $("div#heatmap").before('<div id="class_info" class="alert alert-info"><p><strong>Info: </strong>' + msg + '</p></div>');
            }
            else  {

                var spinner = $('<img>')
                    .attr('src', '../../img/loading1.gif')
                    .attr('width', '40px')
                    .attr('height', '40px');
                var loading = $('<div></div>')
                    .addClass('loading')
                    .append(spinner);

                $('#heatmap').empty().append(loading);

                var url = 'aheatmap?feat_ids=' + feat_ids
                              + '&labeling_name=' + labeling_name
                              + '&class_ids=' + class_ids;

                $.getJSON(url, function(data) {

                    $('#class_info').remove();
                    $('#heatmap').empty();

                    console.log(data);

                    var width = 840;

                    var margin = 20;
                    var x_axis_height = 70
                    var y_axis_width = 0

                    var colorbar_width = 50;
                    var labelbar_width = 20;
                    var between_margin = 4;

                    var above_grid = 10 + data['class-names'].length * 20;

                    var grid_width = width - (2 * margin + y_axis_width)
                        - (colorbar_width + labelbar_width + 2 * between_margin);

                    var labelbar_x = margin + y_axis_width + grid_width + between_margin;
                    var colorbar_x = labelbar_x + labelbar_width + between_margin;

                    var colorbar_min = -3.0;
                    var colorbar_max = 3.0;

                    function get_color(value) {

                        var perc, r, g, b;

                        if(value > 0.0) {

                            if(value > colorbar_max) {
                                value = colorbar_max;
                            }
                            perc = value / colorbar_max;

                            r = Math.round(60 + perc * (255 - 60));
                            g = Math.round(135 + perc * (255 - 135));
                            b = Math.round(190 + perc * (255 - 190));
                        }
                        else if(value < 0.0) {

                            if(value < colorbar_min) {
                                value = colorbar_min;
                            } 
                            perc = value / colorbar_min;

                            r = Math.round(60 - perc * 60);
                            g = Math.round(135 - perc * 135);
                            b = Math.round(190 - perc * 190);
                        }
                        else {
                            r = 60;
                            g = 135;
                            b = 190;
                        }
                        return [r, g, b];
                    }

                    var cell_height = 2;
                    var cell_width = grid_width / data['feature-names'].length

                    var grid_height =
                            cell_height * data['object-labels'].length;
                    var height = grid_height + 2 * margin + x_axis_height
                            + above_grid;

                    var y_offset = height - (margin + x_axis_height);
                    var x_offset = margin + y_axis_width;

                    function x_center(index) {
                        return x_offset + cell_width / 2 + index * cell_width;
                    }
                    function x_px(index) {
                        return x_offset + index * cell_width;
                    }
                    function y_px(index) {
                        return y_offset - index * cell_height;
                    }

                    var colors = ['#204a87', '#fce94f',
                        '#73d216', '#f57900', '#5c3566', '#c17d11', '#729fcf',
                        '#4e9a06', '#fcaf3e', '#ad7fa8', '#8f5902']

                    // viewport
                    var svg = d3.select('#heatmap')
                      .append('svg')
                        .attr('width', width)
                        .attr('height', height);

                    // append gradient
                    var gradient = svg
                        .append('linearGradient')
                        .attr('id', 'colorbar-gradient')
                        .attr('x1', 0)
                        .attr('x2', 0)
                        .attr('y1', 0)
                        .attr('y2', 1);
                    gradient.append('stop')
                        .attr('offset', '0%')
                        .attr('stop-color', 'rgb(255,255,255)');
                    gradient.append('stop')
                        .attr('offset', '50%')
                        .attr('stop-color', 'rgb(60,135,190)');
                    gradient.append('stop')
                        .attr('offset', '100%')
                        .attr('stop-color', 'rgb(0,0,0)');

                    // x grid labels
                    var x_grid_labels = svg.append('g')
                        .selectAll('text.x-grid')
                        .data(data['feature-names'])
                      .enter()
                        .append('text')
                        .attr('class', 'x-grid')
                        .attr('font-size', '9pt')
                        .style('text-anchor', 'end')
                        .text(function(d) {
                            return d;
                        })
                        .attr('x', 0)
                        .attr('y', 0)
                        .attr('transform', function(d, i) {
                            return 'translate(' + (x_center(i) + 5).toString() + ', ' + (height - margin - x_axis_height + 10).toString() + ') rotate(-65)';
                        });

                    // heatmap
                    for(var feat_i = 0; feat_i < data['feature-names'].length; feat_i++) {

                        var featname = data['feature-names'][feat_i];
                        var heatmap_data = data[featname];

                        svg.append('g')
                            .selectAll('rect.feature-value')
                            .data(heatmap_data)
                          .enter()
                            .append('rect')
                            .attr('class', 'feature-value')
                            .attr('stroke-width', 0)
                            .attr('fill', function(d) {
                                var c = get_color(d);
                                return 'rgb(' + c[0] + ',' + c[1] + ',' + c[2] + ')';
                            })
                            .attr('x', x_px(feat_i))
                            .attr('y', function(d, i) {
                                return y_px(i);
                            })
                            .attr('width', cell_width)
                            .attr('height', cell_height);
                    }

                    // label bar
                    svg.append('g')
                        .selectAll('rect.object-label')
                        .data(data['object-labels'])
                      .enter()
                        .append('rect')
                        .attr('class', 'object-label')
                        .attr('stroke-width', 0)
                        .attr('fill', function(d) {
                            return colors[d];
                        })
                        .attr('x', labelbar_x)
                        .attr('y', function(d, i) {
                            return y_px(i);
                        })
                        .attr('width', labelbar_width)
                        .attr('height', cell_height);
                        
                    var colorbar_height = 600;
                    // color bar
                    svg.append('g')
                        .append('rect')
                        .attr('class', 'color-bar')
                        .attr('stroke-width', 1)
                        .attr('stroke', '#2e3436')
                        .attr('x', colorbar_x)
                        .attr('y', y_offset - grid_height)
                        .attr('width', colorbar_width - 30)
                        .attr('height', colorbar_height)
                        .attr('fill', "url(#colorbar-gradient)");

                    // color bar y-axis labels
                    var label_axis_data = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0];

                    svg.append('g')
                        .selectAll('text.colorbar-labels')
                        .data(label_axis_data)
                      .enter()
                        .append('text')
                        .attr('class', 'colorbar-labels')
                        .attr('font-size', '9pt')
                        .style('text-anchor', 'end')
                        .text(function(d) {
                            return d;
                        })
                        .attr('x', colorbar_x + 35)
                        .attr('y', function(d, i) {
                            return margin + above_grid + colorbar_height + 4
                                    - i * Math.round(colorbar_height / 6);
                        })

                    // legend
                    svg.append('g')
                        .selectAll('text.legend')
                        .data(data['class-names'])
                      .enter()
                        .append('text')
                        .attr('class', 'legend')
                        .style('text-anchor', 'end')
                        .text(function(d) {
                            return d;
                        })
                        .attr('x', width - (margin + colorbar_width + 23))
                        .attr('y', function(d, i) {
                            return margin + 17 + i*20;
                        });

                    svg.append('g')
                        .selectAll('rect.legend')
                        .data(data['class-names'])
                      .enter()
                        .append('rect')
                        .attr('fill', function(d, i) {
                            return colors[i];
                        })
                        .attr('width', 13)
                        .attr('height', 13)
                        .attr('x', width - (margin + colorbar_width + 20))
                        .attr('y', function(d, i) {
                            return margin + 6 + i*20;
                        })
                        .attr('stroke', '#2e3436')
                        .attr('stroke-width', '1px')
                });
            }
        });
    }
}
