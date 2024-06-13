jQuery(document).ready(function($){
    $('#next_button').click(function() {
        $.ajax({
            url: '/next',
            type: 'GET',
            success: function (result) {
              var res = JSON.parse(result);
              $('#winner_name').html(res['name']);
              $('#feedback').text(res['feedback']);
            }
        });
    });
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

