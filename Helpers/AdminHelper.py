from TournamentManagementPy import handler
from constants import StringConstants as sC


class AdminHelper:
    def __init__(self, config):
        self.basic_access = 'm'
        self.admin_access = 'bcdefghijklmnopqrstuvy'
        self.admins = eval(config[sC.COUNTER_STRIKE_ADMINS][sC.ADMINS])
        self.table = handler.config[sC.MY_SQL][sC.ADMIN_TABLE]

    @staticmethod
    def __get_steam_id(player_id):
        return handler.dataHelper.get_player_steam_id(player_id)

    def __check_server_admin(self, steam_id):
        return steam_id in self.admins

    def remove_admin(self, player_id):
        steam_id = self.__get_steam_id(player_id)

        if not self.__check_server_admin(steam_id):
            handler.mySQLHelper.execute_query(sC.DELETE_FROM_ADMINS_WHERE_ID_.format(self.table, steam_id))

    def add_admin(self, player_id):
        steam_id = self.__get_steam_id(player_id)

        if not self.__check_server_admin(steam_id):
            handler.mySQLHelper.execute_query(sC.INSERT_ADMINS_VALUES_.format(self.table, steam_id, self.basic_access))

    def add_server_admins(self):
        for admin in self.admins:
            handler.mySQLHelper.execute_query(sC.INSERT_ADMINS_VALUES_.format(self.table, admin, self.admin_access))

    def truncate_admin_table(self):
        handler.mySQLHelper.execute_query(sC.TRUNCATE_TABLE_.format(self.table))
