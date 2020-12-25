document.getElementById('loginBtn').addEventListener('click', function () {
    FB.login(function (response) {
        if (response.authResponse) {
            //user just authorized your app
        }
    }, {scope: 'email,public_profile', return_scopes: true});
}, false);

function statusChangeCallback(response) {
    if (response && response.status === 'connected') {
        testAPI();
    } else {
    }
}

function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

window.fbAsyncInit = function () {
    FB.init({
        appId: fbId,
        cookie: true,  // enable cookies to allow the server to access
                       // the session
        xfbml: true,  // parse social plugins on this page
        version: 'v2.8' // use graph api version 2.8
    });

    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });

    // After your onload method has been called and initial login state has
    // already been determined. (See above about not using these during a page's
    // init function.)
    FB.Event.subscribe('auth.authResponseChange', auth_response_change_callback);
    FB.Event.subscribe('auth.statusChange', auth_status_change_callback);

};

// In your JavaScript
var auth_response_change_callback = function (response) {
    statusChangeCallback(response);
};

var auth_status_change_callback = function (response) {
    statusChangeCallback(response);
};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function testAPI() {
    FB.api('/me?fields=email,name', function (response) {
        if (!response["error"]) {
            var form = document.getElementById('form');
            form.method = 'post';
            form.action = 'steam';
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'name';
            input.value = response["name"];
            form.appendChild(input);
            var input1 = document.createElement('input');
            input1.type = 'hidden';
            input1.name = 'email';
            input1.value = response["email"];
            form.appendChild(input1);
            var input2 = document.createElement('input');
            input2.type = 'hidden';
            input2.name = 'id';
            input2.value = response["id"];
            form.appendChild(input2);
            form.submit();
        }
    });
}

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.12&appId=' + fbId + '&autoLogAppEvents=1';
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function status() {
    FB.api('/me?fields=email,name', function (response) {
    });
}