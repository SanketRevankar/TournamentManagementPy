import datetime
import json
import os
from ftplib import FTP

from google.cloud import storage
from google.cloud.storage import Blob


def get_logs_from_ftp(request):
    """
    Download Match Logs from FTP Server and Save them to Cloud Storage

    :param request: Http Request Object
    """

    request_json = json.loads(request.get_json(silent=True))

    score_starting_ = request_json['score_starting_']
    logs_starting_ = request_json['logs_starting_']
    folder = request_json['folder']
    results_ = request_json['results_']
    amxmodx_logs_ = request_json['amxmodx_logs_']
    cstrike_logs_ = request_json['cstrike_logs_']
    ip = request_json['ip']
    username = request_json['username']
    password = request_json['password']
    date = datetime.datetime.utcfromtimestamp(request_json['date'])

    folders = [
        [results_, score_starting_ + folder],
        [amxmodx_logs_, logs_starting_ + folder],
        [cstrike_logs_, logs_starting_ + folder],
    ]
    ftp = get_ftp_connection(ip, username, password)

    for c_folder in folders:
        for file in ftp.mlsd(c_folder[0]):
            if file[1]['type'] == 'dir' or (".log" not in file[0] and ".txt" not in file[0]):
                continue
            date_file = datetime.datetime.strptime(file[1]['modify'], "%Y%m%d%H%M%S")

            if date_file >= date:
                source = c_folder[0] + "/" + file[0]
                destination = c_folder[1] + "/" + file[0]
                temp_dest = '/tmp/' + file[0]
                download(ftp, source, temp_dest)
                upload_file(destination, temp_dest)
                os.remove(temp_dest)

    ftp.close()


def get_ftp_connection(ip, username, password):
    """
    Get a connection for server using IP, Username and Password

    :param ip: Server IP for connecting to FTP
    :param username: Username of FTP Server
    :param password: Password of FTP Server
    :return: ftp object
    """

    _old_makepasv = FTP.makepasv

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

    ftp = FTP()
    ftp.connect(ip, 21)
    ftp.login(username, password)
    ftp.set_pasv(True)

    return ftp


def download(ftp, source, destination):
    """
    Download file from FTP to local

    :param ftp: FTP connection var
    :param source: Source path - FTP location
    :param destination: Destination path - Temp Storage location
    """

    f = open(destination, 'wb')
    ftp.retrbinary("RETR " + source, f.write)


def upload_file(file_name, file_path):
    """
    Upload a file from local storage to bucket

    :param file_name: Name of the file to upload. (Should include path from bucket)
    :param file_path: Path of the file in local system
    """

    client = storage.Client()
    bucket_name = 'ncl'
    bucket = client.get_bucket(bucket_name)

    blob = Blob(file_name, bucket)
    with open(file_path, "rb") as my_file:
        blob.upload_from_file(my_file)
    log_it_storage(file_name, 'file')


def log_it_storage(location, file_type):
    """
    Log for storage finalize

    :param location: Path of the saved file
    :param file_type: Type of object uploaded [File or Dir]
    """
    log_ = {
        'location': location,
        'type': 'storage',
        'file_type': file_type
    }
    dumps = json.dumps(log_)
    print(dumps)
