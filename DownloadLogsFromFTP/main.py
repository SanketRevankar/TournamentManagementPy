import datetime
import json
import os
from ftplib import FTP

from google.cloud import storage
from google.cloud.storage import Blob


def get_logs_from_ftp(request):
    """
    Get log data from instance

    :param date: date for which the logs will be downloaded
    :param server_id: Id of the server
    :param folder: Destination folder
    """

    request_json = request.get_json(silent=True)

    score_starting_ = request_json['request_json']
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

            if date_file.astimezone() >= date:
                source = c_folder[0] + "/" + file[0]
                destination = c_folder[1] + "/" + file[0]
                temp_dest = '/tmp/' + file[0]
                download(ftp, source, temp_dest)
                upload_file(destination, temp_dest)
                os.remove(temp_dest)

    ftp.close()

def get_ftp_connection(ip, username, password):
    """
    Get a connection for server with server Id from ServerList
    """

    ftp = FTP()
    ftp.connect(ip, 21)
    ftp.login(username, password)
    ftp.set_pasv(False)

    return ftp


def download(ftp, src, des):
    """
    Download file from FTP to local

    :param ftp: FTP connection var
    :param src: Source path - Cloud
    :param des: Destination path - local
    """

    f = open(des, 'wb')
    ftp.retrbinary("RETR " + src, f.write)


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
    log_ = {
        'location': location,
        'type': 'storage',
        'file_type': file_type
    }
    dumps = json.dumps(log_)
    print(dumps)