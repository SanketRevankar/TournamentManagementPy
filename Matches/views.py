from datetime import timedelta, timezone

from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader

from TournamentManagementPy import handler
from constants import StringConstants as sC


def welcome(request):
    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_visit(request, __name__ + '.welcome')

    template = loader.get_template('Matches/matches.html')

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'matches': 'matches',
        'sidebar': True,
    }

    return HttpResponse(template.render(context, request))


def match_details(request, match_id=None):
    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_visit(request, __name__ + '.match_details')

    template = loader.get_template('Matches/match.html')

    context = {
        'mode': handler.config[sC.PROJECT_DETAILS][sC.MODE],
        'SITE_NAME': handler.config[sC.PROJECT_DETAILS][sC.DISPLAY_NAME],
        'match_id': match_id,
        'match': 'match',
    }

    return HttpResponse(template.render(context, request))


def get_matches(request):
    handler.authenticationHelper.validate_login(request)
    handler.logHelper.log_it_api(request, __name__ + '.get_matches')

    statuses = {
        'Started': {
            'id': 'Ongoing',
            'fa': 'fas fa-circle-notch',
        },
        'Created': {
            'id': 'Upcoming',
            'fa': 'fas fa-chevron-up',
        },
        'Completed': {
            'id': 'Completed',
            'fa': 'fas fa-check-double',
        },
    }

    match_data = ''
    match_data_2 = ''

    for status in statuses:
        matches = handler.fireStoreHelper.util.get_matches(status)

        match_data += '<h1 class="h2" id="{}" style="padding-bottom: 1%; border-bottom: 2px solid black;">' \
                      '<i class="{}"></i> {}</h1>'.format(statuses[status]['id'].lower(), statuses[status]['fa'],
                                                          statuses[status]['id'])
        if matches.__len__() < 1:
            match_data += 'No matches found'
            continue

        sorted_matches = list(map(int, matches.keys()))
        sorted_matches.sort()

        for match_id in sorted_matches:
            match = str(match_id)
            team_1 = matches[match]['team_1']
            team_2 = matches[match]['team_2']
            team_1_data = handler.dataHelper.get_team_data_by_id(team_1)
            team_2_data = handler.dataHelper.get_team_data_by_id(team_2)

            match_data_1 = """
<div class="card mb-3 text-center">
    <div class="row no-gutters">
        <div class="col-md-2">
            <img src="{}" class="card-img" alt="" style="border-radius: 0;">
            <div class="card-header bg-dark border-dark text-light">{} ({})</div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-6">
            <div class="card-body">
                <h3 class="card-title" style="border-bottom: 1px solid black;padding-bottom: 1%;font-weight: 600;
                color: #343a40;"><a href='#' class='fas fa-link text-dark text-decoration-none' id='{}' title='Click to copy link!'></a>
                <a href="{}" class='text-dark'> Match #{} {} vs {}</a></h3>
                <script>
                    $('#{}').click(function() {{
                        var textArea = document.createElement("textarea");
                        textArea.value = '{}';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                    }});
                </script>
                """. \
                format(team_1_data['team_logo_url'], team_1_data['team_name'], team_1_data['team_tag'], match, match,
                       match, team_1_data['team_name'], team_2_data['team_name'], match,
                       request.get_raw_uri().split('api')[0] + match)

            if status == 'Completed':
                match_data_2 = """
 <table class="w-50 table-striped table-hover table-bordered" style="margin: 2% auto;">
    <thead><tr><th>Map</th><th>Score</th></tr></thead>
    <tbody>"""
                for i in range(1, 6):
                    if 'map_{}'.format(i) in matches[match]:
                        match_data_2 += '<tr><td>{}</td><td>{}</td></tr>'. \
                            format(matches[match]['map_{}'.format(i)]['name'],
                                   matches[match]['map_{}'.format(i)]['score'])

                match_data_2 += """</tbody>
</table>
<h3 class="card-text" style="font-weight: 600;color: #343a40;">Team Sanket Victory</h3>
"""
            elif status == 'Created':
                match_data_2 = """<h5>Match Scheduled on: {}</h5>
<div class="countdown pt-2 pb-1 w-75" id="countdown_{}" style="margin: auto;">
    <div class='tiles' id='tiles_{}'></div>
    <div class="labels">
        <li>Days</li>
        <li>Hours</li>
        <li>Mins</li>
        <li>Secs</li>
    </div>
</div>
<script>
var target_date_{} = '{}';

var countdown_{} = document.getElementById("tiles_{}");
setInterval(function () {{ getCountdown_{}(); }}, 1000);

function getCountdown_{}(){{

    // find the amount of "seconds" between now and target
    var current_date = new Date().getTime();
    var days, hours, minutes, seconds;
    var seconds_left = (target_date_{} - current_date) / 1000;
    
    days = pad( parseInt(seconds_left / 86400) );
    seconds_left = seconds_left % 86400;
         
    hours = pad( parseInt(seconds_left / 3600) );
    seconds_left = seconds_left % 3600;
          
    minutes = pad( parseInt(seconds_left / 60) );
    seconds = pad( parseInt( seconds_left % 60 ) );
    
    // format countdown string + set tag value
    countdown_{}.innerHTML = 
        "<span>" + days + "</span><span>" + hours + "</span><span>" + minutes + "</span><span>" + seconds + "</span>"; 
}}

function pad(n) {{
    return (n < 10 ? '0' : '') + n;
}}

</script>
<a class="btn btn-dark mt-2" href="{}" target="_blank" rel="nofollow">Add to my calendar</a>
""".format(matches[match]['match_time'].replace(tzinfo=timezone.utc).astimezone(tz=None), match, match, match,
           matches[match]['match_time'].timestamp() * 1000, match, match, match, match, match, match,
           """https://www.google.com/calendar/render?action=TEMPLATE&text=Match+{}+{}+vs+{}&dates={}/{}&details={}&sf=true&output=xml""".
           format(match.zfill(2), team_1_data['team_name'], team_2_data['team_name'],
                  matches[match]['match_time'].strftime('%Y%m%dT%H%M00Z'),
                  (matches[match]['match_time'] + timedelta(hours=4)).strftime('%Y%m%dT%H%M00Z'),
                  'Match Link: {}'.format(request.get_raw_uri().split('api')[0] + match)).replace(' ', '+'))
            elif status == 'Started':
                match_data_2 = '<div>'
                id_ = request.session['id']
                in_team = id_ in team_1_data['players'] or id_ in team_2_data['players']
                if in_team:
                    match_data_2 += "<h5 class='mt-5'>Match Server: {}</h5><h5>HLTV Server: {}</h5>".format(
                        matches[match]['match_external_ip'], matches[match]['hltv_external_ip'])
                else:
                    match_data_2 += "<h5 class='mt-5'>HLTV Server: {}</h5>".format(matches[match]['hltv_external_ip'])
                if in_team:
                    match_data_2 += "<a href='steam://connect/{}' class='btn btn-primary mt-3 text-light mr-3'>" \
                                    "Join Match</a>".format(matches[match]['match_external_ip'])
                match_data_2 += "<a href='steam://connect/{}' class='btn btn-primary mt-3 text-light'>" \
                                "Join HLTV</a></div>".format(matches[match]['hltv_external_ip'])

            match_data_3 = """</div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-2">
            <img src="{}"
                 class="card-img" alt="" style="border-radius: 0;">
            <div class="card-header bg-dark border-dark text-light">{} ({})</div>
        </div>
    </div>
</div>""".format(team_2_data['team_logo_url'], team_2_data['team_name'],
                 team_2_data['team_tag'])

            match_data += match_data_1 + match_data_2 + match_data_3

    return JsonResponse({'match_data': match_data})


