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
    $('#next_button').hide();
    $('#clear_button').show();
    state = states.DRAWN;
}

function clear(){
    $('#winner_name').html('');
    $('#next_button').show();
    $('#clear_button').hide();
    state = states.CLEARED;
}

jQuery(document).ready(function($){

    $('#clear_button').hide();

    $(document).on('keydown', function(e) {
        // on spacebar or enter
        if (e.which === 32 || e.which === 13) {
            e.preventDefault();
            if (state == states.CLEARED) {
                draw();
            } else if (state == states.DRAWN) {
                clear();
            }
        }
    });

    $('#next_button').click(draw);

    $('#clear_button').click(clear);

    $('#freshen_import').click(function() {
        $.ajax({
            url: '/reset',
            type: 'GET',
            success: function (result) {
              $('#feedback').text(result);
            }
        });
    });

    $('#wipe_data').click(function() {
        $.ajax({
            url: '/clear',
            type: 'GET',
            success: function (result) {
              $('#feedback').text(result);
            }
        });
    });
});

