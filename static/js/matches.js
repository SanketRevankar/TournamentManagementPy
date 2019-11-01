$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    $('#content').html('<i class="fas fa-spinner fa-spin" style="font-size: 100px;margin-top: 35vh;margin-left: 40vw;"></i>' +
        '<h3 style="color: black; margin-left: 40vw; margin-top: 3vh;">Loading...</h3>');
    $.ajax({
        url: 'api/v1/get/get_match_data',
        success: function (data) {
            $('#content').html(data['match_data']);
        }
    });
});