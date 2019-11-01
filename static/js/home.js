let join_count = $('#join_count');
$.ajax({
    url: "/TeamFormation/api/v1/func/team_count",
    method: "post",
    data: {
        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
    },
    success: function (data) {
        join_count.text(data);
    }
});

$('[id^=accept-]').click(function() {
    var id = $(this).attr('id');
    var query = id.replace("accept-", "");
    let show_message = $('#show_message_'+query);
    let ignore_id = $('#ignore-'+query);
    let accept_id = $('#accept-'+query);

    if (join_count.text() === 32) {
        accept_id.attr('style', 'display:none');
        ignore_id.attr('style', 'display:none');
        show_message.text('Team Full!');
        show_message.attr('class', 'btn btn-danger');
        show_message.attr('style', 'display:block');
    } else {
        $.ajax({
            url: "/TeamFormation/api/v1/func/accept_player",
            method: "post",
            data: {
                'query': query,
                'csrfmiddlewaretoken': Cookies.get('csrftoken'),
            },

            success: function (_) {
                accept_id.attr('style', 'display:none');
                ignore_id.attr('style', 'display:none');
                show_message.text('Accepted!');
                show_message.attr('style', 'display:block');

                setTimeout(function () {
                    show_message.closest('tr').attr('style', 'display:none');
                }, 1000);

                $.ajax({
                    url: "/TeamFormation/api/v1/func/team_count",
                    method: "post",
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    },
                    success: function (data) {
                        join_count.text(data);
                        if (data === '0') {
                            setTimeout(function () {
                                location.reload();
                            }, 1000);
                        }
                    }
                });
            }
        });
    }
});

$('[id^=ignore-]').click(function() {
    var id = $(this).attr('id');
    var query = id.replace("ignore-", "");
    let show_message = $('#show_message_'+query);
    let ignore_id = $('#ignore-'+query);
    let accept_id = $('#accept-'+query);

    $.ajax({
        url: "/TeamFormation/api/v1/func/ignore_player",
        method: "post",
        data: {
            'query': query,
            'csrfmiddlewaretoken': Cookies.get('csrftoken'),
        },

        success:function(_) {
            accept_id.attr('style', 'display:none');
            ignore_id.attr('style', 'display:none');
            show_message.text('Ignored!');
            show_message.attr('class', 'btn btn-danger');
            show_message.attr('style', 'display:block');

            setTimeout(function () {
                show_message.closest('tr').attr('style', 'display:none');
            }, 1000);

            $.ajax({
                url: "/TeamFormation/api/v1/func/team_count",
                method: "post",
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                },

                success:function(data) {
                    join_count.text(data);
                    if (data === '0') {
                        setTimeout(function() {
                            location.reload();
                        }, 1000);
                    }
                }
            });
        }
    });
});