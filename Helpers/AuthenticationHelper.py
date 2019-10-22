from django.core.exceptions import PermissionDenied

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data.PlayerData import PlayerList


class AuthenticationHelper:
    def __init__(self):
        self.mode9 = handler.config[sC.PROJECT_DETAILS][sC.MODE] == '9'

    def validate_login(self, request):
        if 'id' not in request.session:
            raise PermissionDenied

        if self.mode9:
            if 'team' not in PlayerList[request.session['id']]:
                raise PermissionDenied

    def validate_admin(self, request):
        self.validate_login(request)

        if request.session['id'] not in eval(handler.config[sC.PROJECT_DETAILS][sC.ADMIN_IDS]):
            handler.logHelper.log_it_visit(request, __name__ + '.validate_admin', authorized=False)
            raise PermissionDenied

    def validate_captain(self, player_id, request, target_id):
        if player_id != handler.dataHelper.get_team_id_by_player_id(player_id):
            handler.logHelper.log_it_api(request, __name__ + '.validate_captain', target=target_id, authorized=False)
            raise PermissionDenied

    def validate_mode_9(self):
        if self.mode9:
            raise PermissionDenied
