import json

from TournamentManagementPy import handler
from constants import StringConstants as sC, PrintStrings as pS


def teams(_):
    teams_ = handler.dataHelper.get_teams()

    response = '<option selected>Select a Team</option>'
    for team in teams_:
        response += '<option value="{}" name="{}">{} [{}]</option>'.format(team, team, teams_[team]['team_name'],
                                                                           teams_[team]['team_tag'])
        del teams_[team]['join_requests']
        del teams_[team]['players']

    return {'html': response, 'team_data': {**teams_}}


def servers(_):
    servers_ = handler.dataHelper.get_servers()

    response = '<option selected>Select a Server</option>'
    match = ''
    hltv = ''
    server_data = {}

    for server in servers_:
        option = '<option value="{}" name="{}">{}</option>'.format(server, server, servers_[server]['Server Name'])
        if 'match' in server:
            match += option
        elif 'hltv' in server:
            hltv += option
        server_data[server] = {'server_name': servers_[server]['Server Name']}

    return {'match': response + match, 'hltv': response + hltv, 'server_data': {**server_data}}


def matches_created(_):
    matches = handler.fireStoreHelper.util.get_matches('Created')

    if matches.__len__() > 0:
        response = '<option selected>Select a Match to start</option>'
    else:
        response = '<option selected>Create a new match to start</option>'
    for match in matches:
        response += '<option value="{}" name="{}">{}. {} vs {}</option>'. \
            format(match, match, match,
                   handler.dataHelper.get_team_data_by_id(matches[match]['team_1'])['team_name'],
                   handler.dataHelper.get_team_data_by_id(matches[match]['team_2'])['team_name'])

    return {'matches': response}


def matches_started(_):
    matches = handler.fireStoreHelper.util.get_matches('Started')

    if matches.__len__() > 0:
        response = '<option selected>Select a Match to stop</option>'
    else:
        response = '<option selected>No matches are currently active</option>'
    for match in matches:
        response += '<option value="{}" name="{}">{}. {} vs {}</option>'. \
            format(match, match, match,
                   handler.dataHelper.get_team_data_by_id(matches[match]['team_1'])['team_name'],
                   handler.dataHelper.get_team_data_by_id(matches[match]['team_2'])['team_name'])

    return {'matches': response}


def vac_bans(_):
    create_steam_id64_list()
    ac = open(handler.config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER] +
              handler.config[sC.FILE_LOCATIONS][sC.STEAM_ID_LIST_TXT], sC.READ_PLUS_MODE)
    resp = acc_check_vac(ac)

    return {'html': resp}


def create_steam_id64_list():
    ac = open(handler.config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER] +
              handler.config[sC.FILE_LOCATIONS][sC.STEAM_ID_LIST_TXT], sC.WRITE_MODE)

    players = handler.dataHelper.get_players()
    for player in players:
        if 'steam_id' in players[player]:
            ac.write(players[player][sC.STEAM_URL_ID] + '\n')
    ac.close()


def acc_check_vac(ac):
    """
    VAC Ban checker for players

    """
    resp = ''

    def process_data_vac():
        """
        Process the data fetched from API

        """
        res = ''

        file_base = open(handler.config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER] +
                         handler.config[sC.FILE_LOCATIONS][sC.BANNED_USERS_FILE], sC.READ_PLUS_MODE)
        data = json.load(file_base)
        file_base.close()

        n = (len(data[sC.PLAYERS]))

        for n in range(0, n):
            if (data[sC.PLAYERS][n][sC.VAC_BANNED]) == bool(pS.TRUE):
                res += data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.VAC_BANNED_ + sC.SPACE + \
                       str(data[sC.PLAYERS][n][sC.NUMBER_OF_VAC_BANS]) + sC.SPACE + pS.LAST_TIME_ + sC.SPACE + \
                       str(data[sC.PLAYERS][n][sC.DAYS_SINCE_LAST_BAN]) + sC.SPACE + pS.DAYS_AGO
                res += sC.NEW_LINE + handler.localDataHelper.get_info(data[sC.PLAYERS][n][sC.STEAM_ID_]) + sC.NEW_LINE

            if (data[sC.PLAYERS][n][sC.COMMUNITY_BANNED]) == bool(pS.TRUE):
                res += data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.P_COMMUNITY_BANNED + sC.NEW_LINE

            if (data[sC.PLAYERS][n][sC.ECONOMY_BAN]) == bool(pS.TRUE):
                res += data[sC.PLAYERS][n][sC.STEAM_ID_] + pS.P_ECONOMY_BANN + sC.NEW_LINE

        if n != 0:
            return res + acc_check_vac(ac)

        return res

    if handler.localDataHelper.get_data(ac) != 0:
        resp += process_data_vac()

    return resp

def connections(request):
    steam_id = request.GET.get('steam_id')
    response = ''
    for blob in handler.cloudStorageHelper.get_blobs_by_prefix(handler.config[sC.BUCKET_LOCATIONS][sC.LOGS_STARTING]):
        if blob.name[-1] == '/':
            continue

        if sC.LOG not in blob.name:
            continue

        if sC.L_ in blob.name:
            continue

        blob_str = blob.download_as_string().decode()

        resp = handler.localDataHelper.get_connections(blob_str, steam_id)
        response += blob.name + sC.NEW_LINE + resp + sC.NEW_LINE

    return {'html': response}
