from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from TournamentManagementPy import handler
from constants import StringConstants as sC


@ensure_csrf_cookie
def welcome(request):
    # TODO: Remove (only for DEV)
    # request.session['id'] = 'JsKT2F8df7bLxCCCl6gK'
    # request.session["name"] = 'Sanket Revankar'
    # request.session["fb_id"] = '109850146536478'
    # request.session["steam_id"] = 'STEAM_1:0:102553381'
    # request.session["username"] = 'DarK PhoeniX'
    # request.session["avatar_url"] = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/8a' \
    #                                 '/8aaa3cd00b85b7622f13b0994eff2f42a2a66adf_full.jpg'
    # # request.session['team'] = 'JsKT2F8df7bLxCCCl6gK'
    # # request.session['join_team'] = []
    # request.session['steam_url_id'] = '76561198165372490'

    # request.session['id'] = 'hq4tpdiwF3njUDvYAlHa'
    # request.session["name"] = 'Sanket Revankar'
    # request.session["fb_id"] = '1849900058362481'
    # request.session["steam_id"] = 'STEAM_1:0:102553381'
    # request.session["username"] = 'DarK PhoeniX'
    # request.session["avatar_url"] = 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/ee/' \
    #                                 'ee5ec062fb9f7fa1d473a9b57de65ac24ee6830e_full.jpg'
    # request.session['join_team'] = ['JsKT2F8df7bLxCCCl6gK']
    # request.session['steam_url_id'] = '76561198010346671'
    # ---------------------------------------------------------------------------------------------------------------

    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_visit(request, __name__ + '.welcome')

    if 'team' in handler.dataHelper.get_player_data_by_id(request.session['id']):
        template = loader.get_template('Home/home.html')

        id_ = request.session['id']
        team_id = handler.dataHelper.get_team_id_by_player_id(id_)
        team_data = handler.dataHelper.get_team_data_by_id(team_id)

        context = {
            'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
            'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
            'name': request.session["name"],
            'fb_id': request.session["fb_id"],
            'avatar_url': request.session["avatar_url"],
            'steam_id': request.session["steam_id"],
            'steam_url_id': request.session["steam_url_id"],
            'username': request.session["username"],
            'team_id': team_id,
            'id': id_,
            'home': 'home',
            **team_data,
        }

        if team_id == id_:
            players = handler.fireStoreHelper.util.get_join_requests_by_team_id(team_id)
            join_requests = players.__len__() if players else 0
            context['join_requests'] = join_requests
            if join_requests > 0:
                player_data = handler.dataHelper.get_player_data_arr_by_id(players)
                context['players'] = player_data

        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('Home/TeamFormationHome.html')

        context = {
            'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
            'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
            'name': request.session["name"],
            'fb_id': request.session["fb_id"],
            'avatar_url': request.session["avatar_url"],
            'steam_id': request.session["steam_id"],
            'steam_url_id': request.session["steam_url_id"],
            'username': request.session["username"],
            'home': 'home',
        }

        return HttpResponse(template.render(context, request))
