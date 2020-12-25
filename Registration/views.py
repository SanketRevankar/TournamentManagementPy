from datetime import datetime
from urllib import parse

import requests
import steam
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def welcome(request):
    template = loader.get_template('Registration/welcome.html')
    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME]
    }

    return HttpResponse(template.render(context, request))


def facebook(request):
    template = loader.get_template('Registration/facebook.html')
    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'fbId': handler.config[sC.PROJECT_DETAILS][sC.FACEBOOK_API_KEY],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME]
    }

    return HttpResponse(template.render(context, request))


def steam_login(request):
    name = request.POST["name"]
    email = request.POST["email"]
    fb_id = request.POST["id"]
    request.session["name"] = name
    request.session["fb_id"] = fb_id

    ip = request.META.get('HTTP_X_APPENGINE_USER_IP') if 'HTTP_X_APPENGINE_USER_IP' in request.META \
        else request.META.get('HTTP_X_FORWARDED_FOR')
    city = request.META.get('HTTP_X_APPENGINE_CITY') if 'HTTP_X_APPENGINE_CITY' in request.META else None
    location = request.META.get('HTTP_X_APPENGINE_CITYLATLONG') if 'HTTP_X_APPENGINE_CITYLATLONG' in request.META \
        else None

    request.session['id'], status, doc_data = handler.fireStoreHelper.facebook_login(name, email, fb_id,
                                                                                     datetime.utcnow(),
                                                                                     ip, city, location)

    if status is True:
        request.session["steam_id"] = doc_data['steam_id']
        request.session["username"] = doc_data['username']
        request.session["avatar_url"] = doc_data['avatar_url']
        request.session['steam_url_id'] = doc_data['steam_url_id']

        return redirect('/Home')

    origin = request.META['HTTP_ORIGIN']
    steam_openid_url = 'https://steamcommunity.com/openid/login'
    u = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': origin + '/Registration/steam_auth',
        'openid.realm': origin + '/Registration/',
    }
    query_string = parse.urlencode(u)
    auth_url = steam_openid_url + "?" + query_string
    return redirect(auth_url)


def steam_auth(request):
    steam_login_url_base = "https://steamcommunity.com/openid/login"

    params = {
        "openid.assoc_handle": request.GET.get("openid.assoc_handle"),
        "openid.sig": request.GET.get("openid.sig"),
        "openid.ns": request.GET.get("openid.ns"),
        "openid.mode": "check_authentication",
        'openid.signed': request.GET.get("openid.signed"),
        'openid.op_endpoint': request.GET.get("openid.op_endpoint"),
        'openid.claimed_id': request.GET.get("openid.claimed_id"),
        'openid.identity': request.GET.get("openid.identity"),
        'openid.return_to': request.GET.get("openid.return_to"),
        'openid.response_nonce': request.GET.get("openid.response_nonce"),
    }

    r = requests.post(steam_login_url_base, data=params)
    if "is_valid:true" in r.text:
        steam_url = request.GET.get("openid.claimed_id").split('/')[-1]

        api_url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/'
        api = handler.localDataHelper.steam_api_key

        r = requests.get(api_url + '?key={}&steamids={}'.format(api, steam_url))
        resp = r.json()

        steam_id = steam.steamid.SteamID(steam_url).as_steam2_zero
        username = resp['response']['players']['player'][0]['personaname']
        avatar_url = resp['response']['players']['player'][0]['avatarfull']

        if handler.fireStoreHelper.steam_login(steam_url, steam_id, username, avatar_url, request.session['id'],
                                               datetime.utcnow()):
            template = loader.get_template('Registration/steamid.html')
            context = {
                'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
                'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
                'username': username,
            }

            return HttpResponse(template.render(context, request))

        request.session["steam_id"] = steam_id
        request.session["username"] = username
        request.session["avatar_url"] = avatar_url
        request.session['steam_url_id'] = steam_url

        return redirect('/Home')

    return redirect('steam')
