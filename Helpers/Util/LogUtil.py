from TournamentManagementPy import handler
from constants import StringConstants as sC


class LogUtil:
    def __init__(self):
        self.META_AE_IP = 'HTTP_X_APPENGINE_USER_IP'
        self.FORWARDED_FOR = 'HTTP_X_FORWARDED_FOR'
        self.MODE = handler.config[sC.PROJECT_DETAILS][sC.MODE]

        print('{} - Initialized'.format(__name__))

    def get_ip(self, request):
        return request.META.get(self.META_AE_IP) \
            if self.META_AE_IP in request.META else request.META.get(self.FORWARDED_FOR)

    def player_details(self, player_id):
        if not player_id:
            return None, None
        player_data = handler.dataHelper.get_player_data_arr_by_id(player_id)
        name_ = player_data['name']
        username_ = player_data['username']

        return name_, username_
