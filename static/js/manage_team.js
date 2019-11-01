$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    container: 'body',

    onConfirm: function (_) {
        const id = $(this).attr('id');

        if (id.match('^kick')) {
            const query = id.replace("kick-", "");

            $.ajax({
                url: "/TeamFormation/api/v1/func/remove_player",
                method: "post",
                data: {
                    'query': query,
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                },
                success: function (_) {
                    $('#' + id).text('Kicked!').attr('class', 'btn btn-success');
                    setTimeout(function () {
                        $('a#' + id).closest('tr').remove();
                    }, 1000);
                    setTimeout(function () {
                        if ($("tbody tr").length === 1) {
                            setTimeout(function () {
                                window.location.reload();
                            }, 1020);
                        }
                    }, 1000);
                }
            });
        }

        if (id.match('^rem')) {
            const query = id.replace("rem-", "");

            $.ajax({
                url: "/TeamFormation/api/v1/func/remove_captain",
                method: "post",
                data: {
                    'query': query,
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                },
                success: function (_) {
                    window.location.reload();
                }
            });
        }

        if (id.match('^capt')) {
            const query = id.replace("capt-", "");

            $.ajax({
                url: "/TeamFormation/api/v1/func/make_captain",
                method: "post",
                data: {
                    'query': query,
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                },
                success: function (_) {
                    window.location.reload();
                }
            });
        }
    },

    onCancel: function () {
    }
});