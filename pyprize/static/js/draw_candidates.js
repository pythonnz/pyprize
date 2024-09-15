const states = Object.freeze({
    CLEARED: 0,
    DRAWN: 1,
});

const KEYS = {
    LEFT_ARROW: 37,
    RIGHT_ARROW: 39,
    ENTER: 13,
    BACKSPACE: 8,
    SPACE: 32,
};

let state = states.CLEARED;

function draw(){
    $.ajax({
        url: '/next',
        type: 'GET',
        success: function (result) {
            let winner_name = $("#winner_name")
            winner_name.data("candidate", result.candidate.id);
            winner_name.html(result.candidate.name);
            $('#feedback').text(result.feedback);
        }
    });
    state = states.DRAWN;
}

function clear(){
    $('#winner_name').html('...');
    state = states.CLEARED;
}

function award_prize(action){
    let winner_name = $("#winner_name")
    let candidate_id = winner_name.data("candidate")
    $.ajax({
        url: `/candidate/${candidate_id}/award`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            award_prize: action
        }),
        success: function (result) {
            // Do nothing
            // $('#feedback').text(result.feedback);
        }
    })
    clear()
}


jQuery(document).ready(function() {
    $(document).on('keydown', function(e){
        e.preventDefault()

        if (state === states.CLEARED) {
            if ([KEYS.ENTER, KEYS.SPACE].includes(e.which)) {
                draw()
            }
        } else if (state === states.DRAWN) {
            if ([KEYS.LEFT_ARROW, KEYS.BACKSPACE].includes(e.which)) {
                // award_prize(false)
                // Actually nothing needs to be done here
                clear()
            } else if ([KEYS.RIGHT_ARROW, KEYS.ENTER].includes(e.which)) {
                award_prize(true)
            }
        }
    }
)})


// var handleSubmit = function(event) {
//     event.preventDefault();
//     let challengeDiv = $(event.target).closest('.challenge');
//     let challengeNumber = challengeDiv.data("challengenumber");
