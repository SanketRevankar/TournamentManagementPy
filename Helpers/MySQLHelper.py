from datetime import datetime

import mysql.connector
from mysqlx import ProgrammingError

from TournamentManagementPy import handler
from constants import StringConstants as sC, PyConstants as pC


class MySQLHelper:
    def __init__(self, config):
        self.MY_SQL_HOSTNAME_ = config[sC.MY_SQL][sC.HOSTNAME]
        self.MY_SQL_DATABASE_ = config[sC.MY_SQL][sC.DATABASE]
        self.MY_SQL_USERNAME_ = config[sC.MY_SQL][sC.USER_NAME]
        self.MY_SQL_PASSWORD_ = config[sC.MY_SQL][sC.PASS_WORD]

        print('{} - Initialized'.format(__name__))

    def get_connection(self):
        """
        Get MySQL DB connection

        :return: Connection variable for MySQL
        """
        cnx = None
        try:
            cnx = mysql.connector.connect(user=self.MY_SQL_USERNAME_, password=self.MY_SQL_PASSWORD_,
                                          host=self.MY_SQL_HOSTNAME_, database=self.MY_SQL_DATABASE_)
        except ProgrammingError:
            pass
        return cnx

    def execute_query(self, query):
        cnx = self.get_connection()
        cursor = cnx.cursor()
        resp = True
        try:
            cursor.execute(query)
            handler.logHelper.log_it_query(query)
        except ProgrammingError:
            handler.logHelper.log_it_query(query, status='Fail')
        finally:
            cnx.commit()
            cursor.close()
            self.close_connection(cnx)

        return resp

    @staticmethod
    def close_connection(cnx):
        """
        Close the DB connection

        :param cnx: Connection instance
        """

        cnx.close()

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
        match_id_ = self.match_with_ip_check(query_select)

        if match_id_:
            return match_id_

        query = sC.INSERT_MATCHES_VALUES_.format(int(match_id),
                                                 team1[:pC.MAX_CHARACTERS_SQL], team2[:pC.MAX_CHARACTERS_SQL],
                                                 team_tag1[:pC.MAX_CHARACTERS_SQL], team_tag2[:pC.MAX_CHARACTERS_SQL],
                                                 ip, team1_id, team2_id, datetime.now())

        self.execute_query(query)

    def create_database(self, query):
        cnx = None
        try:
            cnx = mysql.connector.connect(user=self.MY_SQL_USERNAME_,
                                          password=self.MY_SQL_PASSWORD_,
                                          host=self.MY_SQL_HOSTNAME_)
        except ProgrammingError:
            return
        cursor = cnx.cursor()
        cursor.execute(query)
        handler.logHelper.log_it_query(query)
        cnx.commit()
        cursor.close()
        self.close_connection(cnx)

    def match_with_ip_check(self, query):
        cnx = self.get_connection()
        cursor = cnx.cursor()
        cursor.execute(query)
        handler.logHelper.log_it_query(query)
        for result in cursor:
            if result:
                return result[0]
        cnx.commit()
        cursor.close()
        self.close_connection(cnx)

    def end_match(self, match_id):
        query = sC.DELETE_FROM_MATCHES_WHERE_ID_.format(match_id)

        self.execute_query(query)
