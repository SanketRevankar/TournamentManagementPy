import json

from google.cloud import storage, firestore_v1
from google.cloud.storage import Blob


# noinspection DuplicatedCode
def log_manager(data_in, _):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    :param data_in: The Cloud Functions event payload.
    :param _: The Cloud Functions event payload.
    """

    blob_name = data_in['name']
    print('File: {}'.format(blob_name))

    client = storage.Client()
    bucket = client.get_bucket(data_in['bucket'])
    blob = Blob(blob_name, bucket)

    db = firestore_v1.Client()

    for json_obj in blob.download_as_string().decode().strip().split('\n'):
        data = json.loads(json_obj)
        timestamp_ = data['timestamp']

        if 'jsonPayload' in data:
            payload_ = data['jsonPayload']

            if payload_['type'] == 'page':
                requester_ = payload_['requester']
                path_ = payload_['path']

                if not payload_['authorized']:
                    doc_ref = db.collection('unauthorized_requests').document(path_.replace('/', '_'))
                    doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)
                    continue

                doc_ref = db.collection('page_requests').document(path_.replace('/', '_'))
                doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)

            elif payload_['type'] == 'api':
                requester_ = payload_['requester']
                path_ = payload_['path']

                if not payload_['authorized']:
                    doc_ref = db.collection('unauthorized_requests').document(path_.replace('/', '_'))
                    doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)
                    continue

                doc_ref = db.collection('api_requests').document(path_.replace('/', '_'))
                doc_ref.set({requester_: {timestamp_: {**payload_}}}, merge=True)

            elif payload_['type'] == 'query':
                doc_ref = db.collection('queries_mysql').document()
                doc_ref.create({'datetime': timestamp_, **payload_})

            elif payload_['type'] == 'storage':
                doc_ref = db.collection('storage_operations').document()
                doc_ref.create({'datetime': timestamp_, **payload_})

            elif payload_['type'] == 'server':
                doc_ref = db.collection('server_operations').document(payload_['node'])
                doc_ref.set({payload_['action']: {timestamp_: {**payload_}}}, merge=True)
