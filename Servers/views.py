import urllib.request

from django.http import HttpResponse
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def welcome(request):
    template = loader.get_template('Servers/servers.html')
    origin = request.build_absolute_uri('/')[:-1].strip("/")

    servers = handler.fireStoreHelper.util.get_game_servers()
    admin_check = handler.fireStoreHelper.util.check_game_server_admin(request.session['steam_id'])
    approver = handler.dataHelper.check_admin_approver(request.session['id'])

    server_data = []
    for server in servers:
        del servers[server]['admins']
        del servers[server]['admin_requests']

        q_url = origin + '/Servers/api/v1/get/server_data?ip={}&port={}'.format(servers[server]['ip'],
                                                                                    servers[server]['port'])
        contents = urllib.request.urlopen(q_url).read()
        decoded_contents = eval(contents.decode())

        if decoded_contents['status'] == '200':
            server_data.append([
                decoded_contents['server_name'],
                decoded_contents['players_online'],
                decoded_contents['player_data'],
                decoded_contents['map'],
                servers[server]['ip'],
                servers[server]['port'],
                server,
                decoded_contents['game'],
                decoded_contents['player_count'],
                admin_check[server],
            ])

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'servers': server_data,
        'logged_in': 'id' in request.session,
        'name': request.session['name'] if 'name' in request.session else None,
        'username': request.session['username'] if 'username' in request.session else None,
        'steam_id': request.session['steam_id'] if 'steam_id' in request.session else None,
        'approver': approver,
    }

    return HttpResponse(template.render(context, request))


def requests(request):
    handler.authenticationHelper.validate_approver(request)

    template = loader.get_template('Servers/admin_requests.html')
    origin = request.build_absolute_uri('/')[:-1].strip("/")

    servers = handler.fireStoreHelper.util.get_game_servers()

    server_data = []
    for server in servers:
        del servers[server]['admins']

        q_url = origin + '/Servers/api/v1/get/server_data?ip={}&port={}'.format(servers[server]['ip'],
                                                                                    servers[server]['port'])
        contents = urllib.request.urlopen(q_url).read()
        decoded_contents = eval(contents.decode())

        if decoded_contents['status'] == '200':
            requests = []
            for req in servers[server]['admin_requests']:
                requests.append([req, servers[server]['admin_requests'][req]['playerName'],
                                 servers[server]['admin_requests'][req]['playerNick'],
                                 servers[server]['admin_requests'][req]['playerExp'],
                                 servers[server]['admin_requests'][req]['adminOnOtherSv'],
                                 ])

            server_data.append([
                decoded_contents['server_name'],
                decoded_contents['players_online'],
                requests,
                server,
            ])

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'servers_': server_data,
    }

    return HttpResponse(template.render(context, request))


def admins(request, server_id):
    handler.authenticationHelper.validate_approver(request)

    template = loader.get_template('Servers/admins.html')
    origin = request.build_absolute_uri('/')[:-1].strip("/")
    access_types = {
        'basic': 'Basic Admin',
        'elite': 'Elite Admin',
        'manager': 'Manager',
        'owner': 'Owner',
        'fullAccess': 'Full Access',
    }

    admins = handler.fireStoreHelper.util.get_admins_by_server_id(server_id)['admins']
    server_data = handler.fireStoreHelper.util.get_server_data_by_id(server_id)

    q_url = origin + '/Servers/api/v1/get/server_data?ip={}&port={}'.format(server_data['ip'], server_data['port'])
    contents = urllib.request.urlopen(q_url).read()
    decoded_contents = eval(contents.decode())

    admin_data = []
    for admin in admins:
        admin_data.append([
            admin,
            admins[admin]['grantedOn'],
            admins[admin]['playerNick'],
            admins[admin]['playerName'],
            admins[admin]['playerFbUrl'],
            admins[admin]['grantedBy'],
            access_types[admins[admin]['access']],
        ])

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'admin_data': admin_data,
        'server_name': decoded_contents['server_name'],
        'server_id': server_id,
    }

    return HttpResponse(template.render(context, request))