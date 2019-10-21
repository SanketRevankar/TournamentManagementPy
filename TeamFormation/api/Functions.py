from django.http import HttpResponse
from google.cloud import firestore_v1

from TournamentManagementPy import handler


def accept_player(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.accept_player', target=target_id)
    handler.fireStoreHelper.accept_player(target_id, player_id)

    return HttpResponse('')


def ignore_player(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.ignore_player', target=target_id)
    handler.fireStoreHelper.ignore_player(target_id, player_id)

    return HttpResponse('')


def team_count(request):
    player_id = request.session['id']

    players = handler.fireStoreHelper.util.get_join_requests_by_team_id(player_id)
    join_requests = players.__len__()

    return HttpResponse(join_requests)


def remove_player(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.remove_player', target=target_id)

    handler.fireStoreHelper.leave_team(target_id)
    handler.fireStoreHelper.remove_player_from_team(player_id, target_id)

    return HttpResponse('')


def make_captain(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.make_captain', target=target_id)

    handler.fireStoreHelper.util.update_document(handler.fireStoreHelper.TEAMS, player_id, {'vice_captain': target_id})
    handler.adminHelper.add_admin(player_id)

    return HttpResponse('')


def remove_captain(request):
    player_id = request.session['id']
    target_id = request.POST['query']

    handler.authenticationHelper.validate_captain(player_id, request, target_id)
    handler.logHelper.log_it_api(request, __name__ + '.remove_captain', target=target_id)

    handler.fireStoreHelper.util.update_document(handler.fireStoreHelper.TEAMS, player_id,
                                            {'vice_captain': firestore_v1.DELETE_FIELD})
    handler.adminHelper.remove_admin(player_id)

    return HttpResponse('')


