let logoUrl = $('#logo_url');
let logoShow = $("#logo_show");
let id = $('#id_');

function testImage(url, timeoutT) {
    return new Promise(function (resolve, _) {
        const timeout = timeoutT || 5000;
        let timer, img = new Image();
        img.onerror = img.onabort = function () {
            clearTimeout(timer);
            logoShow.attr("style", "width:0vh; height: 0vh;visibility: hidden;");
            logoUrl.removeClass('is-valid').removeClass('is-invalid');
            logoUrl.addClass('is-invalid');
        };
        img.onload = function () {
            clearTimeout(timer);
            resolve("success");
            logoUrl.removeClass('is-valid').removeClass('is-invalid');
            logoUrl.addClass('is-valid');
            logoShow.attr("style", "width:30vh; height: 30vh;visibility: inherit;").attr("src", url);
        };
        timer = setTimeout(function () {
            logoShow.attr("style", "width:0vh; height: 0vh; visibility: hidden;");
        }, timeout);
        img.src = url;
    });
}

logoUrl.bind("change keyup input",function() {
    const search = $(this).val();
    if (search.match('^http.*$')) {
        testImage(search, 300);
    } else {
        logoUrl.removeClass('is-valid').removeClass('is-invalid');
        logoUrl.addClass('is-invalid');
        logoShow.attr("style", "width:0vh; height: 0vh;visibility: hidden;");
    }
});

function validate() {
    return logoUrl.hasClass('is-valid') && id.hasClass('is-valid');
}

id.on('input', function() {
    const team_id = $(this).val();
    $('#small_id_').html(team_id);
    $(this).removeClass('is-valid').removeClass('is-invalid');
    if (team_id.match('^[A-Za-z_]+$')) {
        $(this).addClass('is-valid');
    } else {
        $(this).addClass('is-invalid');
    }
});