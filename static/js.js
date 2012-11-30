String.prototype.contains = function(it) { return this.indexOf(it) != -1; };

// Hide the address bar in mobile safari
window.addEventListener("load",function() {
  setTimeout(function(){
    window.scrollTo(0, 1);
  }, 0);
});

// event listeners
$(".workout_name").click(expand_workout);
$(".measurement_name").click(expand_measurement);
$("#workouts form").submit(add_workout);
$(".add_set").click(add_set);
$("#workouts form").click(remove_set);
$("#measurements form").submit(add_measurement);
$("#search input").focus(searchfocus);
$("#search input")[0].addEventListener("blur", searchblur);
$("#search input").keyup(search);
$("#search input").click(search);
$("#edit_goals").click(not_implemented);
$("#add").click(not_implemented);
// $("input[type=tel]").blur(check_for_submit);

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
function expand_workout(){
    $(this).off("click", expand_workout);
    $(this).click(add_workout);
    $(this).parent().addClass("add");
    var top = $(this).parent().position().top;
    var position = $("#iphone")[0].scrollTop + top - 150;
    $("#iphone").animate({scrollTop: position}, 200);
}

// show the workout form for a workout
function expand_measurement(){
    $(this).off("click", expand_measurement);
    $(this).click(add_measurement);
    $(this).parent().addClass("add");
}



// onblur of form element, check to see if it can be submitted
// if so, submit it
function check_for_submit() {
    save_workout($(this).closest("li"));
}


function save_workout(list_item) {
    
    // remove the submission event handler
    // from the title expander,
    // and reattach the expansion event handler
    var title = list_item.children(".item_name");
    title.off("click", add_workout);
    title.click(expand_workout);

    var form = list_item.children("form");
    submit_workout(form);

    return false;
}


// fires when the workout is collapsed or done is pressed
function add_workout() {
    // hide the form
    var list_item = $(this).parent();
    list_item.removeClass("add");

    save_workout(list_item);
}


// submit a workout to the database
function submit_workout(form) {
    // submit the data via post
    $.post('/api/add_workout', form.serialize(), function(data) {
        console.log(data);
        if (data.submitted === true ) {
            $(document.getElementById("wo_saved_notif_div")).slideToggle();
            window.setTimeout(function(){
                $(document.getElementById("wo_saved_notif_div")).slideToggle();
            },1000)
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
    var el = $(this).parent().children(".set:last");
    if (el.length === 0) {
        el = $(this).parent().children("input[type=hidden]:last");
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
                </div>"
    el.after(content);
}

// remove a set
function remove_set(e) {
    var el = $(e.target);
    if( el.hasClass("remove_set") ) {
        el.parent().remove();
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

done_button(false);