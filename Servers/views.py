from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def welcome(request):
    template = loader.get_template('Servers/servers.html')
    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME]
    }

    return HttpResponse(template.render(context, request))