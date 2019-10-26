from django.apps import AppConfig

from Helpers.AdminHelper import AdminHelper
from Helpers.AuthenticationHelper import AuthenticationHelper
from Helpers.CloudServerHelper import CloudServerHelper
from Helpers.CloudStorageHelper import CloudStorageHelper
from Helpers.ConfigHelper import ConfigHelper
from Helpers.DataHelper import DataHelper
from Helpers.FTPHelper import FTPHelper
from Helpers.FireStoreHelper import FireStoreHelper
from Helpers.LocalDataHelper import LocalDataHelper
from Helpers.LogHelper import LogHelper
from Helpers.MySQLHelper import MySQLHelper
from TournamentManagementPy import handler
from constants import StringConstants as sC


class MyAppConfig(AppConfig):
    name = 'TournamentManagementPy'

    def ready(self):
        # Load config from config/config.conf file
        configHelper = ConfigHelper()
        handler.config = configHelper.get_config()

        # Initialize Helper classes
        handler.fireStoreHelper = FireStoreHelper(handler.config)
        handler.localDataHelper = LocalDataHelper(handler.config)
        handler.cloudStorageHelper = CloudStorageHelper(handler.config)
        handler.logHelper = LogHelper()
        handler.authenticationHelper = AuthenticationHelper()
        handler.dataHelper = DataHelper()
        handler.adminHelper = AdminHelper(handler.config)
        handler.mySQLHelper = MySQLHelper(handler.config)

        # Initialize Helper classes for MODE = 9 (Registration Closed and teams finalized)
        if handler.config[sC.PROJECT_DETAILS][sC.MODE] == '9':
            handler.cloudServerHelper = CloudServerHelper(handler.config)
            handler.ftpHelper = FTPHelper(handler.config)
            handler.fireStoreHelper.util.load_player_data()
            handler.fireStoreHelper.util.load_team_data()
            handler.fireStoreHelper.util.load_server_data()

        # Create Folders and Buckets for storing logs and Create Databases and tables for 1st time run
        if eval(handler.config[sC.PROJECT_DETAILS][sC.INITIAL_SETUP]):
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.LOGS_STARTING])
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.SCORE_STARTING])
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.HLTV_STARTING])
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.IP_LOG_STARTING])
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.CERTIFICATES])
            handler.cloudStorageHelper.create_folder(handler.config[sC.BUCKET_LOCATIONS][sC.RESOURCES])

            handler.mySQLHelper.create_database(sC.CREATE_DATABASE.format(handler.config[sC.MY_SQL][sC.DATABASE]))
            handler.mySQLHelper.execute_query(sC.TABLE_MATCHES.format(sC.MATCHES))
            handler.mySQLHelper.execute_query(sC.TABLE_ADMINS.format(handler.config[sC.MY_SQL][sC.ADMIN_TABLE]))
