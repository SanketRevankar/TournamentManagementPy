from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data.PlayerData import PlayerList
from firestore_data.ServerData import ServerList
from firestore_data.TeamData import TeamList


class DataHelper:
    def __init__(self):
        self.MODE = handler.config[sC.PROJECT_DETAILS][sC.MODE]
        self.mode_9 = True if self.MODE == 9 else False

    def get_player_steam_id_nick(self, player_id):
        if self.mode_9:
            steam_id = PlayerList[player_id]['steam_id']
            username = PlayerList[player_id]['username']
        else:
            player_data = handler.dataHelper.get_player_data_by_id(player_id)
            steam_id = player_data['steam_id']
            username = player_data['username']

        return steam_id, username

    def get_player_steam_id(self, player_id):
        if self.mode_9:
            steam_id = PlayerList[player_id]['steam_id']
        else:
            player_data = self.get_player_data_by_id(player_id)
            steam_id = player_data['steam_id']
        return steam_id

    def get_teams(self):
        if self.mode_9:
            return TeamList
        return handler.fireStoreHelper.util.fsh_get_teams()

    def get_servers(self):
        if self.mode_9:
            return ServerList
        return handler.fireStoreHelper.util.fsh_get_servers()

    def get_players(self):
        if self.mode_9:
            return PlayerList
        return handler.fireStoreHelper.util.fsh_get_players()

    def get_captain_by_team_id(self, team_id):
        captain_data = self.get_player_data_by_id(team_id)
        team_data = self.get_team_data_by_id(team_id)
        vc_data_ = {}
        if 'vice_captain' in team_data:
            vc_data = self.get_player_data_by_id(team_data['vice_captain'])
            vc_data_ = {
                'vc_fb_id': vc_data['fb_id'],
                'vc_name': vc_data['name'],
                'vc_avatar_url': vc_data['avatar_url'],
                'vc_steam_url': vc_data['steam_url_id'],
                'vc_username': vc_data['username'],
            }

        return {
            'captain_fb_id': captain_data['fb_id'],
            'captain_name': captain_data['name'],
            'captain_avatar_url': captain_data['avatar_url'],
            'captain_steam_url': captain_data['steam_url_id'],
            'captain_username': captain_data['username'],
            **vc_data_,
        }

    def get_player_data_by_id(self, player_id):
        if self.mode_9:
            return PlayerList[player_id]
        return handler.fireStoreHelper.util.fsh_get_player_data_by_id(player_id)

    def get_player_data_arr_by_id(self, players):
        player_data_arr = []
        for i, player in enumerate(players):
            player_data = self.get_player_data_by_id(player)
            player_data_arr.append([i + 1, player_data['fb_id'], player_data['name'],
                                    player_data['avatar_url'], player_data['steam_url_id'],
                                    player_data['username'], player])

        return player_data_arr

    def get_team_data_by_id(self, team_id):
        if self.mode_9:
            return TeamList[team_id]
        return handler.fireStoreHelper.util.fsh_get_team_data_by_id(team_id)

    def get_team_id_by_player_id(self, player_id):
        if self.mode_9:
            try:
                return PlayerList[player_id]['team']
            except KeyError:
                return None
        return handler.fireStoreHelper.util.fsh_get_team_id_by_player_id(player_id)

    def check_team_with_id_exists(self, team_id):
        if self.mode_9:
            return team_id in TeamList
        return handler.fireStoreHelper.util.check_team_with_id_exists(team_id)

    def team_name(self, team_id):
        if self.mode_9:
            team_name = TeamList[team_id]['team_name']
            team_tag = TeamList[team_id]['team_tag']
        else:
            team_data = handler.dataHelper.get_team_data_by_id(team_id)
            team_name = team_data['team_name']
            team_tag = team_data['team_tag']

        return team_name, team_tag

    def get_team_nick_name_by_s_id(self, steam_id):
        player_data = self.get_players()
        for player in player_data:
            if player_data[player]['steam_id'] == steam_id:
                return player_data[player]['team'], player_data[player]['username'], player_data[player]['name']