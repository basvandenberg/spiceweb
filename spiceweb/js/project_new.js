// generate a job id based on time stamp
$(document).ready(function() {

    // enable popover info box
    $('.info-button').popover({trigger: "hover", html: "true"});

    // used to create job id
    var pad = function(num, size) {
        var s = "000" + num;
        return s.substr(s.length-size);
    };

    // create a date object.
    var dt = new Date();

    // get the month, day, and year.
    var month = (dt.getMonth() + 1);
    var day = dt.getDate();
    var year = dt.getFullYear();
    var hour = dt.getHours();
    var min = dt.getMinutes();

    // create job id based on time stamp
    var projectId = pad(year,4) + pad(month,2) + pad(day,2) + '_' +
            pad(hour,2) + pad(min,2);

    // put the project id in the project id input field
    $("input#project_id").val(projectId);

    // collapsable taxon reference set selection
    $("#taxon_select.collapse").collapse()

    // upon selecing reference set
    $("input[name=use_reference]").on("change", function() {
        $("#taxon_select.collapse").collapse('toggle')
    });

    // update taxon list on changed taxon domain select
    $("select#taxon_domain").on("change", function() {
        fill_taxon_select();
    });
    
    // fil taxon select
    fill_taxon_select();

    // 
    $("form#create-new-project>button").button();
   
    // check form input, before submit
    $("form#create-new-project").submit(function(){


        var isFormValid = true;

        var project_id = $("input#project_id").val();
        if(!isValidprojectid(project_id)) {
            form_alert("create-new-project", "Incorrect project id");
            isFormValid = false;
        }

        var fasta_file = $("span.fileupload-preview").html();
        if(fasta_file == '') {
            form_alert("create-new-project", "No fasta file selected");
            isFormValid = false;
        }
        if(isFormValid) {
            var ref_checked = $("input[name=use_reference ]:checked")
            if(ref_checked.length) {
                form_info("create-new-project", "Please be patient, the data set is being loaded, this can take some time..."
                );   
            }
            $("form#create-new-project>button").button('loading');
        }

        return isFormValid;
    });

    // submit load example project
    $("form#load-example-project").submit(function(e) {
        e.preventDefault();
        var project_index = $("form#load-example-project input:radio[name='project_index']:checked").attr('id');
        var url = get_url_root() + '/load_example/' + project_index;
        window.location.href = url;
    });
});

function get_url_root() {
    var path = window.location.href;
    var path_list = path.split('/');
    path_list.pop();
    var root_url = path_list.join('/');
    return root_url;
}

// hide alerts
function hide_alerts() {
    $("form > div.alert").remove()
}

// show alert msg above the submit button of the form with form_id
function form_alert(form_id, msg) {
    hide_alerts();
    $("form#" + form_id + "> :submit").before(
    '<div class="alert alert-block alert-error fade in"><p>' + msg + '</p></div>'
    );
}

function form_info(form_id, msg) {
    hide_alerts();
    $("form#" + form_id + "> :submit").before(
    '<div class="alert alert-block alert-info fade in"><p>' + msg + '</p></div>'
    );
}

// check project id
function isValidprojectid(projectid) {
    return /^([0-9a-zA-Z_-]){4,30}$/.test(projectid);
}

// fill taxon select list
function fill_taxon_select() {
    // obtain selected taxon domain ancestral number
    var taxon_domain = $('select#taxon_domain').val();
    var targ = get_url_root() + '/taxon_list';
    // obtain all taxons for this domain
    $.post(targ, {taxon_domain:taxon_domain}).done(function(data) {
        $("select#taxon").empty();
        $("select#taxon").html(data.taxon_list);
    });   
}
