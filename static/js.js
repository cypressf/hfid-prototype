// javascript goes here

function add_workout(sender) {
    outer_div = sender.parentNode;
    workout_name = outer_div.id;
    var workoutNodes = outer_div.childNodes;
    var numSets = 0;
    var reps = [];
    var weights = [];
    var time;
    var length;
    var client_id;
    var workout_type;
    for (var i = 0; i < workoutNodes.length; i++) {
        var this_node = workoutNodes[i]
        if (this_node.name === "client_id") {
            client_id = this_node.value;
        };
        if (this_node.name === "workout_type") {
            workout_type = this_node.value;
        };
        if (this_node.tagName === "DIV" && this_node.id !== workout_name) {
            for (var j = 0; j < this_node.childNodes.length; j++) {
                var numeric_entry = this_node.childNodes[j];
                if (numeric_entry.name === "reps") {
                    reps.push(numeric_entry.value);
                } else if (numeric_entry.name === "weight") {
                    weights.push(numeric_entry.value);
                } else if (numeric_entry.name === "time") {
                    time = numeric_entry.value;
                } else if (numeric_entry.name === "length") {
                    length = numeric_entry.value;
                }
            }
        }
    }
    numSets = reps.length
    post_url = "/api/client/" + client_id + "/add_workout";
    $.post(post_url,{
        workout_name: workout_name,
        workout_type: workout_type,
        reps: reps.toString(),
        sets: numSets,
        weights: weights.toString(),
        workout_time: time,
        workout_length: length
    },
    function () {console.log("post worked!")},
    function() {console.log("post did not work")},
    "json");
    return;
}