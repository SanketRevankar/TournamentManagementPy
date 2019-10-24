import json
from datetime import datetime

from dateutil.tz import tz
from google.cloud import storage, firestore_v1
from google.cloud.storage import Blob


def log_manager(data_in, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    blob_name = data_in['name']
    print('File: {}'.format(blob_name))

    client = storage.Client()
    bucket = client.get_bucket(data_in['bucket'])
    blob = Blob(blob_name, bucket)

    db = firestore_v1.Client()

    if 'stdout' in blob_name:
        pages = {}
        for json_obj in blob.download_as_string().decode().strip().split('\n'):
            data = json.loads(json_obj)
            timestamp_ = data['timestamp']
            utc = datetime.strptime(timestamp_, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=tz.tzutc())
            local_time = utc.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S.%f')
            if 'jsonPayload' in data:
                if data['type'] == 'page':
                    requester_ = data['requester']
                    path_ = data['path']
                    ip_ = data['ip']
                    if path_ not in pages:
                        pages[path_] = {'total_visits': {'total_visits': 0}}
                    pages[path_]['total_visits']['total_visits'] += 1
                    if requester_ not in pages[path_]:
                        pages[path_][requester_] = {
                            'ips': set(ip_),
                            'visits': 1,
                        }
                    else:
                        # noinspection PyUnresolvedReferences
                        pages[path_][requester_]['ips'].add(ip_)
                        pages[path_][requester_]['visits'] += 1

        print(pages)