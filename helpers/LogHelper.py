import json

from helpers.Util import LogUtil


class LogHelper:
    def __init__(self):
        """
        Initialize the Log Helper
        This Class contains Log related Functions

        """

        self.util = LogUtil.LogUtil()

        print('{} - Initialized'.format(__name__))

    def log_it_visit(self, request, function_name, authorized=True):
        """
        Logs page visits

        :param request: Http Request Object
        :param function_name: Name of the function which logged this
        :param authorized: Is this request Authorized
        """

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
        """
        Logs Api Function calls

        :param request: Http Request Object
        :param function_name: Name of the function which logged this
        :param target: Targeted Id for some functions
        :param authorized: Is this request Authorized
        """

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

    @staticmethod
    def log_it_query(query, status='Success'):
        """
        Log MySQL Queries

        :param query: MySQL Query that was fired
        :param status: Query status
        """

        log_ = {
            'query': query,
            'status': status,
            'type': 'query',
        }
        dumps = json.dumps(log_)
        print(dumps)

    @staticmethod
    def log_it_storage(location, file_type):
        """
        Log Cloud Storage Operations

        :param location: Path where storage operation was performed
        :param file_type: Type of the file added ie. File or directory
        """

        log_ = {
            'location': location,
            'type': 'storage',
            'file_type': file_type
        }
        dumps = json.dumps(log_)
        print(dumps)

    @staticmethod
    def log_it_server(node, action):
        """
        Log Cloud Server Operations

        :param node: Server not on which action was taken
        :param action: Action performed
        """

        log_ = {
            'node': node,
            'action': action,
            'type': 'server',
        }
        dumps = json.dumps(log_)
        print(dumps)
