from google.cloud import firestore_v1
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


def ip_whitelist(request):
    steam_id = request.args.get('id')
    ip = request.args.get('ip')
    to_24_range = ip_to_24_range(ip)

    print(steam_id, ip)

    db = firestore_v1.Client()
    firewall_ref = db.collection('firewalls').document('instance_cs')
    allowed_ips = firewall_ref.get(['allowed_ips']).get('allowed_ips')
    if to_24_range in allowed_ips:
        print('IP is already Present: {}'.format(ip))
        return f'' + steam_id + "Accepted"

    firewall_ref.update({'allowed_ips': firestore_v1.ArrayUnion([to_24_range])})
    allowed_ips.append(to_24_range)

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = 'narco-gaming'
    firewall = 'allow-cs'

    firewall_body = {
        'sourceRanges': allowed_ips,
    }

    print(firewall_body)

    request = service.firewalls().patch(project=project, firewall=firewall, body=firewall_body)
    response = request.execute()

    print(response)

    return f'' + steam_id + "Accepted"


def ip_to_24_range(ip):
    ip_s = ip.split('.')

    return ip_s[0] + '.' + ip_s[1] + '.' + ip_s[2] + '.0/24'
