$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});
let last_id = null;

$('.api-call').click(function () {
    let id = $(this).attr('function');
    $('#content').html('<i class="fas fa-spinner fa-spin" style="font-size: 100px;margin-top: 35vh;margin-left: 40vw;"></i>' +
        '<h3 style="color: black; margin-left: 40vw; margin-top: 3vh;">Loading...</h3>');
    if (last_id !== null) {
        $('#' + last_id).removeClass('active');
    }
    $('#' + id).addClass('active');
    last_id = id;

    $.ajax({
        url: 'api/v1/func/' + id,
        success: function (data) {
            $('#content').html(data['html']);
            let $sidebar = $('#sidebar');
            $sidebar.removeClass('active');
            $sidebar.addClass('active');
        }
    })
});