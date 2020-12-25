let kills = $('#kills');
let headshot = $('#headshot');
let knife = $('#knife');
let grenade = $('#grenade');
let defuse = $('#defuse');
let plants = $('#plants');
let deaths = $('#deaths');
let suicide = $('#suicide');

$.ajax({
    url: 'api/v1/get/top/Kills',
    success: function(data) {
        kills.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Headshot',
    success: function(data) {
        headshot.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Grenade',
    success: function(data) {
        grenade.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Knife',
    success: function(data) {
        knife.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Defuse',
    success: function(data) {
        defuse.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Plants',
    success: function(data) {
        plants.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Deaths',
    success: function(data) {
        deaths.html(data['html'])
    },
});

$.ajax({
    url: 'api/v1/get/top/Suicide',
    success: function(data) {
        suicide.html(data['html'])
    },
});
