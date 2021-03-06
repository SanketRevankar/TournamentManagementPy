from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader

from TeamFormation.api.Functions import accept_player, team_count, ignore_player, remove_player, make_captain, \
    remove_captain
from TournamentManagementPy import handler
from constants import StringConstants as sC


def create_team(request):
    handler.authenticationHelper.validate_mode_9()
    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_visit(request, __name__ + '.create_team')

    if 'team' in handler.dataHelper.get_player_data_by_id(request.session['id']):
        raise PermissionDenied('Already in a team')

    template = loader.get_template('TeamFormation/create_team.html')
    context = {
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'Team_name_exists': '',
        'site_url': request.build_absolute_uri('/')[:-1].strip("/"),
    }

    if 'usr' in request.POST:
        team_id = request.POST['id_']
        team_name = request.POST['usr']
        team_tag = request.POST['tag']
        team_logo_url = request.POST['logo_url']

        player_id = request.session['id']
        status_name, status_tag, status_id = handler.fireStoreHelper.create_team(team_id, team_name, team_tag,
                                                                                 team_logo_url, player_id)

        if not status_name and not status_tag and not status_id:
            handler.adminHelper.add_admin(player_id)
            return redirect('/Home')

        context['team_id'] = team_id
        context['logo_url'] = team_logo_url
        context['team_name'] = team_name
        context['team_tag'] = team_tag

        if status_name is True:
            context['Team_name_exists'] = True
        if status_tag is True:
            context['Team_tag_exists'] = True
        if status_id is True:
            context['Team_id_exists'] = True

    return HttpResponse(template.render(context, request))


def manage_team(request):
    handler.authenticationHelper.validate_login(request)
    handler.authenticationHelper.validate_captain(request.session['id'], request, None)
    handler.logHelper.log_it_visit(request, __name__ + '.manage_team')

    template = loader.get_template('TeamFormation/manage_team.html')

    player_id = request.session['id']
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    team_data = handler.fireStoreHelper.util.fsh_get_team_data_by_id(team_id)
    players = handler.dataHelper.get_player_data_arr_by_id(team_data['players'])

    context = {
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        **team_data,
        'players': players,
        'players_count': players.__len__(),
        'id': request.session['id']
    }

    return HttpResponse(template.render(context, request))


def edit_team(request):
    handler.authenticationHelper.validate_mode_9()
    handler.authenticationHelper.validate_login(request)
    handler.authenticationHelper.validate_captain(request.session['id'], request, None)
    handler.logHelper.log_it_visit(request, __name__ + '.edit_team')

    template = loader.get_template('TeamFormation/edit_team.html')

    player_id = request.session['id']
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)
    team_data = handler.dataHelper.get_team_data_by_id(team_id)

    context = {
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        **team_data,
        'id': request.session['id']
    }

    if 'usr' in request.POST:
        team_name = request.POST['usr']
        team_tag = request.POST['tag']
        team_logo_url = request.POST['logo_url']

        handler.fireStoreHelper.update_team(team_name, team_tag, team_logo_url, team_id)
        return redirect('/Home')

    return HttpResponse(template.render(context, request))


def delete_team(request):
    handler.authenticationHelper.validate_mode_9()
    handler.authenticationHelper.validate_login(request)
    handler.authenticationHelper.validate_captain(request.session['id'], request, None)
    handler.logHelper.log_it_visit(request, __name__ + '.delete_team')

    player_id = request.session['id']
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)

    if not team_id:
        raise Http404

    if not handler.fireStoreHelper.delete_team(team_id, player_id):
        raise PermissionDenied

    handler.adminHelper.remove_admin(player_id)

    return redirect('/Home')


def join_team(request, team_id):
    handler.authenticationHelper.validate_mode_9()
    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_api(request, __name__ + '.join_team')

    player_id = request.session['id']
    handler.fireStoreHelper.join_team(player_id, team_id)

    return redirect('/Teams')


def leave_team(request):
    handler.authenticationHelper.validate_mode_9()
    handler.authenticationHelper.validate_login(request)

    player_id = request.session['id']
    team_id = handler.dataHelper.get_team_id_by_player_id(player_id)

    handler.logHelper.log_it_api(request, __name__ + '.leave_team', target=team_id)

    handler.fireStoreHelper.leave_team(player_id)
    handler.fireStoreHelper.remove_player_from_team(team_id, player_id)

    return redirect('/Home')


def api_handler(request, name):
    handler.authenticationHelper.validate_login(request)

    always_allowed = {
        'make_captain': make_captain,
        'remove_captain': remove_captain,
    }

    if name in always_allowed:
        return always_allowed[name](request)

    handler.authenticationHelper.validate_mode_9()

    api_names = {
        'accept_player': accept_player,
        'team_count': team_count,
        'ignore_player': ignore_player,
        'remove_player': remove_player,
    }

    if not name or name not in api_names:
        raise Http404

    return api_names[name](request)
