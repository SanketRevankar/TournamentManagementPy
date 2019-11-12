import datetime

import valve.source
import valve.source.a2s
from django.http import JsonResponse, HttpResponse

from TournamentManagementPy import handler


def get_server_data(request):
    ip = request.GET.get('ip')
    port = request.GET.get('port')

    player_data = []
    try:
        with valve.source.a2s.ServerQuerier((ip, int(port))) as server:
            info = server.info()
            players = server.players()

            for p in players['players']:
                player_data.append([p['name'], p['score'], str(datetime.timedelta(seconds=round(p['duration'])))])

    except valve.source.NoResponseError:
        return JsonResponse({'status': '404'})

    return JsonResponse({
        'server_name': info['server_name'],
        'game': info['game'],
        'map': info['map'],
        'players_online': '{}/{}'.format(info['player_count'], info['max_players']),
        'player_data': player_data,
        'player_count': players['player_count'],
        'status': '200'
    })


def adminship_request(request):
    server_selected = request.POST['serverSelected']

    admin_data = {
        request.POST['playerSteamId']: {
            'playerName': request.POST['playerName'],
            'playerNick': request.POST['playerNick'],
            'playerFbUrl': request.POST['playerFbUrl'],
            'playerExp': request.POST['playerExp'],
            'adminOnOtherSv': request.POST['adminOnOtherSv'],
        }
    }

    handler.adminHelper.add_game_server_admin_request(server_selected, admin_data)

    return HttpResponse('')


def adminship_response(request):
    handler.authenticationHelper.validate_approver(request)

    access_type, steam_id, server_id = request.POST['response'].split('-')

    if access_type == 'ignore':
        handler.fireStoreHelper.ignore_admin_request(steam_id, server_id)
    else:
        requester_data = handler.fireStoreHelper.util.get_requester_data_by_id(steam_id, server_id)
        access_data = {
            steam_id: {
                'access': access_type,
                'grantedBy': request.session['name'],
                'grantedOn': datetime.datetime.utcnow(),
                **requester_data,
            }
        }
        handler.fireStoreHelper.add_server_admin(access_data, server_id)
        handler.fireStoreHelper.ignore_admin_request(steam_id, server_id)
        handler.mySQLHelper.add_server_admin(steam_id, access_type, server_id)

    return HttpResponse('')


def update_admin(request):
    handler.authenticationHelper.validate_approver(request)

    access_type, steam_id, server_id = request.POST['response'].split('-')

    if access_type == 'remove':
        handler.fireStoreHelper.remove_server_admin(steam_id, server_id)
        handler.mySQLHelper.remove_server_admin(steam_id, server_id)
    else:
        requester_data = handler.fireStoreHelper.util.get_admin_data_by_id(steam_id, server_id)
        access_data = {
            steam_id: {
                **requester_data,
                'access': access_type,
                'grantedBy': request.session['name'],
                'grantedOn': datetime.datetime.utcnow(),
            }
        }
        handler.fireStoreHelper.add_server_admin(access_data, server_id)
        handler.mySQLHelper.update_server_admin(steam_id, access_type, server_id)

    return HttpResponse('')
