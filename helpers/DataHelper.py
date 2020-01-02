import re

from TournamentManagementPy import handler
from constants import StringConstants as sC, PrintStrings as pS, PyConstants as pC
from firestore_data.PlayerData import PlayerList, SteamList
from firestore_data.ServerData import ServerList
from firestore_data.TeamData import TeamList


class DataHelper:
    def __init__(self):
        """
        Initialize the Data Helper
        This Class contains Data related Functions

        """

        self.approvers = eval(handler.config[sC.COUNTER_STRIKE_ADMINS][sC.APPROVERS])
        self.MODE = handler.config[sC.PROJECT_DETAILS][sC.MODE]
        self.mode_9 = self.MODE == '9'

    def get_player_steam_id(self, player_id):
        """
        Returns Steam Id of player using Id
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param player_id: Id of the Player
        :return: Steam Id of player
        """

        if self.mode_9:
            steam_id = PlayerList[player_id]['steam_id']
        else:
            player_data = self.get_player_data_by_id(player_id)
            steam_id = player_data['steam_id']
        return steam_id

    def get_teams(self):
        """
        Returns Team Data as a Dict Object
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :return: Team Data as a Dict Object
        """

        if self.mode_9:
            return TeamList.copy()
        return handler.fireStoreHelper.util.fsh_get_teams()

    def get_servers(self):
        """
        Returns Server Data as a Dict Object
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :return: Server Data as a Dict Object
        """

        if self.mode_9:
            return ServerList
        return handler.fireStoreHelper.util.fsh_get_servers()

    def get_players(self):
        """
        Returns Player Data as a Dict Object
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :return: Player Data as a Dict Object
        """

        if self.mode_9:
            return PlayerList
        return handler.fireStoreHelper.util.fsh_get_players()

    def get_captain_by_team_id(self, team_id):
        """
        Returns Captain of the using Id
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param team_id: Id of the Team
        :return: Captain's and V. Captains Details as a Dict Object
        """

        team_data = handler.fireStoreHelper.util.fsh_get_team_data_by_id(team_id)
        captain_data = self.get_player_data_by_id(team_data['captain'])
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
        """
        Returns Player Details as a Dict Object using Id
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param player_id: Id of the Player
        :return: Player Details as a Dict Object
        """

        if self.mode_9:
            return PlayerList[player_id]
        return handler.fireStoreHelper.util.fsh_get_player_data_by_id(player_id)

    def get_player_data_arr_by_id(self, players):
        """
        Returns Player Details as a List Object using Id
        List contains [Count, FB Id, FB Name, Steam Avatar, Steam URL Id, Steam Username, Player Id]
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param players: List of Ids of the Players
        :return: Player Details as a List Object
        """

        player_data_arr = []
        for i, player in enumerate(players):
            player_data = self.get_player_data_by_id(player)
            player_data_arr.append([i + 1, player_data['fb_id'], player_data['name'],
                                    player_data['avatar_url'], player_data['steam_url_id'],
                                    player_data['username'], player])

        return player_data_arr

    def get_team_data_by_id(self, team_id):
        """
        Returns Team Details as a Dict Object using Id
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param team_id: Id of the Team
        :return: Team Details as a Dict Object
        """

        if self.mode_9:
            return TeamList[team_id]
        return handler.fireStoreHelper.util.fsh_get_team_data_by_id(team_id)

    def get_team_id_by_player_id(self, player_id):
        """
        Get Team Id using Player Id if Player is in a Team or else return None
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param player_id: Id of the Player
        :return: Id of the Team or None
        """

        if self.mode_9:
            try:
                return PlayerList[player_id]['team']
            except KeyError:
                return None
        return handler.fireStoreHelper.util.fsh_get_team_id_by_player_id(player_id)

    def check_team_with_id_exists(self, team_id):
        """
        Check if Team with given Id exists
        Mode 1 & 2 -> Queries FireStore for data
        Mode 9 -> Uses local cache

        :param team_id: Id of the Team
        :return: True or False
        """

        if self.mode_9:
            return team_id in TeamList
        return handler.fireStoreHelper.util.check_team_with_id_exists(team_id)

    def team_name(self, team_id):
        """
        Returns Team Name and Team Tag of the team with given Id

        :param team_id: Id of the Team
        :return: Team Name and Team Tag
        """

        if self.mode_9:
            team_name = TeamList[team_id]['team_name']
            team_tag = TeamList[team_id]['team_tag']
        else:
            team_data = handler.dataHelper.get_team_data_by_id(team_id)
            team_name = team_data['team_name']
            team_tag = team_data['team_tag']

        return team_name, team_tag

    def get_team_by_steam_id(self, steam_id):
        """
        Returns Team of the player with given steam Id
        Only Made to use in Mode 9

        :param steam_id: Steam Id of the player
        :return: Team
        """

        if self.mode_9:
            return PlayerList[SteamList[steam_id]]['team']

    def get_team_name_by_steam_id(self, steam_id):
        """
        Returns Team of the player with given steam Id
        Only Made to use in Mode 9

        :param steam_id: Steam Id of the player
        :return: Team
        """

        if self.mode_9:
            return TeamList[PlayerList[SteamList[steam_id]]['team']]['team_name']

    def get_username_by_steam_id(self, steam_id):
        """
        Returns Team of the player with given steam Id
        Only Made to use in Mode 9

        :param steam_id: Steam Id of the player
        :return: Team
        """

        if self.mode_9:
            return PlayerList[SteamList[steam_id]]['username']

    def get_team_nick_name_by_s_id(self, steam_id):
        """
        Returns Team, Username and Name of the player with given steam Id
        Only Made to use in Mode 9

        :param steam_id: Steam Id of the player
        :return: Team, Username and Name
        """

        if self.mode_9:
            return PlayerList[SteamList[steam_id]]['team'] if 'team' in PlayerList[SteamList[steam_id]] else None, \
                PlayerList[SteamList[steam_id]]['username'], PlayerList[SteamList[steam_id]]['name']

    def get_ips_by_steam_id(self, steam_id):
        """
        Returns Ips of the player with given steam Id
        Only Made to use in Mode 9

        :param steam_id: Steam Id of the player
        :return: Team, Username and Name
        """

        if self.mode_9:
            return PlayerList[SteamList[steam_id]]['ips']


    @staticmethod
    def get_steam_id(index, current_team):
        """
        Get steam id of a player with given index belonging to a team if exists

        :param index: Index of the player
        :param current_team: Name of the team
        :return: Steam ID of the player
        """

        try:
            return PlayerList[TeamList[current_team][sC.PLAYERS][index]][sC.S_STEAM_ID]
        except IndexError:
            return sC.NO_PLAYER

    def get_match_name(self, match_id, matches):
        """
        Generate Folder name and create directories to store Logs,Scores and HLTV

        :param match_id: Id of the match
        :param matches: Dict of all matches
        :return: Name of the folder created
        """

        team_1 = self.get_clean_team_name(self.get_team_data_by_id(matches['team_1'])['team_name'])
        team_2 = self.get_clean_team_name(self.get_team_data_by_id(matches['team_2'])['team_name'])

        match_name = pS.MATCH_VS_.format(match_id, team_1, team_2)

        return match_name

    @staticmethod
    def get_clean_team_name(team_name):
        """
        Remove unwanted characters from Team name

        :param team_name: Team name
        :return: Cleaned name
        """

        return re.sub(pC.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, team_name)[:31]

    def check_admin_approver(self, player_id):
        return player_id in self.approvers
