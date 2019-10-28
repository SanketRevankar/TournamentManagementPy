from TournamentManagementPy import handler
from constants import StringConstants as sC


class AdminHelperUtil:
    def __init__(self, config):
        """
        Initiate Admin Helper Util
        This Class contains utilities for helping with Admin on Server

        :param config: Config object
        """

        self.admins = eval(config[sC.COUNTER_STRIKE_ADMINS][sC.ADMINS])

    @staticmethod
    def get_steam_id(player_id):
        """
        Get Steam Id from Player Id

        :param player_id: Id of the Player
        :return: Steam Id
        """

        return handler.dataHelper.get_player_steam_id(player_id)

    def check_server_admin(self, steam_id):
        """
        Check if Steam Id is of Admin

        :param steam_id: Steam Id
        :return: True or False
        """

        return steam_id in self.admins
