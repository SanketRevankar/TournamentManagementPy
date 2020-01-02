from django.http import HttpResponse
from google.cloud import firestore_v1

from TournamentManagementPy import handler


def accept_player(request):
    player_id = request.session['id']
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.accept_player', target=target_id)
    handler.fireStoreHelper.accept_player(target_id, team_id)

    return HttpResponse('')


def ignore_player(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.ignore_player', target=target_id)
    handler.fireStoreHelper.ignore_player(target_id, team_id)

    return HttpResponse('')


def team_count(request):
    player_id = request.session['id']

    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    players = handler.fireStoreHelper.util.get_join_requests_by_team_id(team_id)
    join_requests = players.__len__()

    return HttpResponse(join_requests)


def remove_player(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.remove_player', target=target_id)

    handler.fireStoreHelper.leave_team(target_id)
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    handler.fireStoreHelper.remove_player_from_team(team_id, target_id)

    return HttpResponse('')


def make_captain(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)

    handler.logHelper.log_it_api(request, __name__ + '.make_captain', target=target_id)
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    handler.fireStoreHelper.util.update_document(handler.fireStoreHelper.util.TEAMS, team_id, {'vice_captain': target_id})
    handler.adminHelper.add_admin(target_id)

    return HttpResponse('')


def remove_captain(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.remove_captain', target=target_id)

    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    handler.fireStoreHelper.util.update_document(handler.fireStoreHelper.util.TEAMS, team_id,
                                            {'vice_captain': firestore_v1.DELETE_FIELD})
    handler.adminHelper.remove_admin(target_id)

    return HttpResponse('')
