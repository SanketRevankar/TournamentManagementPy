from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from Manager.api import Functions as ApiF, GetRequests as GetR, PutRequests as PutR
from TournamentManagementPy import handler
from constants import StringConstants as sC


@ensure_csrf_cookie
def welcome(request):
    handler.authenticationHelper.validate_admin(request)
    handler.logHelper.log_it_visit(request, __name__ + '.welcome')

    template = loader.get_template('Manager/Manage.html')

    admin_functions = {
        'new_match': {
            'title': 'Create a New Match',
            'title_sm': 'Create',
            'text': 'Used to create a new match',
            'function': 'new_match',
            'active': False,
            'fa_class': 'fas fa-plus',
        },
        'start_match': {
            'title': 'Start Match',
            'title_sm': 'Start',
            'text': 'Used to start a match which was created',
            'function': 'start_match',
            'active': False,
            'fa_class': 'fas fa-play',
        },
        'end_match': {
            'title': 'End Match',
            'title_sm': 'End',
            'text': 'Used to end a match which was started',
            'function': 'end_match',
            'active': False,
            'fa_class': 'fas fa-stop',
        },
        'match_scores': {
            'title': 'Match Scores',
            'title_sm': 'Scores',
            'text': 'Print map scores of all completed matches',
            'function': 'match_scores',
            'active': False,
            'fa_class': 'fab fa-stripe-s',
        },
        'player_stats': {
            'title': 'Player Stats',
            'title_sm': 'Stats',
            'text': 'Save Team-wise Player Stats to Excel File, default to team-wise_player-stats.xlsx',
            'function': 'player_stats',
            'active': False,
            'fa_class': 'fas fa-chart-bar',
        },
        'highest_stats': {
            'title': 'Top Stats',
            'title_sm': 'Top Stats',
            'text': 'Get top players for all stats over all matches, stats can be either actual values of stats or '
                    'average over number of matches played by that player',
            'function': 'highest_stats',
            'active': False,
            'fa_class': 'fas fa-sort-amount-up',
        },
        'ip_matches': {
            'title': 'IP matches',
            'title_sm': 'IP matches',
            'text': 'Print IPs of players if IP of 2 or more players matches over the period of tournament',
            'function': 'ip_matches',
            'active': False,
            'fa_class': 'fas fa-terminal',
        },
        'connections': {
            'title': 'Connections',
            'title_sm': 'Connections',
            'text': 'Print all connections and disconnections of a specific player',
            'function': 'connections',
            'active': False,
            'fa_class': 'fas fa-network-wired',
        },
        'team_details': {
            'title': 'Team Details',
            'title_sm': 'Team Details',
            'text': 'Save list of players per team to Excel File, default location team_details.xlsx',
            'function': 'team_details',
            'active': False,
            'fa_class': 'fas fa-info',
        },
        'vac_bans': {
            'title': 'VAC Bans',
            'title_sm': 'VAC Bans',
            'text': 'Check for VAC Bans of players using community Ids stored, default location resources/'
                    'Steam_id_list.txt',
            'function': 'vac_bans',
            'active': False,
            'fa_class': 'fas fa-ban',
        },
        'player_list': {
            'title': 'Player List',
            'title_sm': 'Player List',
            'text': 'Get the latest player list from Firestore',
            'function': 'player_list',
            'active': False,
            'fa_class': 'fas fa-user',
        },
        'team_list': {
            'title': 'Team List',
            'title_sm': 'Team List',
            'text': 'Get the latest team list from Datastore',
            'function': 'team_list',
            'active': False,
            'fa_class': 'fas fa-users',
        },
        'server_list': {
            'title': 'Server List',
            'title_sm': 'Server List',
            'text': 'Get the latest server list from Datastore',
            'function': 'server_list',
            'active': False,
            'fa_class': 'fas fa-server',
        },
        'match_list': {
            'title': 'Match List',
            'title_sm': 'Match List',
            'text': 'Get the latest match list from Datastore',
            'function': 'match_list',
            'active': False,
            'fa_class': 'fas fa-fist-raised',
        },
        'steam_ids_db': {
            'title': 'Steam IDs to DB',
            'title_sm': 'Steam IDs to DB',
            'text': 'Add all the players in constants/PlayerDetails.py to MySQL Database by team Id',
            'function': 'steam_ids_db',
            'active': False,
            'fa_class': 'fas fa-database',
        },
        'participation_certificates': {
            'title': 'Participation certificates',
            'title_sm': 'Participation certificates',
            'text': 'Prints certificates for players using a template image and print names of the players',
            'function': 'participation_certificates',
            'active': False,
            'fa_class': 'fas fa-graduation-cap',
        },
        'access_list': {
            'title': 'Access list for captains',
            'title_sm': 'Access list',
            'text': 'Print access strings for all captains.',
            'function': 'access_list',
            'active': False,
            'fa_class': 'fas fa-universal-access',
        },
    }

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'functions': [list(i.values()) for i in list(admin_functions.values())],
        'sidebar': True,
        'sidebar_active': True,
    }

    return HttpResponse(template.render(context, request))


def api_handler(request, name=None):
    handler.authenticationHelper.validate_admin(request)
    # handler.logHelper.log_it_api(request, __name__ + '.api_handler')

    functions = {
        'new_match': ApiF.new_match,
        'start_match': ApiF.start_match,
        'end_match': ApiF.end_match,
        'player_stats': ApiF.player_stats,
        'highest_stats': ApiF.highest_stats,
        'match_scores': ApiF.match_scores,
        'ip_matches': ApiF.ip_matches,
        'connections': ApiF.connections,
        'team_details': ApiF.team_details,
        'vac_bans': ApiF.vac_bans,
        'player_list': ApiF.player_list,
        'team_list': ApiF.team_list,
        'server_list': ApiF.server_list,
        'match_list': ApiF.match_list,
        'steam_ids_db': ApiF.steam_ids_db,
        'participation_certificates': ApiF.participation_certificates,
        'access_list': ApiF.access_list,
    }

    if not name or name not in functions:
        raise Http404

    return JsonResponse(functions[name]())


def get_api_handler(request, name=None):
    handler.authenticationHelper.validate_admin(request)
    # handler.logHelper.log_it_api(request, __name__ + '.get_api_handler')

    functions = {
        'teams': GetR.teams,
        'servers': GetR.servers,
        'matches_created': GetR.matches_created,
        'matches_started': GetR.matches_started,
        'vac_bans': GetR.vac_bans,
        'connections': GetR.connections,
        'ip_matches': GetR.ip_matches,
        'get_ip_logs': GetR.get_ip_logs,
    }

    if not name or name not in functions:
        raise Http404

    return JsonResponse(functions[name](request))


def put_api_handler(request, name=None):
    handler.authenticationHelper.validate_admin(request)
    handler.logHelper.log_it_api(request, __name__ + '.put_api_handler')

    functions = {
        'create_match': PutR.create_match,
        'start_match': PutR.start_match,
        'start_match_server': PutR.start_match_server,
        'start_hltv_server': PutR.start_hltv_server,
        'start_match_db': PutR.start_match_db,
        'end_match': PutR.end_match,
        'stop_match_server': PutR.stop_match_server,
        'stop_hltv_server': PutR.stop_hltv_server,
        'end_match_db': PutR.end_match_db,
        'download_match_logs': PutR.download_match_logs,
        'download_match_demos': PutR.download_match_demos,
        'parse_match_logs': PutR.parse_match_logs,
    }

    if not name or name not in functions:
        raise Http404

    return JsonResponse(functions[name](request))
