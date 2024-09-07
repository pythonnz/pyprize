const states = Object.freeze({
    CLEARED: 0,
    DRAWN: 1,
});

let state = states.CLEARED;

function draw(){
    $.ajax({
        url: '/next',
        type: 'GET',
        success: function (result) {
          var res = JSON.parse(result);
          $('#winner_name').html(res['name']);
          $('#feedback').text(res['feedback']);
        }
    });
    state = states.DRAWN;
}

function clear(){
    $('#winner_name').html('...');
    state = states.CLEARED;
}

function clear_or_draw(){
    if (state == states.CLEARED) {
        draw();
    } else if (state == states.DRAWN) {
        clear();
    }
}

jQuery(document).ready(function($){
    $(document).on('keydown', function(e) {
        // on spacebar or enter
        if (e.which === 32 || e.which === 13) {
            e.preventDefault();
            clear_or_draw()
        }
    });
});
