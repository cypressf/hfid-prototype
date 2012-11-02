// Hide the address bar in mobile safari
window.addEventListener("load",function() {
  setTimeout(function(){
    window.scrollTo(0, 1);
  }, 0);
});

// attach event listener to clicking workout name
$(".workout_name").click(expand_workout);

function expand_workout(){
    $(this).parent().addClass("add");
}

$("form").submit(add_workout);

function add_workout() {
    console.log("submit");
    $(this).parent().removeClass("add");

    return false;
}

$(".add_set").click(add_set);

// make another set appear in the form
function add_set() {
    el = $(this).parent().children(".set:last");
    content = "<div class=\"set\">\
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

$("#workouts form").click(remove_set);

// remove a set
function remove_set(e) {
    el = $(e.target);
    if( el.hasClass("remove_set") ) {
        el.parent().remove();
    }
    // $(this).parent().remove();
}