from datetime import datetime

from google.api_core.exceptions import AlreadyExists, PermissionDenied
from google.cloud import firestore_v1

from helpers.Util.FireStoreUtil import FireStoreUtil
from TournamentManagementPy import handler
from constants import StringConstants as sC


class FireStoreHelper:
    def __init__(self, config):
        """
        Initialize the FireStore Helper
        This Class contains FireStore related Functions

        :param config: Config object
        """

        self.util = FireStoreUtil(config)
        self.MATCHES = u'matches'
        self.PLAYERS = u'players'
        self.TEAMS = u'teams'
        self.HELP = u'help'

        print('{} - Initialized'.format(__name__))

    def facebook_login(self, name, email, fb_id, login_time, ip, city, location):
        """
        Function for Facebook login

        :param name: Facebook Name
        :param email: Facebook Login
        :param fb_id: Facebook Unique Id for user and login app
        :param login_time: Time of login
        :param ip: Ip of the user
        :param city: City of the user
        :param location: Location of the user in Lat, Long
        :return: Document Id -> Id of the player, Status -> Player Data is Created or not, Player Data if Data exists
        """

        collection_ref = self.util.get_collection(self.PLAYERS)
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
        """
        Function for Steam login

        :param steam_url: Steam URL Id
        :param steam_id: Steam Id32
        :param username: Steam Username
        :param avatar_url: Steam Avatar
        :param steam_account_created: Steam Account Created on
        :param doc_id: Player Id to add details in
        :param login_time: Time of Login
        """

        steam_login_data = {
            'steam_id': steam_id,
            'username': username,
            'avatar_url': avatar_url,
            'steam_url_id': steam_url,
            'steam_account_created': steam_account_created,
            'steam_login': login_time
        }

        self.util.update_document(self.PLAYERS, doc_id, steam_login_data)

    def create_team(self, team_id, team_name, team_tag, team_logo_url, player_id):
        """
        Create a new Team after validating no Team of same Name and Tag exists

        :param team_id: Id of the team
        :param team_name: Name of the Team
        :param team_tag: Tag of the Team
        :param team_logo_url: Logo of the Team
        :param player_id: Id of the team ie, Player Creating the team
        :return: Boolean, Boolean if Team with same Name, Tag Exists
        """

        collection_ref = self.util.get_collection(self.TEAMS)
        status_name, status_tag, status_id = False, False, False

        if self.util.check_team_with_id_exists(team_id):
            status_id = True

        docs = collection_ref.where(u'team_name', u'==', team_name).stream()
        for doc in docs:
            if doc.to_dict()['team_name'] == str(team_name):
                status_name = True

        docs = collection_ref.where(u'team_tag', u'==', team_tag).stream()
        for doc in docs:
            if doc.to_dict()['team_tag'] == str(team_tag):
                status_tag = True

        if status_name or status_tag:
            return status_name, status_tag, status_id

        doc_ref = collection_ref.document(document_id=team_id)
        doc_ref.create({'team_name': team_name, 'team_tag': team_tag, 'team_logo_url': team_logo_url,
                        'players': [player_id], 'join_requests': [], 'captain': player_id})

        join_team = self.util.clear_join_team_for_player(player_id)
        self.util.remove_player_id_from_all_teams_requests(join_team, player_id)
        self.util.get_player_ref_by_player_id(player_id).update({'team': team_id})

        return False, False, False

    def update_team(self, team_name, team_tag, team_logo_url, team_id):
        """
        Update Data of a existing Team

        :param team_name: New Name of the Team
        :param team_tag: New Tag of the Team
        :param team_logo_url: New Logo of the Team
        :param team_id: Id of the team
        """

        new_team_data = {'team_name': team_name, 'team_tag': team_tag, 'team_logo_url': team_logo_url}
        self.util.update_document(self.TEAMS, team_id, new_team_data)

    def delete_team(self, team_id, player_id):
        """
        Delete a Team, only if it is empty (except for the captain)

        :param team_id: Id of the Team to join
        :param player_id: Id of the Player
        :return: Boolean, Whether Team is Deleted or not
        """

        if self.util.fsh_get_team_data_by_id(team_id)['players'].__len__() > 1:
            return False

        self.util.get_team_ref_by_team_id(team_id).delete()
        self.leave_team(player_id)

        return True

    def join_team(self, player_id, team_id):
        """
        Called when a player requests to join a team with given Id

        :param player_id: Id of the Player
        :param team_id: Id of the Team to join
        """

        player_ref = self.util.get_player_ref_by_player_id(player_id)
        join_team = player_ref.get(['join_team']).get('join_team')
        join_team.append(team_id)
        player_ref.update({'join_team': join_team})

        team_ref = self.util.get_team_ref_by_team_id(team_id)
        join_requests = team_ref.get(['join_requests']).get('join_requests')
        join_requests.append(player_id)
        team_ref.update({'join_requests': join_requests})

    def accept_player(self, player_id, team_id):
        """
        Adds a Player to a Team

        :param player_id: Id of the Player
        :param team_id: Id of the Team
        """

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
        """
        Removes Player from a Team

        :param team_id: Id of the Team
        :param player_id: Id of the Player
        """

        team_ref = self.util.get_team_ref_by_team_id(team_id)
        team_data = self.util.fsh_get_team_data_by_id(team_id)
        players = team_data['players']
        players.remove(player_id)

        if 'vice_captain' in team_data and team_data['vice_captain'] == player_id:
            handler.adminHelper.remove_admin(player_id)

        team_ref.update({'players': players})

    def ignore_player(self, player_id, team_id):
        """
        Ignore a Join Request from a player

        :param player_id: Id of the Player
        :param team_id: Id of the Team
        """

        team_ref = self.util.get_team_ref_by_team_id(team_id)
        join_requests = team_ref.get(['join_requests']).get('join_requests')
        join_requests.remove(player_id)
        team_ref.update({'join_requests': join_requests})

        player_ref = self.util.get_player_ref_by_player_id(player_id)
        join_team = player_ref.get(['join_team']).get('join_team')
        join_team.remove(team_id)
        player_ref.update({'join_team': join_team})

    def leave_team(self, player_id):
        """
        Remove Player with Id from the team

        :param player_id: Id of the Player
        """

        team_id = self.util.fsh_get_team_id_by_player_id(player_id)
        if team_id:
            self.util.get_player_ref_by_player_id(player_id).update({'team': firestore_v1.DELETE_FIELD})

    def create_match(self, match_id, team_1, team_2, match_server, hltv_server, user_id, date_time):
        """
        Creates a new match

        :param match_id: Id of the Match
        :param team_1: Id of Team 1
        :param team_2: Id of Team 2
        :param match_server: Id of Match Server
        :param hltv_server: Id of HLTV Server
        :param user_id: Id of the Manager who created the match
        :param date_time: Time of match creation
        :return: Html string for indicating match creation status
        """

        match_ref = self.util.get_collection(self.MATCHES).document(match_id)

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
