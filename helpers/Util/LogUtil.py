class LogUtil:
    def __init__(self):
        """
        Initiate Log Util.
        This Class contains utilities for helping with Logging

        """

        self.META_AE_IP = 'HTTP_X_APPENGINE_USER_IP'
        self.FORWARDED_FOR = 'HTTP_X_FORWARDED_FOR'

        print('{} - Initialized'.format(__name__))

    def get_ip(self, request):
        """
        Get Ip from request

        :param request: Http Request Object
        :return: Ip of the player connected
        """

        return request.META.get(self.META_AE_IP) \
            if self.META_AE_IP in request.META else request.META.get(self.FORWARDED_FOR)
