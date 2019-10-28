from django.http import HttpResponseServerError

from helpers.Util.CloudServerUtil import CloudServerUtil
from constants import StringConstants as sC
from firestore_data.ServerData import ServerList


class CloudServerHelper:
    def __init__(self, config):
        """
        Initiate Cloud Server Helper
        This Class contains Cloud Server Functions

        :param config: Config object
        """

        self.util = CloudServerUtil(config)

        print('{} - Initialized'.format(__name__))

    def stop_server(self, server_id):
        """
        Used to stop a Compute Engine Instance. If already stopped no action will be taken.

        :param server_id: Id of the server
        """

        node_name = ServerList[server_id][sC.INSTANCE_NAME]

        node = self.util.get_node(node_name)
        server_status = self.util.status(node)

        if server_status == sC.RUNNING:
            if not self.util.stop(node):
                raise HttpResponseServerError

    def start_server(self, server_id):
        """
        Used to start a Compute Engine Instance. If already running no action will be taken.

        :param server_id: ID of the server
        :return: Instance variable which was started
        """
        node_name = ServerList[server_id][sC.INSTANCE_NAME]
        server_name = ServerList[server_id][sC.SERVER_NAME]

        node = self.util.get_node(node_name)
        server_status = self.util.status(node)

        if server_status == sC.STOPPED:
            if not self.util.start(node):
                raise HttpResponseServerError
            node = self.util.get_node(node_name)

        return self.util.ip(node) + sC.COLON + ServerList[server_id][sC.PORT], server_name
