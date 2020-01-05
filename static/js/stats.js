let team_list = $('#team_list')
let view_stats = $('#view-stats')

team_list.click(function () {
    let team = team_list.val();

    team_list.removeClass('is-valid').removeClass('is-invalid');

    if (!team.match('Select a Team')) {
        team_list.addClass('is-valid');
    } else {
        team_list.addClass('is-invalid');
    }
});

view_stats.click(function () {
    let team = team_list.val();

    if (team_list.hasClass('is-valid')) {
        window.location.href = 'Stats/Team/' + team
    } else {
        return false;
    }
});