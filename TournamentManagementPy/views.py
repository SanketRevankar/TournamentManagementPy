from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def home(request):
    return redirect('Registration/')


def logout(request):
    request.session.clear()

    return redirect('/Registration')


def me(request):
    print(dict(request.session.items()))
    handler.authenticationHelper.validate_login(request)
    template = loader.get_template('me.html')

    context = {
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'player_id': request.session['id'],
        'name': request.session['name'],
    }

    if 'steam_id' in request.session:
        context.update({
            'username': request.session['username'],
            'steam_id': request.session['steam_id']
        })

    return HttpResponse(template.render(context, request))
