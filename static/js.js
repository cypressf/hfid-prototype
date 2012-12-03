String.prototype.contains = function(it) { return this.indexOf(it) != -1; };

// Hide the address bar in mobile safari
window.addEventListener("load",function() {
  setTimeout(function(){
    window.scrollTo(0, 1);
  }, 0);
});

// event listeners
$(".workout_name").click(expand_collapse);
$(".measurement_name").click(expand_measurement);
$("#workouts form").submit(done_clicked);
$(".add_set").click(add_set);
$("#workouts form").click(remove_set);
$("#measurements form").submit(add_measurement);
$("#search input").focus(searchfocus);
$("#search input")[0].addEventListener("blur", searchblur);
$("#search input").keyup(search);
$("#search input").click(search);
$("#edit_goals").click(not_implemented);
$("#add").click(not_implemented);

var checks = false;
var notification = false;

var workout_inputs = $("input[type=tel]");
for (var i = 0; i < workout_inputs.length; i++) {
    console.log(workout_inputs[i]);
    workout_inputs[i].addEventListener("keyup", check_for_submit);
}

function not_implemented(){
    $("#edit_goals").off("click", not_implemented);
    var el = $("#iphone");
    var content = "<p class=\"alert\">\
                    <a href=\"\" id=\"close\"></a>\
                    This is not yet implemented.\
                    </p>"
    el.before(content);
    $("#close").click(close_alert);
    return false;
}

function close_alert() {
    $(this).off("click", close_alert);
    $("#edit_goals").click(not_implemented);
    $(this).parent().remove();
    console.log("removed")
    return false;
}

function search() {
    console.log(this.value);
    filter(this.value);
}


function filter(search_string) {
    search_string = search_string.toLowerCase();

    var workouts = $("#workouts li");
    var j = 0;
    for (var i = 0; i < workouts.length; i ++) {
        var w = workouts[i].id.toLowerCase();
        if ( w.contains(search_string) ) {
            $(workouts[i]).removeClass("hidden");
            j ++;
        }
        else {
           $(workouts[i]).addClass("hidden");
        }
    }

    if (!j) {
        $(".search-error").removeClass("hidden");
    }
    else {
        $(".search-error").addClass("hidden");
    }
}

function searchfocus(){
    window.scrollTo(0, 1);
    $("header").addClass("hidden");
    $(this).parent().addClass("focus");
}

function searchblur(){
    $(this).parent().removeClass("focus");
    $("header").removeClass("hidden");
}


// show the workout form for a workout
function expand_collapse(){
    var li = $(this).parent();
    if (li.hasClass("add")) {
        collapse_and_submit(li);
    }
    else {
        li.addClass("add");
        var sets = li[0].querySelectorAll(".set");
        var last_set = sets[sets.length -1];
        var active_field = last_set.querySelector("input");
        active_field.focus();

        scroll_to_workout(li);
    }

}

function scroll_to_workout(li) {
    var top = li.position().top;
    var position = $("#iphone")[0].scrollTop + top - 150;
    $("#iphone").animate({scrollTop: position}, 200);
}

// show the workout form for a workout
function expand_measurement(){
    $(this).off("click", expand_measurement);
    $(this).click(add_measurement);
    $(this).parent().addClass("add");
}


function check_for_submit(e) {
    var form = $(this).closest("form");
    var set = $(this).closest(".set");
    if (validate(set)) {
        set.removeClass("saved");
        if ( $(".spinner", set).length < 1 ) {
            console.log("yes");
            spinner_on(set[0]);
        };
        submit_workout(form,  {checks:true});
    }
}

function validate(set) {
    var inputs = set[0].querySelectorAll("input");
    var is_valid = true;
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];
        if (isNaN(input.value)) {
            is_valid = false;
            break;
        }
    }
    return is_valid;
}

// fires when workout is submitted via done button
function done_clicked(e) {
    collapse_and_submit($(this).closest("li"));
    // prevent the "done" button from refreshing the page
    return false;
}

// submit a workout, and collapse the form
function collapse_and_submit(li) {
    // hide the form, and submit the data
    li.removeClass("add");
    var form = li.children("form");
    submit_workout(form, {notification:true});
}

