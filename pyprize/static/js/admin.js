jQuery(document).ready(function($){

    $('#freshen_import').click(function() {
        $.ajax({
            url: '/reset',
            type: 'GET',
            success: function (result) {
              $('#feedback').text(result);
              window.location.reload(true);
            }
        });
    });
    
    $('#wipe_data').click(function() {
        $.ajax({
            url: '/clear',
            type: 'GET',
            success: function (result) {
                $('#feedback').text(result);
                window.location.reload(true);
            }
        });
    });
});
