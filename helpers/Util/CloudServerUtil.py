from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from TournamentManagementPy import handler
from constants import StringConstants as sC, PrintStrings as pS


class CloudServerUtil:
    def __init__(self, config):
        """
        Initiate Cloud Server Util.
        This Class contains utilities for helping with Cloud Server operations

        :param config: Config object
        """

        self.ComputeEngine = get_driver(Provider.GCE)
        # self.gc = self.ComputeEngine('', '', project=config[sC.PROJECT_DETAILS][sC.PROJECT_ID])

        self.gc = self.ComputeEngine(config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_EMAIL],
                                     config[sC.PROJECT_DETAILS][sC.SERVICE_ACCOUNT_KEY_PATH],
                                     project=config[sC.PROJECT_DETAILS][sC.PROJECT_ID])

        print('{} - Initialized'.format(__name__))

    @staticmethod
    def status(node):
        """
        Used to get Status a server.

        :param node: Node Object
        :return: Status of the server
        """

        return node.state

    def start(self, node):
        """
        Start a node. This is only possible if the node is stopped.

        :param node: Node Object
        :return: Server start success status
        """

        handler.logHelper.log_it_server(node.name, sC.SERVER_STATUS_START)
        return self.gc.ex_start_node(node) if self.status(node) == sC.STOPPED else pS.ALREADY_RUNNING

    def stop(self, node):
        """
        Stop a node. This is only possible if the node is started.

        :param node: Node Object
        :return: Server stop success status
        """

        handler.logHelper.log_it_server(node.name, sC.SERVER_STATUS_STOP)
        return self.gc.ex_stop_node(node) if self.status(node) == sC.RUNNING else pS.ALREADY_STOPPED

    def ip(self, node):
        """
        IP of a node. This is only possible if the node is started.

        :param node: Node Object
        :return: Server IP
        """

        return node.public_ips[0] if self.status(node) == sC.RUNNING else pS.SERVER_TO_GET_IP

    def get_node(self, node_name):
        """
        Get node by given node name.

        :type node_name: String
        :param node_name: Name of the node
        :return: node object
        """

        return self.gc.ex_get_node(node_name)
