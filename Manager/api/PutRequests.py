import datetime
import json

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data.ServerData import ServerList


def create_match(request):
    team_1 = request.POST['team_1']
    team_2 = request.POST['team_2']
    match_server = request.POST['match_server']
    hltv_server = request.POST['hltv_server']
    match_id = request.POST['match_id']
    date_time = request.POST['datetime']

    handler.logHelper.log_it_api(request, __name__ + '.create_match', target=match_id)
    handler.matchBannerHelper.create_banner(match_id, team_1, team_2, date_time)

    return {'match_id': handler.fireStoreHelper.create_match(match_id, team_1, team_2, match_server, hltv_server,
                                                             request.session['id'], date_time)}


def start_match(request):
    match_id = request.POST['match_id']

    handler.logHelper.log_it_api(request, __name__ + '.start_match', target=match_id)

    match_server, hltv_server = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)

    return {
        'match_server': ServerList[match_server][sC.SERVER_NAME],
        'hltv_server': ServerList[hltv_server][sC.SERVER_NAME]
    }


def start_match_server(request):
    match_id = request.POST['match_id']
    match_server, _ = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)
    match_ip, server_name = handler.cloudServerHelper.start_server(match_server)

    return {'status': 'Started', 'ip': match_ip, 'server_name': server_name}


def start_hltv_server(request):
    match_id = request.POST['match_id']
    _, hltv_server = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)
    hltv_ip, server_name = handler.cloudServerHelper.start_server(hltv_server)

    return {'status': 'Started', 'ip': hltv_ip, 'server_name': server_name}


def start_match_db(request):
    id_ = request.session['id']
    match_id = request.POST['match_id']
    match_ip = request.POST['match_ip']
    hltv_ip = request.POST['hltv_ip']
    match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)

    team_1 = match_data['team_1']
    team_2 = match_data['team_2']
    team1, team_tag1 = handler.dataHelper.team_name(team_1)
    team2, team_tag2 = handler.dataHelper.team_name(team_2)
    ip = ServerList[match_data['match_server']]['Server IP'] + ':' + ServerList[match_data['match_server']]['Port']
    match_id_ = handler.mySQLHelper.add_match(int(match_id), team1, team2, team_tag1, team_tag2, ip, team_1, team_2)
    if match_id_:
        return {'error': 'Match with id {} is already set, stop that match before starting this one.'.format(match_id_)}

    handler.fireStoreHelper.util.update_document('matches', match_id,
                                                 {'status': 'Started', 'start_time': datetime.datetime.utcnow(),
                                                  'started_by': id_, 'hltv_external_ip': hltv_ip,
                                                  'match_external_ip': match_ip})

    return {'status': 'Success'}


def end_match(request):
    match_id = request.POST['match_id']
    match_server, hltv_server = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)
    match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)
    folder = handler.dataHelper.get_match_name(match_id, match_data)
    handler.localDataHelper.create_dirs_for_match_data(folder)

    handler.logHelper.log_it_api(request, __name__ + '.end_match', target=match_id)

    return {
        'match_server': ServerList[match_server][sC.SERVER_NAME],
        'hltv_server': ServerList[hltv_server][sC.SERVER_NAME],
        'match_name': folder,
    }


def download_match_logs(request):
    match_id = request.POST['match_id']
    match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)
    folder = handler.dataHelper.get_match_name(match_id, match_data)

    start_time = match_data['start_time'].replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
    handler.ftpHelper.get_logs_from_ftp(start_time, match_data['match_server'], folder)

    return {'status': 'Completed'}


def download_match_demos(request):
    match_id = request.POST['match_id']
    match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)
    folder = handler.dataHelper.get_match_name(match_id, match_data)

    start_time = match_data['start_time'].replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
    handler.ftpHelper.get_hltv_demos_from_ftp(start_time, match_data['hltv_server'], folder)

    return {'status': 'Completed'}


def stop_match_server(request):
    match_id = request.POST['match_id']
    match_server, _ = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)
    handler.cloudServerHelper.stop_server(match_server)

    return {'status': 'Stopped'}


def stop_hltv_server(request):
    match_id = request.POST['match_id']
    _, hltv_server = handler.fireStoreHelper.util.get_servers_by_match_id(match_id)
    handler.cloudServerHelper.stop_server(hltv_server)

    return {'status': 'Stopped'}


def parse_match_logs(request):
    match_id = request.POST['match_id']
    match_data = handler.fireStoreHelper.util.get_match_data_by_id(match_id)

    match_name = handler.dataHelper.get_match_name(match_id, match_data)
    stats = handler.localDataHelper.get_stats_from_logs(match_name)
    handler.localDataHelper.upload_stats_to_bucket(match_name, stats)
    handler.fireStoreHelper.util.update_document(handler.fireStoreHelper.MATCHES, match_id, {'stats': stats})
    handler.localDataHelper.save_logs(match_name)

    return {'status': 'Completed'}


def end_match_db(request):
    match_id = request.POST['match_id']
    scores = json.loads(request.POST['scores'])
    id_ = request.session['id']

    map_count = 1
    for map_ in scores:
        score = '{}-{}'.format(scores[map_]['team_1'], scores[map_]['team_2'])
        handler.fireStoreHelper.util.update_document('matches', match_id, {
            'map_{}'.format(map_count): {
                'name': map_,
                'score': score,
            }
        })
        map_count += 1

    handler.fireStoreHelper.util.update_document('matches', match_id, {'status': 'Completed', 'stopped_by': id_,
                                                                       'end_time': datetime.datetime.utcnow()})

    handler.mySQLHelper.end_match(match_id)

    return {'status': 'Success'}
