import json

import requests
from django.views.defaults import server_error

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data.ServerData import ServerList


class FTPHelper:
    def __init__(self, config):
        """
        Initialize the FTP Helper
        This Class contains FTP related Functions

        :param config: Config Object
        """

        self.locations_hltv_starting_ = config[sC.BUCKET_LOCATIONS][sC.HLTV_STARTING]
        self.score_starting_ = config[sC.BUCKET_LOCATIONS][sC.SCORE_STARTING]
        self.logs_starting_ = config[sC.BUCKET_LOCATIONS][sC.LOGS_STARTING]
        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]
        self.results_ = config[sC.FOLDER_LOCATIONS][sC.CONFIGS_RESULTS]
        self.amxmodx_logs_ = config[sC.FOLDER_LOCATIONS][sC.ADDONS_AMXMODX_LOGS]
        self.cstrike_logs_ = config[sC.FOLDER_LOCATIONS][sC.CSTRIKE_LOGS]
        self.hltv_demos_func_url = config[sC.CLOUD_FUNCTIONS_URLS][sC.HLTV_DEMOS_FUNC]
        self.ftp_logs_func_url = config[sC.CLOUD_FUNCTIONS_URLS][sC.FTP_LOGS_FUNC]

        print('{} - Initialized'.format(__name__))

    def get_hltv_demos_from_ftp(self, date, server_id, folder):
        """
        Download Match HLTV demos from instance

        :param date: date for which the demos will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """

        node = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.INSTANCE_NAME])
        ip = handler.cloudServerHelper.util.ip(node)

        request = {
            'locations_hltv_starting_': self.locations_hltv_starting_,
            'folder': folder,
            'ip': ip,
            'username': ServerList[server_id][sC.USERNAME],
            'password': ServerList[server_id][sC.PASSWORD],
            'date': date.timestamp(),
        }

        data_json = json.dumps(request)
        r = requests.post(self.hltv_demos_func_url, json=data_json)
        if r.status_code != 200:
            raise server_error

    def get_logs_from_ftp(self, date, server_id, folder):
        """
        Get log data from instance

        :param date: date for which the logs will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """

        node = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.INSTANCE_NAME])
        ip = handler.cloudServerHelper.util.ip(node)

        request = {
            'score_starting_': self.score_starting_,
            'logs_starting_': self.logs_starting_,
            'results_': self.results_,
            'amxmodx_logs_': self.amxmodx_logs_,
            'cstrike_logs_': self.cstrike_logs_,
            'folder': folder,
            'ip': ip,
            'username': ServerList[server_id][sC.USERNAME],
            'password': ServerList[server_id][sC.PASSWORD],
            'date': date.timestamp(),
        }

        data_json = json.dumps(request)
        r = requests.post(self.ftp_logs_func_url, json=data_json)

        if r.status_code != 200:
            raise server_error
