import json

from Helpers.Util import LogUtil


class LogHelper:
    def __init__(self):
        self.util = LogUtil.LogUtil()

        print('{} - Initialized'.format(__name__))

    def log_it_visit(self, request, function_name, authorized=True):
        log_ = {
            'func': function_name,
            'path': request.META['PATH_INFO'],
            'ip': self.util.get_ip(request),
            'requester': request.session['id'],
            'type': 'page',
            'authorized': authorized,
        }
        dumps = json.dumps(log_)
        print(dumps)

    def log_it_api(self, request, function_name, target=None, authorized=True):
        log_ = {
            'func': function_name,
            'path': request.META['PATH_INFO'],
            'ip': self.util.get_ip(request),
            'requester': request.session['id'],
            'type': 'api',
            'target': target,
            'authorized': authorized,
        }
        dumps = json.dumps(log_)
        print(dumps)

    def log_it_query(self, query, status='Success'):
        log_ = {
            'query': query,
            'status': status,
            'type': 'query',
        }
        dumps = json.dumps(log_)
        print(dumps)

    def log_it_storage(self, location, file_type):
        log_ = {
            'location': location,
            'type': 'storage',
            'file_type': file_type
        }
        dumps = json.dumps(log_)
        print(dumps)

    def log_it_server(self, node, action):
        log_ = {
            'node': node,
            'action': action,
            'type': 'server',
        }
        dumps = json.dumps(log_)
        print(dumps)
