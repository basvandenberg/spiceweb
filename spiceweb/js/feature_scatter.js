// global settings
var min_num_classes = 1;
var max_num_classes = 10;

function updateContent(labeling_name, class_ids, feat_ids, changed_classes, changed_features) {

    if(feat_ids.length != 2) {
        $("div#feat_error").remove()
        $("div#scatter").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select exactly two features using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">feature filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
        $('#scatter').empty();
    }
    else {
        $("div#feat_error").remove()
    }

    if(class_ids.length < min_num_classes) {
        $("div#class_error").remove()
        $("div#scatter").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />Select one ore more labels using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">label filter</a> in the right panel. The right panel is closed by default, click on the dark gray box with the arrow to open it.</p></div>'
        );
        $('#scatter').empty();
    }
    else {
        $("div#class_error").remove()
    }

    if(class_ids.length > max_num_classes) {
        $("div#class_error").remove()
        $("div#scatter").before(
            '<div id="feat_error" class="alert alert-info alert-error fade in"><p><strong>Info:</strong><br />It is not possible to show more than 10 labels in one scatter plot. Please select 10 or less labels using the <a href="http://localhost:8080/spice/doc/tutorial1.html#filter-sidebar">label filter</a></p></div>'
        );
        $('#scatter').empty();
    }
    else {
        $("div#class_error").remove()
    }

    if(feat_ids.length == 2 && class_ids.length >= min_num_classes
            && class_ids.length <= max_num_classes) {

        var spinner = $('<img>')
            .attr('src', '../../img/loading1.gif')
            .attr('width', '40px')
            .attr('height', '40px');
        var loading = $('<div></div>')
            .addClass('loading')
            .append(spinner);

        $('#scatter').empty().append(loading);

        url = 'ascatter?feat_ids=' + feat_ids
                      + '&labeling_name=' + labeling_name
                      + '&class_ids=' + class_ids;

        $.getJSON(url, function(data) {

            $('#scatter').empty();

            console.log(data);

            var width = 840;
            var height = 840;

            var margin = 20;

            var x_axis_height = 70;
            var y_axis_width = 40;

            var grid_width = width - 2 * margin - y_axis_width;
            var grid_height = height - (2 * margin + x_axis_height);

            var x_grid = data['x-grid'];
            var y_grid = data['y-grid'];

            var max_x = x_grid[x_grid.length - 1];
            var min_x = x_grid[0];
            function x_px(x_val) {

                var perc = (x_val - min_x) / (max_x - min_x);
                var x = perc * grid_width;
                return margin + y_axis_width + x;
            }
            var max_y = y_grid[y_grid.length - 1];
            var min_y = y_grid[0];
            function y_px(y_val) {

                var perc = (y_val - min_y) / (max_y - min_y);
                var y = perc * grid_height;
                return height - (margin + x_axis_height + y);
            }

            // viewport
            var svg = d3.select('#scatter')
              .append('svg')
                .attr('width', width)
                .attr('height', height);

            var y_offset = height - (margin + x_axis_height);
            var x_offset = margin + y_axis_width;

            // y grid lines
            var y_grid_lines = svg.append('g')
                .selectAll('line.y-grid')
                .data(y_grid)
              .enter()
                .append('line')
                .attr('class', 'y-grid')
                .attr('stroke', '#999999')
                .attr('stroke-width', '1px')
                .attr('x1', x_offset)
                .attr('y1', function(d){
                    return y_px(d);
                })
                .attr('x2', width - margin)
                .attr('y2', function(d) {
                    return y_px(d);
                });

            // y grid labels
            var y_grid_labels = svg.append('g')
                .selectAll('text.y-grid')
                .data(y_grid)
              .enter()
                .append('text')
                .attr('class', 'y-grid')
                .attr('font-size', '9pt')
                .style('text-anchor', 'end')
                .text(function(d) {
                    return d.toFixed(3);
                })
                .attr('x', margin + y_axis_width - 4)
                .attr('y', function(d) {
                    return y_px(d) + 4;
                })

            // x grid lines
            var x_grid_lines = svg.append('g')
                .selectAll('line.x-grid')
                .data(x_grid)
              .enter()
                .append('line')
                .attr('class', 'x-grid')
                .attr('stroke', '#999999')
                .attr('stroke-width', '1px')
                .attr('y1', y_offset)
                .attr('x1', function(d){
                    return x_px(d);
                })
                .attr('y2', margin)
                .attr('x2', function(d) {
                    return x_px(d);
                });

            // x grid labels
            var x_grid_labels = svg.append('g')
                .selectAll('text.x-grid')
                .data(x_grid)
              .enter()
                .append('text')
                .attr('class', 'x-grid')
                .attr('font-size', '9pt')
                .style('text-anchor', 'end')
                .text(function(d) {
                    return d.toFixed(3);
                })
                .attr('x', 0)
                .attr('y', 0)
                .attr('transform', function(d) {
                    return 'translate(' + (x_px(d) + 5).toString() + ', ' + (height - margin - x_axis_height + 10).toString() + ') rotate(-65)';
                });

            // x axis label
            var x_axis_label = svg.append('g')
                .append('text')
                .attr('class', 'x-axis-label')
                .text(data['x-label'])
                .style('text-anchor', 'middle')
                .attr('x', (grid_width / 2) + margin + y_axis_width)
                .attr('y', height - (margin + 3))

            var colors = ['#204a87', '#fce94f',
                    '#73d216', '#f57900', '#5c3566', '#c17d11', '#729fcf',
                    '#4e9a06', '#fcaf3e', '#ad7fa8', '#8f5902']

            // scatters
            for(var leg_i = 0; leg_i < data['legend'].length; leg_i++) {

                var legend = data['legend'][leg_i];
                var scatter_data = data[legend];

                var g = svg.append('g');
                g.selectAll('circle')
                    .data(scatter_data)
                  .enter()
                    .append('circle')
                    .attr('stroke', '#2e3436')
                    .attr('stroke-width', 1)
                    .attr('fill', colors[leg_i])
                    .attr('cx', function(d) {

                        return x_px(d[0]);
                    })
                    .attr('cy', function(d) {

                        return y_px(d[1]);
                    })
                    .attr('r', 4);
            }

            // legend
            svg.append('g')
                .selectAll('text.legend')
                .data(data['legend'])
              .enter()
                .append('text')
                .attr('class', 'legend')
                .style('text-anchor', 'end')
                .text(function(d) {
                    return d;
                })
                .attr('x', width - (margin + 27))
                .attr('y', function(d, i) {
                    return margin + 18 + i*20;
                });

            svg.append('g')
                .selectAll('rect.legend')
                .data(data['legend'])
              .enter()
                .append('rect')
                .attr('fill', function(d, i) {
                    return colors[i];
                })
                .attr('width', 13)
                .attr('height', 13)
                .attr('x', width - (margin + 23))
                .attr('y', function(d, i) {
                    return margin + 6 + i*20;
                })
                .attr('stroke', '#2e3436')
                .attr('stroke-width', '1px')

        });

        return false;
    }
}
