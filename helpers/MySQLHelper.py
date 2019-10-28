from datetime import datetime

import mysql.connector
from mysqlx import ProgrammingError

from TournamentManagementPy import handler
from constants import StringConstants as sC, PyConstants as pC
from helpers.Util.MySQLHelperUtil import MySQLHelperUtil


class MySQLHelper:
    def __init__(self, config):
        """
        Initiate MySQL Helper
        This Class contains functions for helping with MySQL Queries

        :param config: Config object
        """

        self.util = MySQLHelperUtil(config)

        self.hostname = config[sC.MY_SQL][sC.HOSTNAME]
        self.database = config[sC.MY_SQL][sC.DATABASE]
        self.username = config[sC.MY_SQL][sC.USER_NAME]
        self.password = config[sC.MY_SQL][sC.PASS_WORD]

        print('{} - Initialized'.format(__name__))

    def execute_query(self, query):
        """
        Executes a Query on Database

        :param query: Query as str
        """

        cnx = self.util.get_connection()
        cursor = cnx.cursor()
        try:
            cursor.execute(query)
            handler.logHelper.log_it_query(query)
        except ProgrammingError:
            handler.logHelper.log_it_query(query, status='Fail')
        finally:
            cnx.commit()
            cursor.close()
            self.util.close_connection(cnx)


    def add_match(self, match_id, team1, team2, team_tag1, team_tag2, ip, team1_id, team2_id):
        """
        Add a new match to MySQL DB

        :param match_id: Id of the match
        :param team1: Name of team 1
        :param team2: Name of team 2
        :param team_tag1: Tag of team 1
        :param team_tag2: Tag of team 2
        :param ip: Ip of the server on which match will be player
        :param team1_id: Email of team 1 captain
        :param team2_id: Email of team 2 captain
        """

        query_select = sC.SELECT_MATCHES_WHERE_IP_.format(ip)
        match_id_ = self.util.match_with_ip_check(query_select)

        if match_id_:
            return match_id_

        query = sC.INSERT_MATCHES_VALUES_.format(int(match_id),
                                                 team1[:pC.MAX_CHARACTERS_SQL], team2[:pC.MAX_CHARACTERS_SQL],
                                                 team_tag1[:pC.MAX_CHARACTERS_SQL], team_tag2[:pC.MAX_CHARACTERS_SQL],
                                                 ip, team1_id, team2_id, datetime.now())

        self.execute_query(query)

    def create_database(self, query):
        """
        Creates a Database using MySQL Connection

        :param query: Create database query
        :return: None
        """

        try:
            cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.hostname)
        except ProgrammingError:
            return
        cursor = cnx.cursor()
        cursor.execute(query)
        handler.logHelper.log_it_query(query)
        cnx.commit()
        cursor.close()
        self.util.close_connection(cnx)

    def end_match(self, match_id):
        """
        Ends a active match and removes it from MySQL DB

        :param match_id: Id of the Match
        """

        query = sC.DELETE_FROM_MATCHES_WHERE_ID_.format(match_id)

        self.execute_query(query)
