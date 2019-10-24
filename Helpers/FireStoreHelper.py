from datetime import datetime

from google.api_core.exceptions import AlreadyExists, PermissionDenied
from google.cloud import firestore_v1

from Helpers.Util.FireStoreUtil import FireStoreUtil
from TournamentManagementPy import handler
from constants import StringConstants as sC


class FireStoreHelper:
    def __init__(self):
        self.util = FireStoreUtil()
        self.db = firestore_v1.Client()
        self.MATCHES = u'matches'
        self.PLAYERS = u'players'
        self.TEAMS = u'teams'

        print('{} - Initialized'.format(__name__))

    def facebook_login(self, name, email, fb_id, login_time, ip, city, location):
        collection_ref = self.db.collection(self.PLAYERS)
        docs = collection_ref.where(u'fb_id', u'==', fb_id).stream()

        for doc in docs:
            doc_data = doc.to_dict()
            if doc_data['fb_id'] == str(fb_id):
                if 'steam_id' in doc_data:
                    ips = doc_data['ips']
                    if ip not in ips:
                        ips[ip] = {'city': city, 'location': location}
                    collection_ref.document(doc.id).update({'ips': ips})
                    return doc.id, True, {'steam_id': doc_data['steam_id'], 'steam_url_id': doc_data['steam_url_id'],
                                          'avatar_url': doc_data['avatar_url'], 'username': doc_data['username']}
                else:
                    return doc.id, False, {}

        doc_ref = collection_ref.document()
        doc_ref.create({'name': name, 'email': email, 'fb_id': fb_id, 'facebook_login': login_time, 'join_team': [],
                        'ips': [ip]})

        return doc_ref.id, False, {}

    def steam_login(self, steam_url, steam_id, username, avatar_url, steam_account_created, doc_id, login_time):
        collection_ref = self.db.collection(self.PLAYERS)
        doc_ref = collection_ref.document(doc_id)
        doc_ref.update({'steam_id': steam_id, 'username': username, 'avatar_url': avatar_url, 'steam_url_id': steam_url,
                        'steam_account_created': steam_account_created, 'steam_login': login_time})

    def create_team(self, team_name, team_tag, team_logo_url, player_id):
        collection_ref = self.db.collection(self.TEAMS)
        status_name, status_tag = False, False

        docs = collection_ref.where(u'team_name', u'==', team_name).stream()
        for doc in docs:
            if doc.to_dict()['team_name'] == str(team_name):
                status_name = True

        docs = collection_ref.where(u'team_tag', u'==', team_tag).stream()
        for doc in docs:
            if doc.to_dict()['team_tag'] == str(team_tag):
                status_tag = True

        if status_name or status_tag:
            return status_name, status_tag

        doc_ref = collection_ref.document(document_id=player_id)
        doc_ref.create({'team_name': team_name, 'team_tag': team_tag, 'team_logo_url': team_logo_url,
                        'players': [player_id], 'join_requests': [], 'captain': player_id})

        join_team = self.util.clear_join_team_for_player(player_id)
        self.util.remove_player_id_from_all_teams_requests(join_team, player_id)
        self.util.get_player_ref_by_player_id(player_id).update({'team': player_id})

        return False, False

    def update_team(self, team_name, team_tag, team_logo_url, id_):
        self.util.get_team_ref_by_team_id(id_).update(
            {'team_name': team_name, 'team_tag': team_tag, 'team_logo_url': team_logo_url})

    def delete_team(self, team_id, player_id):
        if self.util.fsh_get_team_data_by_id(team_id)['players'].__len__() > 1:
            return False

        self.util.get_team_ref_by_team_id(team_id).delete()
        self.leave_team(player_id)

        return True

    def join_team(self, id_, team_id):
        player_ref = self.util.get_player_ref_by_player_id(id_)
        join_team = player_ref.get(['join_team']).get('join_team')
        join_team.append(team_id)
        player_ref.update({'join_team': join_team})

        team_ref = self.util.get_team_ref_by_team_id(team_id)
        join_requests = team_ref.get(['join_requests']).get('join_requests')
        join_requests.append(id_)
        team_ref.update({'join_requests': join_requests})

    def accept_player(self, player_id, team_id):
        team_ref = self.util.get_team_ref_by_team_id(team_id)
        players = team_ref.get(['players']).get('players')
        if players.__len__() >= int(handler.config[sC.PROJECT_DETAILS][sC.MAX_PLAYERS]):
            raise PermissionDenied('Team already has max players')
        team_ref.update({
            'players': players + [player_id],
        })

        join_team = self.util.clear_join_team_for_player(player_id)
        self.util.remove_player_id_from_all_teams_requests(join_team, player_id)
        self.util.get_player_ref_by_player_id(player_id).update({'team': team_id})

    def remove_player_from_team(self, team_id, player_id):
        team_ref = self.util.get_team_ref_by_team_id(team_id)
        team_data = self.util.fsh_get_team_data_by_id(team_id)
        players = team_data['players']
        players.remove(player_id)

        if 'vice_captain' in team_data and team_data['vice_captain'] == player_id:
            handler.adminHelper.remove_admin(player_id)

        team_ref.update({'players': players})

    def ignore_player(self, player_id, team_id):
        team_ref = self.util.get_team_ref_by_team_id(team_id)
        join_requests = team_ref.get(['join_requests']).get('join_requests')
        join_requests.remove(player_id)
        team_ref.update({'join_requests': join_requests})

        player_ref = self.util.get_player_ref_by_player_id(player_id)
        join_team = player_ref.get(['join_team']).get('join_team')
        join_team.remove(team_id)
        player_ref.update({'join_team': join_team})

    def leave_team(self, player_id):
        team_id = self.util.fsh_get_team_id_by_player_id(player_id)
        if team_id:
            self.util.get_player_ref_by_player_id(player_id).update({'team': firestore_v1.DELETE_FIELD})

    def create_match(self, match_id, team_1, team_2, match_server, hltv_server, user_id, date_time):
        match_ref = self.db.collection(self.MATCHES).document(match_id)

        try:
            match_ref.create({
                'team_1': team_1,
                'team_2': team_2,
                'match_server': match_server,
                'hltv_server': hltv_server,
                'match_time': datetime.strptime(date_time + ' +0530', '%Y-%m-%dT%H:%M %z'),
                'status': 'Created',
                'created_by': user_id,
            })
        except AlreadyExists:
            return '<p class="text-danger">Match with id {} already exists</p>'.format(match_id)

        return '<p class="text-success">Match with id {} created</p>'.format(match_id)
