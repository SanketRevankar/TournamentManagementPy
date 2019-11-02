var isPhoto = false;

function testImage(url, timeoutT) {
    return new Promise(function (resolve, _) {
        var timeout = timeoutT || 5000;
        var timer, img = new Image();
        img.onerror = img.onabort = function () {
            clearTimeout(timer);
            $("#logo_show").attr("style", "width:0vh; height: 0vh;visibility: hidden;");
            isPhoto = false;
        };
        img.onload = function () {
            clearTimeout(timer);
            resolve("success");
            isPhoto = true;
            $("#logo_show").attr("style", "width:30vh; height: 30vh;visibility: inherit;").attr("src", url);
        };
        timer = setTimeout(function () {
            $("#logo_show").attr("style", "width:0vh; height: 0vh; visibility: hidden;");
        }, timeout);
        img.src = url;
    });
}

$(document).ready(function () {
    let $logoUrl = $('#logo_url');
    testImage($logoUrl.val(), 300);
    $logoUrl.bind("change keyup input",function() {
        var search = $(this).val();
        if (search !== '') {
            testImage(search, 300);
        } else {
            $("#logo_show").attr("style", "width:0vh; height: 0vh;visibility: hidden;");
        }
    });
});

function photoValidate() {
    if (isPhoto)
        return true;
    else {
        window.alert('Enter Valid Image URL to continue.');
        return false;
    }
}