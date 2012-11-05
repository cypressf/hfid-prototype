// Hide the address bar in mobile safari
window.addEventListener("load",function() {
  setTimeout(function(){
    window.scrollTo(0, 1);
  }, 0);
});

// event listeners
$(".workout_name").click(expand_workout);
$("#workouts form").submit(add_workout);
$(".add_set").click(add_set);
$("#workouts form").click(remove_set);
$("#measurements_form form").submit(add_measurement);
$("#search input").focus(searchfocus);

function searchfocus(){
    window.scrollTo(0, 1);
    console.log('focus');
}

// show the workout form for a workout
function expand_workout(){
    $(this).parent().addClass("add");
}


// submit the workout to the database
function add_workout() {
    // hide the form
    $(this).parent().removeClass("add");

    // submit the data via post
    var form = $(this).parent().children("form");
    $.post('/api/add_workout', form.serialize(), function(data) {
        console.log(data);
    });

    return false;
}

function add_measurement() {
    console.log("measurement being added....")
    // hide the form
    //$(this).parent().removeClass("add");

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

function search() {

}

$(function() {
    var availableTags = ['Arm Pullover','Chest Fly','Chest Press','Crossover Chest Fly','Decline Chest Fly','Decline Chest Press','Decline Push Up','Incline Chest Fly','Incline Chest Press','Kneeling Single-Arm Chest Fly','Parallel Grip Chest Press','Reverse Grip Chest Press','Reverse Grip Decline Chest Press','Reverse Grip Incline Chest Press','Single Arm Chest Fly','Single Arm Chest Press','Wide Chest Press','Abdominal Crunch','Cable Abdominal Crunch','Cross-body Pull Over Crunch','Incline Sit-Up','Kneeling Torso Twist','Reverse Fly','Shoulder Abduction','Shoulder Shrug','Supine Cross-Body Shoulder ','Forearm Curl','Incline Biceps Curl','Kneeling Biceps Curl','Kneeling Lateral Biceps Curl','Kneeling Reverse Biceps Curl','Lateral Biceps Curl','Preacher Concentration Curl','Preacher Curl','Preacher Reverse Curl','Prone Biceps Curl','Reverse Forearm Curl','Seated Biceps Curl','Seated Concentration Curl','Seated Reverse Biceps Curl','Supine Biceps Curl','Supine Concentration Curl','Supine Reverse Biceps Curl','High Crossover Lat Row','High Lat Row','Kneeling Lat Row','Lat Fly','Lat Pull-Down','Lat Row','Low Back Extension','Low Crossover Lat Row','Parallel Grip Kneeling Lat Row','Parallel Grip Lat Pull-Down','Parallel Grip Lat Row','Pull Up','Reverse Grip Kneeling Lat Row','Reverse Grip Lat Pull-Down','Reverse Grip Lat Row','Reverse Grip Pull Up','Single Arm Lat Row','Single Arm Pull Up','Surfer Lat Pull','Buns-Up Leg Press','Calf Raise','Cardio Pull','Decline Lunge','Hamstring Curl','Hip Abduction','Hip Adduction','Hip Extension','Incline Lunge','Lateral Lunge','Leg Extension','Leg Thrust','Lying Hip Adduction','Plyometric Split Squat','Plyometric Squat','Rowing Machine','Single Leg Calf Raise','Single Leg Side Squat','Skiing','Split Squat','Sprint Squat','Squat','Standing Split Squat','Toes In Squat','Toes Out Squat','Swimmer','Upright Row','Close Grip Chest Press','Kneeling Reverse Triceps Kickback','Kneeling Triceps Kickback','Lateral Triceps Extension','Overhead Triceps Press','Reverse Grip Overhead Triceps','Reverse Grip Triceps Pressdown','Triceps Dip','Triceps Pressdown'];
    $( "#tags" ).autocomplete({
        source: availableTags
    });
});
