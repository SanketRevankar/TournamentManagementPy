import datetime
import json
import os
from ftplib import FTP

import requests

from TournamentManagementPy import handler
from constants import StringConstants as sC, PyConstants as pC
from firestore_data.ServerData import ServerList


class FTPHelper:
    def __init__(self, config):
        """
        Initialize the FTPHelper Class

        :param config: Config Object
        """
        self.locations_hltv_starting_ = config[sC.BUCKET_LOCATIONS][sC.HLTV_STARTING]
        self.score_starting_ = config[sC.BUCKET_LOCATIONS][sC.SCORE_STARTING]
        self.logs_starting_ = config[sC.BUCKET_LOCATIONS][sC.LOGS_STARTING]
        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]
        self.results_ = config[sC.FOLDER_LOCATIONS][sC.CONFIGS_RESULTS]
        self.amxmodx_logs_ = config[sC.FOLDER_LOCATIONS][sC.ADDONS_AMXMODX_LOGS]
        self.cstrike_logs_ = config[sC.FOLDER_LOCATIONS][sC.CSTRIKE_LOGS]

        _old_makepasv = FTP.makepasv

        print('{} - Initialized'.format(__name__))

        def _new_makepasv(self_):
            """
            To use passive mode for FTP

            :param self_: current reference
            :return: host and port
            """
            host, port = _old_makepasv(self_)
            host = self_.sock.getpeername()[0]
            return host, port

        FTP.makepasv = _new_makepasv

    @staticmethod
    def get_ftp_connection(server_id):
        """
        Get a connection for server with server Id from ServerList

        :param server_id: Id of the server as mentioned in ServerList
        :return:
        """
        node = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.INSTANCE_NAME])
        ip = handler.cloudServerHelper.util.ip(node)

        ftp = FTP()
        ftp.connect(ip, 21)
        ftp.login(ServerList[server_id][sC.USERNAME], ServerList[server_id][sC.PASSWORD])
        ftp.set_pasv(True)

        return ftp

    @staticmethod
    def close_ftp_connection(ftp):
        ftp.close()

    def download(self, ftp, src, des):
        """
        Download file from FTP to local

        :param ftp: FTP connection var
        :param src: Source path - Cloud
        :param des: Destination path - local
        """
        f = open(des, sC.WB_MODE)
        ftp.retrbinary(sC.RETR_ + src, f.write)

    def get_hltv_demos_from_ftp(self, date, server_id, folder):
        """
        Download Match HLTV demos from instance

        :param date: date for which the demos will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """
        ftp = self.get_ftp_connection(server_id)

        for file in ftp.mlsd(sC.CSTRIKE):
            if file[1][sC.TYPE] == sC.DIR or sC.DEMO_FORMAT not in file[0]:
                continue
            date_file = datetime.datetime.strptime(file[1][sC.MODIFY], pC.DATETIME_FORMAT)

            if date_file.astimezone() >= date:
                source = sC.CSTRIKE + sC.SEPARATOR + file[0]
                destination = self.locations_hltv_starting_ + folder + sC.SEPARATOR + file[0]
                temp_dest = self.temp + file[0]
                self.download(ftp, source, temp_dest)
                handler.cloudStorageHelper.upload_file(destination, temp_dest)
                os.remove(temp_dest)

        self.close_ftp_connection(ftp)

    def get_logs_from_ftp(self, date, server_id, folder):
        """
        Get log data from instance

        :param date: date for which the logs will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """
        # ftp = self.get_ftp_connection(server_id)
        #
        # folders = [
        #     [self.results_, self.score_starting_ + folder],
        #     [self.amxmodx_logs_, self.logs_starting_ + folder],
        #     [self.cstrike_logs_, self.logs_starting_ + folder],
        # ]
        #

        # for c_folder in folders:
        #     for file in ftp.mlsd(c_folder[0]):
        #         if file[1][sC.TYPE] == sC.DIR or (sC.LOG not in file[0] and sC.TXT not in file[0]):
        #             continue
        #         date_file = datetime.datetime.strptime(file[1][sC.MODIFY], pC.DATETIME_FORMAT)
        #
        #         if date_file.astimezone() >= date:
        #             source = c_folder[0] + sC.SEPARATOR + file[0]
        #             destination = c_folder[1] + sC.SEPARATOR + file[0]
        #             temp_dest = self.temp + file[0]
        #             self.download(ftp, source, temp_dest)
        #             handler.cloudStorageHelper.upload_file(destination, temp_dest)
        #             os.remove(temp_dest)
        #
        # self.close_ftp_connection(ftp)

        node = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.INSTANCE_NAME])
        ip = handler.cloudServerHelper.util.ip(node)

        request = {
            'score_starting_': self.score_starting_,
            'logs_starting_': self.logs_starting_,
            'folder': folder,
            'results_': self.results_,
            'amxmodx_logs_': self.amxmodx_logs_,
            'cstrike_logs_': self.cstrike_logs_,
            'ip': ip,
            'username': ServerList[server_id][sC.USERNAME],
            'password': ServerList[server_id][sC.PASSWORD],
            'date': date.timestamp(),
        }

        data_json = json.dumps(request)
        r = requests.post("https://us-central1-narcogaming.cloudfunctions.net/get_logs_from_ftp", json=data_json)
        print(r)
