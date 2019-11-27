import datetime
import json
import os
from ftplib import FTP

from google.cloud import storage
from google.cloud.storage import Blob


def get_hltv_demos_from_ftp(request):
    """
    Download HLTV Demos from FTP Server and Save them to Cloud Storage

    :param request: Http Request Object
    """

    request_json = json.loads(request.get_json(silent=True))

    locations_hltv_starting_ = request_json['locations_hltv_starting_']
    folder = request_json['folder']
    ip = request_json['ip']
    username = request_json['username']
    password = request_json['password']
    date = datetime.datetime.utcfromtimestamp(request_json['date'])

    ftp = get_ftp_connection(ip, username, password)

    for file in ftp.mlsd('cstrike'):
        if file[1]['type'] == 'dir' or ".dem" not in file[0]:
            continue
        date_file = datetime.datetime.strptime(file[1]['modify'], "%Y%m%d%H%M%S")

        if date_file >= date:
            source = 'cstrike/' + file[0]
            destination = locations_hltv_starting_ + folder + '/' + file[0]
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
    bucket_name = 'ncl_6'
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