def get_match_data(request, match_id=None):
    if match_id is None:
        raise Http404

    handler.logHelper.log_it_api(request, __name__ + '.get_match_data')

    statuses = {
        'Started': {
            'id': 'Ongoing',
            'fa': 'fas fa-circle-notch',
        },
        'Created': {
            'id': 'Upcoming',
            'fa': 'fas fa-chevron-up',
        },
        'Completed': {
            'id': 'Completed',
            'fa': 'fas fa-check-double',
        },
    }

    match_details_ = handler.fireStoreHelper.util.get_match_data_by_id(str(int(match_id)))
    if match_details_ is None:
        raise Http404

    status = match_details_['status']

    match_data = '<h1 class="h2" id="{}" style="padding-bottom: 1%; border-bottom: 2px solid black;">' \
                  '<i class="{}"></i> {}</h1>'.format(statuses[status]['id'].lower(), statuses[status]['fa'],
                                                      statuses[status]['id'])

    team_1 = match_details_['team_1']
    team_2 = match_details_['team_2']
    team_1_data = handler.dataHelper.get_team_data_by_id(team_1)
    team_2_data = handler.dataHelper.get_team_data_by_id(team_2)

    match_data_1 = """
    <div class="card text-center" style="border-bottom: none;">
        <div class="row no-gutters">
            <div class="col-md-2">
                <img src="{}" class="card-img" alt="" style="border-radius: 0;">
                <div class="card-header bg-dark border-dark text-light">{} ({})</div>
            </div>
            <div class="col-md-1"></div>
            <div class="col-md-6">
                <div class="card-body">
                    <h3 class="card-title" style="border-bottom: 1px solid black;padding-bottom: 1%;font-weight: 600;
                    color: #343a40;"><a href='#' class='fas fa-link text-dark text-decoration-none' id='{}' title='Click to copy link!'></a>
                    <a href="{}" class='text-dark'> Match #{} {} vs {}</a></h3>
                    <script>
                        $('#{}').click(function() {{
                            var textArea = document.createElement("textarea");
                            textArea.value = '{}';
                            document.body.appendChild(textArea);
                            textArea.focus();
                            textArea.select();
                            document.execCommand('copy');
                            document.body.removeChild(textArea);
                        }});
                    </script>
                    """. \
        format(team_1_data['team_logo_url'], team_1_data['team_name'], team_1_data['team_tag'], match_id, match_id,
               match_id, team_1_data['team_name'], team_2_data['team_name'], match_id,
               request.get_raw_uri().split('api')[0] + match_id)

    match_data_2 = ''
    if status == 'Completed':
        match_data_2 = """
     <table class="w-50 table-striped table-hover table-bordered" style="margin: 2% auto;">
        <thead><tr><th>Map</th><th>Score</th></tr></thead>
        <tbody>"""
        for i in range(1, 6):
            if 'map_{}'.format(i) in match_details_:
                match_data_2 += '<tr><td>{}</td><td>{}</td></tr>'. \
                    format(match_details_['map_{}'.format(i)]['name'],
                           match_details_['map_{}'.format(i)]['score'])

        match_data_2 += """</tbody>
    </table>
    <h3 class="card-text" style="font-weight: 600;color: #343a40;">Team Sanket Victory</h3>
    """
    elif status == 'Created':
        match_data_2 = """<h5>Match Scheduled on: {}</h5>
    <div class="countdown pt-2 pb-1 w-75" id="countdown_{}" style="margin: auto;">
        <div class='tiles' id='tiles_{}'></div>
        <div class="labels">
            <li>Days</li>
            <li>Hours</li>
            <li>Mins</li>
            <li>Secs</li>
        </div>
    </div>
    <script>
    var target_date_{} = '{}';

    var countdown_{} = document.getElementById("tiles_{}");
    setInterval(function () {{ getCountdown_{}(); }}, 1000);

    function getCountdown_{}(){{

    	// find the amount of "seconds" between now and target
    	var current_date = new Date().getTime();
        var days, hours, minutes, seconds;
    	var seconds_left = (target_date_{} - current_date) / 1000;

    	days = pad( parseInt(seconds_left / 86400) );
    	seconds_left = seconds_left % 86400;

    	hours = pad( parseInt(seconds_left / 3600) );
    	seconds_left = seconds_left % 3600;

    	minutes = pad( parseInt(seconds_left / 60) );
    	seconds = pad( parseInt( seconds_left % 60 ) );

    	// format countdown string + set tag value
    	countdown_{}.innerHTML = "<span>" + days + "</span><span>" + hours + "</span><span>" + minutes + "</span><span>" + seconds + "</span>"; 
    }}

    function pad(n) {{
    	return (n < 10 ? '0' : '') + n;
    }}

    </script>
    <a class="btn btn-dark mt-2" href="{}" target="_blank" rel="nofollow">Add to my calendar</a>
    """.format(match_details_['match_time'].replace(tzinfo=timezone.utc).astimezone(tz=None),
               match_id, match_id, match_id, match_details_['match_time'].timestamp() * 1000, match_id, match_id,
               match_id, match_id, match_id, match_id,
               """https://www.google.com/calendar/render?action=TEMPLATE&text=Match+{}+{}+vs+{}&dates={}/{}&details={}&sf=true&output=xml""".
               format(match_id.zfill(2), team_1_data['team_name'], team_2_data['team_name'],
                      match_details_['match_time'].strftime('%Y%m%dT%H%M00Z'),
                      (match_details_['match_time'] + timedelta(hours=4)).strftime('%Y%m%dT%H%M00Z'),
                      'Match Link: {}'.format(request.get_raw_uri().split('api')[0] + match_id)).replace(' ', '+'))
    elif status == 'Started':
        match_data_2 = '<div>'
        id_ = request.session['id']
        in_team = id_ in team_1_data['players'] or id_ in team_2_data['players']
        if in_team:
            match_data_2 += "<h5 class='mt-5'>Match Server: {}</h5><h5>HLTV Server: {}</h5>".format(
                match_details_['match_external_ip'], match_details_['hltv_external_ip'])
        else:
            match_data_2 += "<h5 class='mt-5'>HLTV Server: {}</h5>".format(match_details_['hltv_external_ip'])
        if in_team:
            match_data_2 += "<a href='steam://connect/{}' class='btn btn-primary mt-3 text-light mr-3'>Join Match</a>".format(
                match_details_['match_external_ip'])
        match_data_2 += "<a href='steam://connect/{}' class='btn btn-primary mt-3 text-light'>Join HLTV</a></div>".format(
            match_details_['hltv_external_ip'])

    match_data_3 = """</div>
            </div>
            <div class="col-md-1"></div>
            <div class="col-md-2">
                <img src="{}"
                     class="card-img" alt="" style="border-radius: 0;">
                <div class="card-header bg-dark border-dark text-light">{} ({})</div>
            </div>
        </div>
    </div>""".format(team_2_data['team_logo_url'], team_2_data['team_name'], team_2_data['team_tag'])

    match_data += match_data_1 + match_data_2 + match_data_3

    team_data = """
<div class="card" style="border-top: none;">
    <div class="row no-gutters">
        <div class="col-md-6">
            <div class="col-md-4">
                <ul class="list-group list-group-flush">
        """

    for player_id in team_1_data['players']:
        player_data = handler.dataHelper.get_player_data_by_id(player_id)
        team_data += """
                <li class="list-group-item" style='background: transparent;'>
                    <img src="{}" title="" alt="" style="height: 4vh; width: 4vh">
                    <a target="_blank" href="https://steamcommunity.com/profiles/{}" style='vertical-align: sub; padding-left: .75rem;'> {}</a>
                </li>
        """.format(player_data['avatar_url'], player_data['steam_url_id'], player_data['username'], )

    team_data += """
                </ul>
            </div>
            <div class="col-md-6"></div>
        </div>
        <div class="col-md-6">
            <div class="col-md-8"></div>
            <div class="col-md-4 ml-md-auto text-right">
                <ul class="list-group list-group-flush">
        """

    for player_id in team_2_data['players']:
        player_data = handler.dataHelper.get_player_data_by_id(player_id)
        team_data += """
                <li class="list-group-item" style='background: transparent;'>
                    <a target="_blank" href="https://steamcommunity.com/profiles/{}" style='vertical-align: sub; padding-right: .75rem;'>{} </a>
                    <img src="{}" title="" alt="" style="height: 4vh; width: 4vh">
                </li>
        """.format(player_data['steam_url_id'], player_data['username'], player_data['avatar_url'], )

    team_data += """
                </ul>
            </div>
        </div>
    </div>
</div>
"""

    return JsonResponse({'match_data': match_data + team_data})
