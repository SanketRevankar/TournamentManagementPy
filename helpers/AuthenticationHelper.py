from django.core.exceptions import PermissionDenied

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data.PlayerData import PlayerList


class AuthenticationHelper:
    def __init__(self, config):
        """
        Initiate Authentication Helper
        This Class contains functions for helping with Authentication

        :param config: Config object
        """

        self.mode9 = config[sC.PROJECT_DETAILS][sC.MODE] == '9'
        self.admins = eval(handler.config[sC.PROJECT_DETAILS][sC.ADMIN_IDS])

    def validate_login(self, request):
        """
        Validate Login for given Request, checking Http session object for id

        :param request: Http Request Object
        """

        if 'id' not in request.session or 'steam_id' not in request.session:
            raise PermissionDenied('You need to login')

        if self.mode9:
            if 'team' not in PlayerList[request.session['id']]:
                raise PermissionDenied('Player is not in a team!')

    def validate_admin(self, request):
        """
        Validate Admin Login for given Request, checking Http session id in Admin ids in config

        :param request: Http Request Object
        """

        self.validate_login(request)

        if request.session['id'] not in self.admins:
            handler.logHelper.log_it_visit(request, __name__ + '.validate_admin', authorized=False)
            raise PermissionDenied('You need to be an admin to access this page.')

    @staticmethod
    def validate_captain(player_id, request, target_id):
        """
        Check if Id of the player is same as Id of the Captain

        :param player_id: Id of the Player
        :param request: Http Request Object
        :param target_id: Id of the Target Player
        """

        team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
        team_data = handler.dataHelper.get_team_data_by_id(team_id)

        if not team_data:
            raise PermissionDenied('Only captains can access this function.')

        if player_id != team_data['captain'] and player_id != team_data.get('vice_captain'):
            handler.logHelper.log_it_api(request, __name__ + '.validate_captain', target=target_id, authorized=False)
            raise PermissionDenied('Only captains can modify their team.')

    def validate_mode_9(self):
        """
        Disable some apps if Mode is 9

        """

        if self.mode9:
            raise PermissionDenied('You cannot access this now!')