function move_to_top(li) {
    // move the li to the top and add the "today" class
    // if it isn't there already
    var active_input = document.activeElement;

    if (!li.hasClass("today")) {
        var ul = li.parent();
        li.detach();

        // if the "today's workouts" and "other workouts"
        // headers are hidden, then show them
        var headers = ul.children(".list-header");
        if (headers.hasClass("hidden")) {
            headers.removeClass("hidden");
        }

        $(headers[0]).after(li);
        li.addClass("today");

        // move the screen so we can see it, 
        // and refocus the input element, so we can
        // keep typing with ease
        scroll_to_workout(li);
        if (active_input){
            active_input.focus();
        }
    }
}


// submit a workout to the database
function submit_workout(form, validation) {
    // submit the data via post
    var data_to_post = form.serialize();
    console.log(data_to_post);
    $.post('/api/add_workout', data_to_post function(data) {
        console.log(data);
        spinner_off(form);
        if (data.submitted === true ) {
            var li = form.closest("li");
            move_to_top(li);
            if(notification && validation.notification) {
                $(document.getElementById("wo_saved_notif_div")).slideToggle();
                window.setTimeout(function(){
                    $(document.getElementById("wo_saved_notif_div")).slideToggle();
                },1000)
            }
            if(checks && validation.checks) {
                $(".set", $(form)).addClass("saved");
            }
        }
    });
}

function add_measurement() {
    console.log("measurement being added....")
    // hide the form
    $(this).parent().removeClass("add");

    // remove the submission event handler
    // from the title expander,
    // and reattach the expansion event handler
    var title = $(this).parent().children(".item_name");
    title.off("click", add_measurement);
    title.click(expand_measurement);

    // submit the data via post
    var form = $(this).parent().children("form");
    $.post('/api/add_measurement', form.serialize(), function(data) {
        console.log(data);
    });

    return false;
}

// make another set appear in the form
function add_set() {
    var last_set = $(this).parent().children(".set:last");
    if (last_set.length === 0) {
        last_set = $(this).parent().children("input[type=hidden]:last");
    }
    var content = "<div class=\"set\">\
                    <a class=\"remove_set\"></a>\
                    <label>\
                        <input type=\"tel\" name=\"reps\">\
                        reps\
                    </label>\
                    <label>\
                        <input type=\"tel\" name=\"weight\">\
                        lbs\
                    </label>\
                </div>";
    last_set.after(content);
    var new_set = last_set.next();
    var input_fields =  new_set.children("label").children("input");
    for (var i = 0; i < input_fields.length; i++) {
        input_fields[i].addEventListener("keyup", check_for_submit);
    }
    input_fields[0].focus();
}

// remove a set
function remove_set(e) {
    var element = $(e.target);
    if( element.hasClass("remove_set") ) {
        var set = element.parent();
        set.remove();
        var form = set.closest("form");
        submit_workout(form, {notification: true});
    }
    // $(this).parent().remove();
}

function done_button(bool){
    if (bool) {
        $(".list").removeClass("no-done");
    }
    else {
        $(".list").addClass('no-done');
    }
}

function set_checks(bool) {
    checks = bool;
}

function set_notification(bool) {
    notification = bool;
}

done_button(false);
set_checks(true);
set_notification(true);

function spinner_off(form) {
    $(".spinner", $(form)).remove();
}

function spinner_on(set){
    var opts = {
      lines: 9, // The number of lines to draw
      length: 4, // The length of each line
      width: 2, // The line thickness
      radius: 4, // The radius of the inner circle
      corners: 1, // Corner roundness (0..1)
      rotate: 0, // The rotation offset
      color: '#000', // #rgb or #rrggbb
      speed: 1, // Rounds per second
      trail: 60, // Afterglow percentage
      shadow: false, // Whether to render a shadow
      hwaccel: false, // Whether to use hardware acceleration
      className: 'spinner', // The CSS class to assign to the spinner
      zIndex: 2e9, // The z-index (defaults to 2000000000)
      top: 0, // Top position relative to parent in px
      left: 265 // Left position relative to parent in px
    };
    var spinner = new Spinner(opts).spin(set);
}