from TournamentManagementPy import handler
from constants import StringConstants as sC
from helpers.Util.AdminHelperUtil import AdminHelperUtil


class AdminHelper:
    def __init__(self, config):
        """
        Initiate Admin Helper
        This Class contains functions for helping with Admins on Server

        :param config: Config object
        """

        self.util = AdminHelperUtil(config)

        self.basic_access = 'm'
        self.admin_access = 'bcdefghijklmnopqrstuvy'
        self.admins = eval(config[sC.COUNTER_STRIKE_ADMINS][sC.ADMINS])
        self.table = handler.config[sC.MY_SQL][sC.ADMIN_TABLE]

    def remove_admin(self, player_id):
        """
        Remove admin access for the player with given Id if he is not an Admin

        :param player_id: Id of the Player
        """

        steam_id = self.util.get_steam_id(player_id)

        if not self.util.check_server_admin(steam_id):
            handler.mySQLHelper.execute_query(sC.DELETE_FROM_ADMINS_WHERE_ID_.format(self.table, steam_id))

    def add_admin(self, player_id):
        """
        Add admin access for the player with given Id if he is not an Admin

        :param player_id: Id of the Player
        """

        steam_id = self.util.get_steam_id(player_id)

        if not self.util.check_server_admin(steam_id):
            handler.mySQLHelper.execute_query(sC.INSERT_ADMINS_VALUES_.format(self.table, steam_id, self.basic_access))

    def add_server_admins(self):
        """
        Add admin access for all Admins

        """

        for admin in self.admins:
            handler.mySQLHelper.execute_query(sC.INSERT_ADMINS_VALUES_.format(self.table, admin, self.admin_access))

    def truncate_admin_table(self):
        """
        Remove admin access of everyone

        """

        handler.mySQLHelper.execute_query(sC.TRUNCATE_TABLE_.format(self.table))
