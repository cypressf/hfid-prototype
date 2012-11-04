// Hide the address bar in mobile safari
window.addEventListener("load",function() {
  setTimeout(function(){
    window.scrollTo(0, 1);
  }, 0);
});

// event listeners
$(".workout_name").click(expand_workout);
$("form").submit(add_workout);
$(".add_set").click(add_set);
$("#workouts form").click(remove_set);


// show the workout form for a workout
function expand_workout(){
    $(this).parent().addClass("add");
}


// submit the workout to the database
function add_workout() {
    console.log("submit");
    // hide the form
    $(this).parent().removeClass("add");

    // submit the data via post
    var form = $(this).parent().children("form");
    $.post('/api/add_workout', form.serialize(), function(data) {
        console.log(data);
    });

    return false;
}

// make another set appear in the form
function add_set() {
    var el = $(this).parent().children(".set:last");
    var content = "<div class=\"set\">\
                    <a class=\"remove_set\">-</a>\
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