from django.http import HttpResponse, Http404
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def home(request):
    handler.authenticationHelper.validate_login(request)

    handler.logHelper.log_it_visit(request, __name__ + '.home')

    template = loader.get_template('Teams/teams.html')

    id_ = request.session['id']
    player_team = handler.dataHelper.get_team_id_by_player_id(id_)

    teams = handler.dataHelper.get_teams()
    team_list = []
    for i, team in enumerate(teams):
        team_list.append([i + 1, team, teams[team]['team_name'], teams[team]['team_tag'],
                          teams[team]['team_logo_url']])

    join_team = handler.fireStoreHelper.util.get_join_team_for_player_id(id_)

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'teams': team_list,
        'player_team': player_team,
        'join_team': join_team,
        'teams_page': True,
        'sidebar': True,
        'count': team_list.__len__(),
    }

    return HttpResponse(template.render(context, request))


def team_details(request, team_id):
    handler.authenticationHelper.validate_login(request)

    handler.logHelper.log_it_visit(request, __name__ + '.team_details')

    if not handler.dataHelper.check_team_with_id_exists(team_id):
        raise Http404

    template = loader.get_template('Teams/teams.html')
    id_ = request.session['id']
    player_team = handler.dataHelper.get_team_id_by_player_id(id_)

    team_data = handler.dataHelper.get_team_data_by_id(team_id)
    captain_data = handler.dataHelper.get_captain_by_team_id(team_id)
    players = handler.dataHelper.get_player_data_arr_by_id(team_data['players'])
    n_players = team_data['players'].__len__()

    join_team = handler.fireStoreHelper.util.get_join_team_for_player_id(id_)

    teams = handler.dataHelper.get_teams()
    team_list = []
    for i, team in enumerate(teams):
        team_list.append([i + 1, team, teams[team]['team_name'], teams[team]['team_tag'],
                          teams[team]['team_logo_url']])

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'player_count': players.__len__(),
        'teams': team_list,
        'player_team': player_team,
        'join_team': join_team,
        'team_id': team_id,
        'sidebar': True,
        'sidebar_active': True,
        **team_data,
        **captain_data,
        'players': players,
        'n_players': n_players,
        'max_players': int(handler.config[sC.PROJECT_DETAILS][sC.MAX_PLAYERS]),
    }

    return HttpResponse(template.render(context, request))
