import json

from google.cloud import storage, firestore_v1
from google.cloud.storage import Blob


# noinspection DuplicatedCode
# FireStore Collection names for storing logs
UNAUTHORIZED_REQUESTS = 'unauthorized_requests'
SERVER_OPERATIONS = 'server_operations'
STORAGE_OPERATIONS = 'storage_operations'
QUERIES_MYSQL = 'queries_mysql'
API_REQUESTS = 'api_requests'
PAGE_REQUESTS = 'page_requests'

# Log Types
SERVER = 'server'
STORAGE = 'storage'
QUERY = 'query'
PAGE = 'page'

# Datetime values for Queries and Storage log types
DATETIME = 'datetime'

# JsonPayLoad Dict Keys
AUTHORIZED = 'authorized'
ACTION = 'action'
NODE = 'node'
API = 'api'
PATH = 'path'
REQUESTER = 'requester'
TYPE = 'type'

# Data event keys for input to function
NAME = 'name'
BUCKET = 'bucket'

# Json Log keys for each log
TIMESTAMP = 'timestamp'
JSONPAYLOAD = 'jsonPayload'


def log_manager(data_in, _):
    """
    Background Cloud Function to be triggered by Cloud Storage.
    This function parses logs and saves relevant data to FireStore.

    :param data_in: The Cloud Functions event payload.
    :param _: The Cloud Functions context. [Not Used here]
    """

    db = firestore_v1.Client()
    client = storage.Client()

    # Get path of the log file saved in storage
    blob_name = data_in[NAME]
    # Get bucket name
    bucket = client.get_bucket(data_in[BUCKET])
    print('File: {}'.format(blob_name))

    # Get Blob Object of the log file
    blob = Blob(blob_name, bucket)

    # For each line in log file
    for json_obj in blob.download_as_string().decode().strip().split('\n'):
        data = json.loads(json_obj)
        timestamp_ = data[TIMESTAMP]

        # Only Parsing Json Type logs, ignoring rest.
        if JSONPAYLOAD in data:
            payload_ = data[JSONPAYLOAD]

            # Parse Page Visits
            if payload_[TYPE] == PAGE:
                requester_ = payload_[REQUESTER]
                path_ = payload_[PATH]

                if check_unauthorized(db, path_, payload_, requester_, timestamp_):
                    continue

                doc_ref = db.collection(PAGE_REQUESTS).document(get_clean_path(path_))
                doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)

            # Parse Api Calls
            elif payload_[TYPE] == API:
                requester_ = payload_[REQUESTER]
                path_ = payload_[PATH]

                if check_unauthorized(db, path_, payload_, requester_, timestamp_):
                    continue

                doc_ref = db.collection(API_REQUESTS).document(get_clean_path(path_))
                doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)

            # Parse MySQL DB Queries
            elif payload_[TYPE] == QUERY:
                doc_ref = db.collection(QUERIES_MYSQL).document()
                doc_ref.create({DATETIME: timestamp_, **payload_})

            # Parse Cloud Storage operations
            elif payload_[TYPE] == STORAGE:
                doc_ref = db.collection(STORAGE_OPERATIONS).document()
                doc_ref.create({DATETIME: timestamp_, **payload_})

            # Parse Cloud Compute Engine Server Operations
            elif payload_[TYPE] == SERVER:
                doc_ref = db.collection(SERVER_OPERATIONS).document(payload_[NODE])
                doc_ref.set({payload_[ACTION]: {timestamp_: {**payload_}}}, merge=True)


def check_unauthorized(db, path_, payload_, requester_, timestamp_):
    """
    Validate Authorization of client and log if not authorized

    :param db: FireStore Client Object
    :param path_: Path of the Url which caused this log
    :param payload_: Original log payload
    :param requester_: Id of the player who visited the path
    :param timestamp_: Time of the log
    :return:
    """
    if not payload_[AUTHORIZED]:
        doc_ref = db.collection(UNAUTHORIZED_REQUESTS).document(get_clean_path(path_))
        doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)
        return True
    return False


def get_clean_path(path_):
    """
    Changing '/' to '_' as '/' causes FireStore to think it as a path.

    :param path_: Actual Path which was logged
    :return: FireStore safe logs
    """
    return path_.replace('/', '_')
