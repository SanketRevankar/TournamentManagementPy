from google.cloud import storage
from google.cloud.storage import Blob

from TournamentManagementPy import handler
from constants import StringConstants as sC


class CloudStorageHelper:
    def __init__(self, config):
        """
        Initialize the Cloud Storage Helper
        This Class contains Cloud Storage Functions

        :param config: Config Object
        """

        self.client = storage.Client()
        self.bucket_name = config[sC.BUCKET_LOCATIONS][sC.FILES_HOME]
        self.bucket = self.client.get_bucket(self.bucket_name)

        print('{} - Initialized'.format(__name__))

    def create_folder(self, folder):
        """
        Creates a folder in the bucket

        :param folder: Path of the folder to create
        :return: None
        """

        blob = Blob(folder, self.bucket)
        if blob.exists(self.client):
            return
        blob.upload_from_string('')
        handler.logHelper.log_it_storage(folder, 'dir')

    def upload_file(self, file_name, file_path, public=False):
        """
        Upload a file from local storage to bucket

        :param file_name: Name of the file to upload. (Should include path from bucket)
        :param file_path: Path of the file in local system
        """

        blob = Blob(file_name, self.bucket)
        with open(file_path, "rb") as my_file:
            blob.upload_from_file(my_file)
            if public:
                blob.make_public()
        handler.logHelper.log_it_storage(file_name, 'file')

    def get_blobs_by_prefix(self, prefix):
        """
        Get Blob List by path prefix

        :param prefix: Prefix of path
        :return: Blob List
        """

        return self.bucket.list_blobs(prefix=prefix)

    def get_blob_with_path(self, path):
        """
        Get Blob using given path

        :param path: Path
        :return: Blob
        """

        return Blob(path, self.bucket)
