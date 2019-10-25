import datetime
import os
from ftplib import FTP

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

        print('{} - Initialized'.format(__name__))


    @staticmethod
    def get_ftp_connection(server_id):
        """
        Get a connection for server with server Id from ServerList

        :param server_id: Id of the server as mentioned in ServerList
        :return:
        """
        ip = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.SERVER_IP])
        # node = handler.cloudServerHelper.util.get_node(ServerList[server_id][sC.INSTANCE_NAME])
        # ip = handler.cloudServerHelper.util.ip(node)

        ftp = FTP()
        ftp.connect(ip, 21)
        ftp.login(ServerList[server_id][sC.USERNAME], ServerList[server_id][sC.PASSWORD])
        ftp.set_pasv(True)

        return ftp

    @staticmethod
    def close_ftp_connection(ftp):
        ftp.close()

    def download(self, server_id, src, des):
        """
        Download file from FTP to local

        :param ftp: FTP connection var
        :param src: Source path - Cloud
        :param des: Destination path - local
        """
        ftp = self.get_ftp_connection(server_id)

        f = open(des, sC.WB_MODE)
        ftp.retrbinary(sC.RETR_ + src, f.write)
        self.close_ftp_connection(f)

        self.close_ftp_connection(ftp)

    def get_hltv_demos_from_ftp(self, date, server_id, folder):
        """
        Download Match HLTV demos from instance

        :param date: date for which the demos will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """
        ftp = self.get_ftp_connection(server_id)
        files = []
        for file in ftp.mlsd(sC.CSTRIKE):
            if file[1][sC.TYPE] == sC.DIR or sC.DEMO_FORMAT not in file[0]:
                continue
            files.append(file)
        self.close_ftp_connection(ftp)

        for file in files:
            date_file = datetime.datetime.strptime(file[1][sC.MODIFY], pC.DATETIME_FORMAT)

            if date_file.astimezone() >= date:
                source = sC.CSTRIKE + sC.SEPARATOR + file[0]
                destination = self.locations_hltv_starting_ + folder + sC.SEPARATOR + file[0]
                temp_dest = self.temp + file[0]
                self.download(server_id, source, temp_dest)
                handler.cloudStorageHelper.upload_file(destination, temp_dest)
                os.remove(temp_dest)

    def get_logs_from_ftp(self, date, server_id, folder):
        """
        Get log data from instance

        :param date: date for which the logs will be downloaded
        :param server_id: Id of the server
        :param folder: Destination folder
        """

        folders = [
            [self.results_, self.score_starting_ + folder],
            [self.amxmodx_logs_, self.logs_starting_ + folder],
            [self.cstrike_logs_, self.logs_starting_ + folder],
        ]

        for c_folder in folders:
            ftp = self.get_ftp_connection(server_id)
            files = []
            for file in ftp.mlsd(c_folder[0]):
                if file[1][sC.TYPE] == sC.DIR or (sC.LOG not in file[0] and sC.TXT not in file[0]):
                    continue
                files.append(file)
            self.close_ftp_connection(ftp)

            for file in files:
                date_file = datetime.datetime.strptime(file[1][sC.MODIFY], pC.DATETIME_FORMAT)

                if date_file.astimezone() >= date:
                    source = c_folder[0] + sC.SEPARATOR + file[0]
                    destination = c_folder[1] + sC.SEPARATOR + file[0]
                    temp_dest = self.temp + file[0]
                    self.download(ftp, source, temp_dest)
                    handler.cloudStorageHelper.upload_file(destination, temp_dest)
                    os.remove(temp_dest)
