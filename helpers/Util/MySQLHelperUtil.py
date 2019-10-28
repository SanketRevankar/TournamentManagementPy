import mysql.connector
from mysqlx import ProgrammingError

from TournamentManagementPy import handler
from constants import StringConstants as sC


class MySQLHelperUtil:
    def __init__(self, config):
        """
        Initiate MySQL Helper Util.
        This Class contains utilities for helping with MySQL operations

        :param config: Config object
        """

        self.hostname = config[sC.MY_SQL][sC.HOSTNAME]
        self.database = config[sC.MY_SQL][sC.DATABASE]
        self.username = config[sC.MY_SQL][sC.USER_NAME]
        self.password = config[sC.MY_SQL][sC.PASS_WORD]

        print('{} - Initialized'.format(__name__))

    def get_connection(self):
        """
        Get MySQL DB connection

        :return: Connection variable for MySQL
        """

        cnx = None
        try:
            cnx = mysql.connector.connect(user=self.username, password=self.password,
                                          host=self.hostname, database=self.database)
        except ProgrammingError:
            pass
        return cnx

    def match_with_ip_check(self, query):
        """
        Checks if match is set on the same server

        :param query: Query to run
        :return: Boolean whether match exists
        """

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

    @staticmethod
    def close_connection(cnx):
        """
        Close the DB connection

        :param cnx: Connection instance
        """

        cnx.close()
