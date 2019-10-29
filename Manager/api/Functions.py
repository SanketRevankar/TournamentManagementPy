import os
import re

import pandas as pd

from TournamentManagementPy import handler
from constants import StringConstants as sC, PyConstants as pC
from firestore_data.MatchData import MatchList
from firestore_data.PlayerData import PlayerList, SteamList
from firestore_data.ServerData import ServerList
from firestore_data.TeamData import TeamList


def new_match():
    return dict(html="""<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h2>Create a new Match</h2>
    <h5>Used to create a new match</h5>
</div>

<div id="match-config">
    <div class="form-row">

        <div class="form-group col-md-2">
            <label for="match-id" id="label-match-id">Match ID</label>
            <input type="text" class="form-control" aria-roledescription="match-id-help" id="match-id" 
            placeholder="Enter Match ID">
            <small id="match-id-help" class="form-text text-muted">Enter Match Id</small>
        </div>
        <div class='col-sm-2'>
            <label for='datetimepicker'>Match start time</label>
            <input type='datetime-local' class="form-control" id='datetimepicker' />
        </div>
        <div class="form-group col-md-2">
            <label for="team-1" id="label-team-1">Team 1</label>
            <div class="input-group">
                <select class="form-control custom-select" id="team-1" aria-roledescription="team-1-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="team-1-help" class="form-text text-muted">Select a Team</small>
        </div>

        <div class="form-group col-md-2">
            <label for="team-2" id="label-team-2">Team 2</label>
            <div class="input-group">
                <select class="form-control custom-select" id="team-2" aria-roledescription="team-2-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="team-2-help" class="form-text text-muted">Select a Team</small>
        </div>

        <div class="form-group col-md-2">
            <label for="match-servers" id="label-wifi-connections">Match Server</label>
            <div class="input-group">
                <select class="form-control custom-select" id="match-servers" aria-roledescription="match-server-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="match-server-help" class="form-text text-muted">Select a Match Server</small>
        </div>

        <div class="form-group col-md-2">
            <label for="hltv-servers">HLTV Server</label>
            <div class="input-group">
                <select class="form-control custom-select" id="hltv-servers" aria-roledescription="match-hltv-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="match-hltv-help" class="form-text text-muted">Select a HLTV Server</small>
        </div>

    </div>

    <div class="form-row mt-3">
        <div class="col-md-4"></div>
        <div class="col-md-4">
            <button class="btn btn-success w-100" id="preview-match">Preview Match Data</button>
        </div>
        <div class="col-md-4"></div>
    </div>

    <div class="row m-0 mt-4" id='preview-data' style="height: 55vh; 
    background: url('https://static.ewistore.co.uk/uploads/2019/02/silicone-vs.-silicate-vs.-bio.jpg') center; 
    background-size: cover;" hidden>
        <div class="col-md-4 pl-5">
            <img src="" id='team-1-logo' alt="" style="height: 40vh; width: 40vh; align-self: center; margin-top: 5vh;
             margin-bottom: 1vh;">
            <h2 id="team-1-name"></h2>
        </div>
        <div class="col-md-4">
            <p class="card-text" id="match-name" style="text-align: left; color: black; font-size: 1.2rem; 
            margin-bottom: auto; margin-top: 5%;">Match Server #1</p>
            <p class="card-text" id="hltv-name" style="text-align: right; color: white; bottom: 5%; right: 5%; 
            font-size: 1.2rem; position: absolute;">HLTV Server #1</p>
        </div>
        <div class="col-md-4 pr-5" style="    text-align: right;">
            <img src="" id='team-2-logo' alt="" style="height: 40vh; width: 40vh; align-self: center; margin-top: 5vh; 
            margin-bottom: 1vh;">
            <h2 id="team-2-name" style="color: white"></h2>
        </div>
    </div>

    <div class="form-row mt-3">
        <div class="col-md-4"></div>
        <div class="col-md-4">
            <button class="btn btn-success w-100" id="create-match" hidden>Create Match</button>
        </div>
        <div class="col-md-4"></div>
    </div>

</div>

<div class="modal" tabindex="-1" id='confirm-modal' role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Create Match</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body" id="modal-body"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <a href="/Manager" type="button" class="btn btn-success">Manage</a>
                <button type="button" class="btn btn-primary" id="confirmationModal">Create a new match</button>
            </div>
        </div>
    </div>
</div>

<script>
    $(document).ready(function() {
        let team1 = $('#team-1');
        let team2 = $('#team-2');
        let match_servers = $('#match-servers');
        let hltv_servers = $('#hltv-servers');
        let team_1_name = $('#team-1-name');
        let team_1_logo = $('#team-1-logo');
        let team_2_name = $('#team-2-name');
        let team_2_logo = $('#team-2-logo');
        let match_name = $('#match-name');
        let match_id = $('#match-id');
        let hltv_name = $('#hltv-name');
        let preview_data = $('#preview-data');
        let preview_match = $('#preview-match');
        let create_match = $('#create-match');
        let datetime = $('#datetimepicker');
        var team_data;
        var server_data;

        match_id.focusout(function () {
            let match_id_ = $(this).val();

            $(this).removeClass('is-valid').removeClass('is-invalid');

            if (match_id_.match('^[0-9]+$')) {
                $(this).addClass('is-valid');
            } else {
                $(this).addClass('is-invalid');
            }
        });

        match_servers.click(function () {
            server_id = match_servers.val();

            match_servers.removeClass('is-valid').removeClass('is-invalid');

            if (!server_id.match('Select a Server') && !server_id.match('Loading...')) {
                match_servers.addClass('is-valid');
                clear_preview();
            } else {
                match_servers.addClass('is-invalid');
                clear_preview();
            }
        });

        hltv_servers.click(function () {
            server_id = hltv_servers.val();

            hltv_servers.removeClass('is-valid').removeClass('is-invalid');

            if (!server_id.match('Select a Server') && !server_id.match('Loading...')) {
                hltv_servers.addClass('is-valid');
                clear_preview();
            } else {
                hltv_servers.addClass('is-invalid');
                clear_preview();
            }
        });

        team1.click(function () {
            let team_1 = team1.val();
            let team_2 = team2.val();

            if (team_1 === team_2) {
                team1.addClass('is-invalid');
                return false;
            }

            team1.removeClass('is-valid').removeClass('is-invalid');

            if (!team_1.match('Select a Team') && !team_1.match('Loading...')) {
                team1.addClass('is-valid');
                clear_preview();
            } else {
                team1.addClass('is-invalid');
                clear_preview();
            }
        });

        function clear_preview() {
            preview_data.attr('hidden', '');
            create_match.attr('hidden', '');
            preview_match.removeAttr('hidden');
        }

        team2.click(function () {
            let team_1 = team1.val();
            let team_2 = team2.val();

            if (team_1 === team_2) {
                team2.addClass('is-invalid');
                return false;
            }

            team2.removeClass('is-valid').removeClass('is-invalid');

            if (!team_2.match('Select a Team') && !team_2.match('Loading...')) {
                team2.addClass('is-valid');
                clear_preview();
            } else {
                team2.addClass('is-invalid');
                clear_preview();
            }
        });

        datetime.focusout(function () {
            datetime.removeClass('is-valid').removeClass('is-invalid');
            if (datetime.val() !== '') {
                datetime.addClass('is-valid');
            } else {
                datetime.addClass('is-invalid');                
            }
        });

        preview_match.click(function () {
            if (match_servers.hasClass('is-valid') && team1.hasClass('is-valid') && team2.hasClass('is-valid') && 
                match_id.hasClass('is-valid') && hltv_servers.hasClass('is-valid') && datetime.hasClass('is-valid')) {
                let team_1 = team1.val();
                let team_2 = team2.val();

                team_1_name.html(team_data[team_1]['team_name']);
                team_1_logo.attr('src', team_data[team_1]['team_logo_url']);

                team_2_name.html(team_data[team_2]['team_name']);
                team_2_logo.attr('src', team_data[team_2]['team_logo_url']);

                match_name.html(server_data[match_servers.val()]['server_name']);
                hltv_name.html(server_data[hltv_servers.val()]['server_name']);

                preview_data.removeAttr('hidden');
                create_match.removeAttr('hidden');
                preview_match.attr('hidden', '');
            }
        });

        create_match.click(function () {
            $.ajax({
                url: 'api/v1/func/put/create_match',
                method: 'post',
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    "team_1": team1.val(),
                    "team_2": team2.val(),
                    'match_server': match_servers.val(),
                    'hltv_server': hltv_servers.val(),
                    'match_id': match_id.val(),
                    'datetime': datetime.val(),
                },
                success: function (data) {
                    $('#modal-body').html(data['match_id']);
                    $('#confirm-modal').modal('show');
                }
            });
        });


        $('#confirmationModal').click(function () {
            $('#confirm-modal').modal('hide');

            $('#content').html('<i class="fas fa-spinner fa-spin" style="font-size: 100px;margin-top: 35vh;margin-left: 40vw;"></i>' +
                '<h3 style="color: black; margin-left: 40vw; margin-top: 3vh;">Loading...</h3>');

            $.ajax({
                url: 'api/v1/func/new_match',
                success: function (data) {
                    $('#content').html(data['html']);
                }
            })
        });

        $.ajax({
            url: 'api/v1/func/get/teams',
            success: function (data) {
                team_data = data['team_data'];
                team1.html(data['html']);
                team2.html(data['html']);
            }
        });
        $.ajax({
            url: 'api/v1/func/get/servers',
            success: function (data) {
                server_data = data['server_data'];
                match_servers.html(data['match']);
                hltv_servers.html(data['hltv']);
            }
        });
    });
</script>
    """)


def start_match():
    """
    Starts a match

    """

    return dict(html="""<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h2>Start a created Match</h2>
    <h5>Used to start a match</h5>
</div>
<div id="match-start">
    <div class="form-row">
        <div class="form-group col-md-3">
            <label for="matches" id="label-matches">Matches</label>
            <div class="input-group">
                <select class="form-control custom-select" id="matches" aria-roledescription="matches-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="matches-help" class="form-text text-muted">Select a Match</small>
        </div>
    </div>

    <button class='btn btn-success' id='start-match'>Start Match</button>


    <div class="modal" tabindex="-1" id='confirm-modal' role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Start Match</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body" id="modal-body"></div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="confirmationModal">Start match</button>
                </div>
            </div>
        </div>
    </div>
</div>

<div id="run-code" class='mt-3' hidden  style='font-size: 1.2rem;'>
    <h3 id='match-title'></h3>
    <div class='mt-3' style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a id='match-server-name' style='font-size: 1.4rem;'>Match Server</a><br>
        <i id='match-server-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='match-server-status' class='text-primary'>Starting...</st><br>
        <a id='match-server-ip-copy' href='#' class='fas fa-copy' hidden></a>
        <ip id='match-server-ip' hidden>Ip will be shown after server starts.</ip>
    </div>
    <div class='mt-3' style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a id='hltv-server-name' style='font-size: 1.4rem;'>HLTV Server</a><br>
        <i id='hltv-server-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='hltv-server-status' class='text-primary'>Starting...</st><br>
        <a id='hltv-server-ip-copy' href='#' class='fas fa-copy' hidden></a>
        <ip id='hltv-server-ip' hidden>Ip will be shown after server starts.</ip>
    </div>
    <h5 class='mt-4' id='match-start-status' hidden>Match started successfully</h5>
</div>

<script>

    $(document).ready(function() {
        let matches = $('#matches');

        $('#start-match').click(function () {
            if (matches.hasClass('is-valid')) {
                $('#modal-body').html('Are you sure to start match: ' + $('#matches option:selected').html() +
                    '<p class="text-primary">All the servers related to the match will be started now</p>');
                $('#confirm-modal').modal('show');
            }
            return false;
        });

        let match_server_name = $('#match-server-name');
        let match_server_stat = $('#match-server-stat');
        let match_server_status = $('#match-server-status');
        let match_server_ip = $('#match-server-ip');
        let match_server_ip_copy = $('#match-server-ip-copy');
        let hltv_server_name = $('#hltv-server-name');
        let hltv_server_stat = $('#hltv-server-stat');
        let hltv_server_status = $('#hltv-server-status');
        let hltv_server_ip = $('#hltv-server-ip');
        let hltv_server_ip_copy = $('#hltv-server-ip-copy');
        let match_status = $('#match-start-status');

        $('#confirmationModal').click(function () {
            $('#confirmationModal').modal('hide');
            let servers = 0;

            $('#confirm-modal').modal('hide');
            $('#match-start').attr('hidden', '');
            $('#match-title').html('Starting Match: #' + $('#matches option:selected').html());
            $('#run-code').removeAttr('hidden');


            $.ajax({
                url: 'api/v1/func/put/start_match',
                method: 'post',
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    'match_id': matches.val(),
                },
                success: function (data) {
                    match_server_name.html(data['match_server']);
                    hltv_server_name.html(data['hltv_server']);
                }
            });

            $.ajax({
                url: 'api/v1/func/put/start_match_server',
                method: 'post',
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    'match_id': matches.val(),
                },
                success: function (data) {
                    servers += 1;
                    match_server_ip.html(data['ip']);
                    match_server_ip.removeAttr('hidden');
                    match_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                    match_server_stat.addClass('fa-check-circle').addClass('text-success');
                    match_server_status.removeAttr('hidden');
                    match_server_status.html(data['status']);
                    match_server_status.addClass('text-success');
                    match_server_ip_copy.removeAttr('hidden');
                    start_match_in_db();
                },
                error: function (_) {
                    match_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                    match_server_stat.addClass('fa-times-circle').addClass('text-danger');
                    match_server_status.removeAttr('hidden');
                    match_server_status.html('Failed');
                    match_server_status.removeClass('text-primary').addClass('text-danger');
                }
            });

            $.ajax({
                url: 'api/v1/func/put/start_hltv_server',
                method: 'post',
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    'match_id': matches.val(),
                },
                success: function (data) {
                    servers += 1;
                    hltv_server_ip.html(data['ip']);
                    hltv_server_ip.removeAttr('hidden');
                    hltv_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                    hltv_server_stat.addClass('fa-check-circle').addClass('text-success');
                    hltv_server_status.removeAttr('hidden');
                    hltv_server_status.html(data['status']);
                    hltv_server_status.addClass('text-success');
                    hltv_server_ip_copy.removeAttr('hidden');
                    start_match_in_db();
                },
                error: function (_) {
                    hltv_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                    hltv_server_stat.addClass('fa-times-circle').addClass('text-danger');
                    hltv_server_status.removeAttr('hidden');
                    hltv_server_status.html('Failed');
                    hltv_server_status.removeClass('text-primary').addClass('text-danger');
                }
            });

            function start_match_in_db() {
                if (servers !== 2) {
                    return false;
                }

                $.ajax({
                    url: 'api/v1/func/put/start_match_db',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                        'match_ip': match_server_ip.html(),
                        'hltv_ip': hltv_server_ip.html(),
                    },
                    success: function (data) {
                        if ('error' in data) {
                             match_status.removeAttr('hidden');
                             match_status.html(data['error']);
                             match_status.addClass('text-danger');
                        }
                        match_status.removeAttr('hidden');
                        match_status.addClass('text-success');
                    },
                    error: function (data) {
                        match_status.removeAttr('hidden');
                        match_status.html('Match start failed');
                        match_status.addClass('text-danger');
                    }
                });
            }
        });

        hltv_server_ip_copy.click(function() {{
            var textArea = document.createElement("textarea");
            textArea.value = 'HLTV Ip: ' + hltv_server_ip.html();
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }});

        match_server_ip_copy.click(function() {{
            var textArea = document.createElement("textarea");
            textArea.value = 'Match Server Ip: ' + match_server_ip.html();
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }});

        matches.click(function () {
            match_id = matches.val();

            matches.removeClass('is-valid').removeClass('is-invalid');

            if (!match_id.match('Select a Match to start') && !match_id.match('Loading...')
                && !match_id.match('Create a new match to start')) {
                matches.addClass('is-valid');
            } else {
                matches.addClass('is-invalid');
            }
        });

        $.ajax({
            url: 'api/v1/func/get/matches_created',
            success: function (data) {
                matches.html(data['matches']);
            }
        })
    });
</script>""")


def end_match():
    return {'html': """<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h2>End a Match</h2>
    <h5>Used to end a match</h5>
</div>
<div id="match-end">
    <div class="form-row">
        <div class="form-group ml-1 mr-1 col-md-12">
            <label for="matches" id="label-matches">Matches</label>
            <div class="input-group">
                <select class="form-control custom-select" id="matches" aria-roledescription="matches-help">
                    <option selected>Loading...</option>
                </select>
            </div>
            <small id="matches-help" class="form-text text-muted">Select a Match</small>
        </div>
    </div>

    <div class='row mt-3'>
        <div class='col-md-1'>
            <div class="custom-control custom-switch text-right">
                Maps
            </div>
            <div class='form-group ml-1 mr-1 ta-r'>
                <label for="team_1"></label>
                <input type="email" class="form-control-plaintext text-right" id="team_1" placeholder="Team 1" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="team_2"></label>
                <input type="email" class="form-control-plaintext text-right" id="team_2" placeholder="Team 2" disabled>
            </div>
        </div>
        <div class='col-md'>
            <div class="ml-3 custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="de_dust2">
                <label class="custom-control-label" for="de_dust2">de_dust2</label>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_dust2_team_1"></label>
                <input type="email" class="form-control" id="de_dust2_team_1" placeholder="Score" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_dust2_team_2"></label>
                <input type="email" class="form-control" id="de_dust2_team_2" placeholder="Score" disabled>
            </div>
        </div>
        <div class='col-md'>
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="de_inferno">
                <label class="ml-3 custom-control-label" for="de_inferno">de_inferno</label>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_inferno_team_1"></label>
                <input type="email" class="form-control" id="de_inferno_team_1" placeholder="Score" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_inferno_team_2"></label>
                <input type="email" class="form-control" id="de_inferno_team_2" placeholder="Score" disabled>
            </div>
        </div>
        <div class='col-md'>
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="de_nuke">
                <label class="ml-3 custom-control-label" for="de_nuke">de_nuke</label>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_nuke_team_1"></label>
                <input type="email" class="form-control" id="de_nuke_team_1" placeholder="Score" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_nuke_team_2"></label>
                <input type="email" class="form-control" id="de_nuke_team_2" placeholder="Score" disabled>
            </div>
        </div>
        <div class='col-md'>
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="de_train">
                <label class="ml-3 custom-control-label" for="de_train">de_train</label>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_train_team_1"></label>
                <input type="text" class="form-control" id="de_train_team_1" placeholder="Score" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_train_team_2"></label>
                <input type="text" class="form-control" id="de_train_team_2" placeholder="Score" disabled>
            </div>
        </div>
        <div class='col-md'>
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="de_mirage">
                <label class="ml-3 custom-control-label" for="de_mirage">de_mirage</label>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_mirage_team_1"></label>
                <input type="text" class="form-control" id="de_mirage_team_1" placeholder="Score" disabled>
            </div>
            <div class='form-group ml-1 mr-1'>
                <label for="de_mirage_team_2"></label>
                <input type="text" class="form-control" id="de_mirage_team_2" placeholder="Score" disabled>
            </div>
        </div>
    </div>

    <div class='row'>
        <div class='col-md-3'></div>
        <button class='col-md-6 btn btn-success mt-5' id='end-match'>End Match</button>
        <div class='col-md-3'></div>
    </div>
</div>

<div id="run-code" class='mt-3' style='font-size: 1.2rem;' hidden>
    <h3 id='match-title'></h3>
    <div class='mt-3' id='download-logs' hidden style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a style='font-size: 1.4rem;'>Copying logs</a><br>
        <i id='download-logs-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='download-logs-status' class='text-primary'>Copying...</st><br>
    </div>
    <div class='mt-3' id='download-demos' hidden style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a style='font-size: 1.4rem;'>Copying HLTV Demos</a><br>
        <i id='download-demos-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='download-demos-status' class='text-primary'>Copying...</st><br>
    </div>
    <div class='mt-3' id='parsing-logs' hidden style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a style='font-size: 1.4rem;'>Parsing Logs</a><br>
        <i id='parsing-logs-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='parsing-logs-status' class='text-primary'>Parsing...</st><br>
    </div>
    <button class='btn btn-primary mt-3 ml-2' id='match-server-stop' hidden>Stop Match Server</button>
    <div class='mt-3' id='match-server' hidden style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a id='match-server-name' style='font-size: 1.4rem;'>Match Server</a><br>
        <i id='match-server-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='match-server-status' class='text-primary'>Stopping...</st><br>
    </div>
    <button class='btn btn-primary mt-3 ml-2' id='hltv-server-stop' hidden>Stop HLTV Server</button>
    <div class='mt-3' id='hltv-server' hidden style="border-left: 2px solid black; padding-left: 10px; margin-left: 10px;">
        <a id='hltv-server-name' style='font-size: 1.4rem;'>HLTV Server</a><br>
        <i id='hltv-server-stat' class='far fa-circle fa-grow text-primary'></i>
        <st id='hltv-server-status' class='text-primary'>Stopping...</st><br>
    </div>
    <h5 class='mt-4' id='match-end-status' hidden>Match stopped successfully</h5>
</div>

<div class="modal" tabindex="-1" id='confirm-modal' role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">End Match</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body" id="modal-body"></div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-danger" id="confirmationModal">End match</button>
            </div>
        </div>
    </div>
</div>

</div>
<script>

    $(document).ready(function() {
        let de_dust2 = $('#de_dust2');
        let de_dust2_team_1 = $('#de_dust2_team_1');
        let de_dust2_team_2 = $('#de_dust2_team_2');
        let de_inferno = $('#de_inferno');
        let de_inferno_team_1 = $('#de_inferno_team_1');
        let de_inferno_team_2 = $('#de_inferno_team_2');
        let de_nuke = $('#de_nuke');
        let de_nuke_team_1 = $('#de_nuke_team_1');
        let de_nuke_team_2 = $('#de_nuke_team_2');
        let de_train = $('#de_train');
        let de_train_team_1 = $('#de_train_team_1');
        let de_train_team_2 = $('#de_train_team_2');
        let de_mirage = $('#de_mirage');
        let de_mirage_team_1 = $('#de_mirage_team_1');
        let de_mirage_team_2 = $('#de_mirage_team_2');
        let scores = {};

        $('#confirmationModal').click(function () {
            $('#confirmationModal').modal('hide');

            let download_logs = $('#download-logs');
            let download_logs_stat = $('#download-logs-stat');
            let download_logs_status = $('#download-logs-status');
            let download_demos = $('#download-demos');
            let download_demos_stat = $('#download-demos-stat');
            let download_demos_status = $('#download-demos-status');
            let match_server = $('#match-server');
            let match_server_name = $('#match-server-name');
            let match_server_stat = $('#match-server-stat');
            let match_server_status = $('#match-server-status');
            let hltv_server = $('#hltv-server');
            let hltv_server_name = $('#hltv-server-name');
            let hltv_server_stat = $('#hltv-server-stat');
            let hltv_server_status = $('#hltv-server-status');
            let parsing_logs = $('#parsing-logs');
            let parsing_logs_stat = $('#parsing-logs-stat');
            let parsing_logs_status = $('#parsing-logs-status');
            let match_status = $('#match-end-status');
            let match_server_stop = $('#match-server-stop');
            let hltv_server_stop = $('#hltv-server-stop');

            $.ajax({
                url: 'api/v1/func/put/end_match',
                method: 'post',
                data: {
                    'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                    'match_id': matches.val(),
                },
                success: function (data) {
                    $('#confirm-modal').modal('hide');
                    $('#match-end').attr('hidden', '');
                    $('#run-code').removeAttr('hidden');
                    $('#match-title').html(data['match_name']);
                    match_server_name.html(data['match_server']);
                    hltv_server_name.html(data['hltv_server']);

                    copy_logs_demos();
                }
            });

            function copy_logs_demos() {
                let copied = 0;
                download_logs.removeAttr('hidden');
                download_demos.removeAttr('hidden');

                $.ajax({
                    url: 'api/v1/func/put/download_match_logs',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                    },
                    success: function (data) {
                        copied += 1;
                        download_logs_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        download_logs_stat.addClass('fa-check-circle').addClass('text-success');
                        download_logs_status.removeAttr('hidden');
                        download_logs_status.html(data['status']);
                        download_logs_status.removeClass('text-primary').addClass('text-success');
                        parse_logs();

                        if (copied === 2) {
                            stop_servers();
                        }
                    },
                    error: function (_) {
                        download_logs_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        download_logs_stat.addClass('fa-times-circle').addClass('text-danger');
                        download_logs_status.removeAttr('hidden');
                        download_logs_status.html('Failed');
                        download_logs_status.removeClass('text-primary').addClass('text-danger');
                    }
                });

                $.ajax({
                    url: 'api/v1/func/put/download_match_demos',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                    },
                    success: function (data) {
                        copied += 1;
                        download_demos_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        download_demos_stat.addClass('fa-check-circle').addClass('text-success');
                        download_demos_status.removeAttr('hidden');
                        download_demos_status.html(data['status']);
                        download_demos_status.removeClass('text-primary').addClass('text-success');

                        if (copied === 2) {
                            stop_servers();
                        }
                    },
                    error: function (_) {
                        download_demos_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        download_demos_stat.addClass('fa-times-circle').addClass('text-danger');
                        download_demos_status.removeAttr('hidden');
                        download_demos_status.html('Failed');
                        download_demos_status.removeClass('text-primary').addClass('text-danger');
                    }
                });
            }

            match_server_stop.click(function () {
                match_server_stop.attr('hidden', '');
                match_server.removeAttr('hidden');

                $.ajax({
                    url: 'api/v1/func/put/stop_match_server',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                    },
                    success: function (data) {
                        match_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        match_server_stat.addClass('fa-check-circle').addClass('text-success');
                        match_server_status.removeAttr('hidden');
                        match_server_status.html(data['status']);
                        match_server_status.addClass('text-success');
                    },
                    error: function (_) {
                        match_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        match_server_stat.addClass('fa-times-circle').addClass('text-danger');
                        match_server_status.removeAttr('hidden');
                        match_server_status.html('Failed');
                        match_server_status.removeClass('text-primary').addClass('text-danger');
                    }
                });
            });

            hltv_server_stop.click(function () {
                hltv_server_stop.attr('hidden', '');
                hltv_server.removeAttr('hidden');

                $.ajax({
                    url: 'api/v1/func/put/stop_hltv_server',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                    },
                    success: function (data) {
                        hltv_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        hltv_server_stat.addClass('fa-check-circle').addClass('text-success');
                        hltv_server_status.removeAttr('hidden');
                        hltv_server_status.html(data['status']);
                        hltv_server_status.addClass('text-success');
                    },
                    error: function (_) {
                        hltv_server_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        hltv_server_stat.addClass('fa-times-circle').addClass('text-danger');
                        hltv_server_status.removeAttr('hidden');
                        hltv_server_status.html('Failed');
                        hltv_server_status.removeClass('text-primary').addClass('text-danger');
                    }
                });
            });

            function stop_servers() {
                match_server_stop.removeAttr('hidden');
                hltv_server_stop.removeAttr('hidden');
            }

            function parse_logs() {
                parsing_logs.removeAttr('hidden');

                $.ajax({
                    url: 'api/v1/func/put/parse_match_logs',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                    },
                    success: function (data) {
                        parsing_logs_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        parsing_logs_stat.addClass('fa-check-circle').addClass('text-success');
                        parsing_logs_status.removeAttr('hidden');
                        parsing_logs_status.html(data['status']);
                        parsing_logs_status.addClass('text-success');

                        end_match_db()
                    },
                    error: function (_) {
                        parsing_logs_stat.removeClass('fa-circle').removeClass('fa-grow').removeClass('text-primary');
                        parsing_logs_stat.addClass('fa-times-circle').addClass('text-danger');
                        parsing_logs_status.removeAttr('hidden');
                        parsing_logs_status.html('Failed');
                        parsing_logs_status.removeClass('text-primary').addClass('text-danger');
                    }
                });
            }

            function end_match_db() {
                $.ajax({
                    url: 'api/v1/func/put/end_match_db',
                    method: 'post',
                    data: {
                        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
                        'match_id': matches.val(),
                        'scores': JSON.stringify(scores),
                    },
                    success: function (_) {
                        match_status.removeAttr('hidden');
                        match_status.addClass('text-success');
                    },
                    error: function (_) {
                        match_status.removeAttr('hidden');
                        match_status.html('Match stop failed');
                        match_status.addClass('text-danger');
                    }
                });
            }
        });


        $('[id*=team]').focusout(function() {
            $(this).removeClass('is-valid').removeClass('is-invalid');

            if ($(this).val().match('^[0-9]+$')) {
                $(this).addClass('is-valid');
            } else {
                $(this).addClass('is-invalid');
            }
        });

        $('.custom-control-input').click(function () {
            id_ = $(this).attr('id');
            let $1 = $('#' + id_ + '_team_1');
            let $2 = $('#' + id_ + '_team_2');
            if($(this).is(":checked")) {
                $1.removeAttr('disabled');
                $2.removeAttr('disabled');
            } else {
                $1.val('');
                $1.removeClass('is-valid').removeClass('is-invalid');
                $1.attr('disabled', '');
                $2.val('');
                $2.removeClass('is-valid').removeClass('is-invalid');
                $2.attr('disabled', '');
            }
        });

        let matches = $('#matches');

        $('#end-match').click(function () {
            let selected = 0;

            if(de_dust2.is(':checked')) {
                if (de_dust2_team_1.hasClass('is-valid') && de_dust2_team_2.hasClass('is-valid')) {
                    selected += 1;
                    scores[de_dust2.attr('id')] = {
                        "team_1": de_dust2_team_1.val(),
                        "team_2": de_dust2_team_2.val(),
                    }
                }
            }

            if(de_inferno.is(':checked')) {
                if (de_inferno_team_1.hasClass('is-valid') && de_inferno_team_2.hasClass('is-valid')) {
                    selected += 1;
                    scores[de_inferno.attr('id')] = {
                        "team_1": de_inferno_team_1.val(),
                        "team_2": de_inferno_team_2.val(),
                    }
                }
            }

            if(de_nuke.is(':checked')) {
                if (de_nuke_team_1.hasClass('is-valid') && de_nuke_team_2.hasClass('is-valid')) {
                    selected += 1;
                    scores[de_nuke.attr('id')] = {
                        "team_1": de_nuke_team_1.val(),
                        "team_2": de_nuke_team_2.val(),
                    }
                }
            }

            if(de_train.is(':checked')) {
                if (de_train_team_1.hasClass('is-valid') && de_train_team_2.hasClass('is-valid')) {
                    selected += 1;
                    scores[de_train.attr('id')] = {
                        "team_1": de_train_team_1.val(),
                        "team_2": de_train_team_2.val(),
                    }
                }
            }

            if(de_mirage.is(':checked')) {
                if (de_mirage_team_1.hasClass('is-valid') && de_mirage_team_2.hasClass('is-valid')) {
                    selected += 1;
                    scores[de_mirage.attr('id')] = {
                        "team_1": de_mirage_team_1.val(),
                        "team_2": de_mirage_team_2.val(),
                    }
                }
            }

            if (selected < 2) {
                alert('Enter atleast 2 map scores to continue');

                return false;
            }

            if (matches.hasClass('is-valid')) {
                let print_sc = '';
                for (var data in scores) {
                    print_sc += '<br>' + data + ": " + scores[data]["team_1"] + '-' + scores[data]["team_2"];
                }
                $('#modal-body').html('Are you sure to end match: ' + $('#matches option:selected').html() + print_sc);
                $('#confirm-modal').modal('show');
            } else {
                matches.removeClass('is-invalid');
                matches.addClass('is-invalid');
            }

            return false;
        });

        matches.click(function () {
            match_id = matches.val();

            matches.removeClass('is-valid').removeClass('is-invalid');

            if (!match_id.match('Select a Match to stop') && !match_id.match('Loading...')
                && !match_id.match('No matches are currently active')) {
                matches.addClass('is-valid');
            } else {
                matches.addClass('is-invalid');
            }
        });

        $.ajax({
            url: 'api/v1/func/get/matches_started',
            success: function (data) {
                matches.html(data['matches']);
            }
        })
    });
</script>"""}


def match_scores():
    response = """<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h1>Match Scores</h1>
    <h5>Displaying scores of all Completed Matches</h5>
</div>
<div class='card-columns'>"""

    matches = handler.fireStoreHelper.util.get_matches('Completed')
    for match in matches:
        team_1 = handler.dataHelper.get_team_data_by_id(matches[match]['team_1'])['team_name']
        team_2 = handler.dataHelper.get_team_data_by_id(matches[match]['team_2'])['team_name']
        response += """
    <div class="card border-dark text-center">
    <div class="card-header bg-dark border-dark text-light">{}. {} vs {}</div>
        <div class="card-body p-0">
        <table class='w-100 table-striped'>
        <thead><tr><th>Map</th><th>Score</th></tr></thead>
    <tbody>""".format(match, team_1, team_2)
        for i in range(1, 6):
            if 'map_{}'.format(i) in matches[match]:
                response += '<tr><td>{}</td><td>{}</td></tr>'. \
                    format(matches[match]['map_{}'.format(i)]['name'], matches[match]['map_{}'.format(i)]['score'])
        response += """
    </tbody>
    </table>
    </div>
</div>"""

    response += '</div>'

    return {'html': response}


def player_stats():
    return {}


def highest_stats():
    return {}


def ip_matches():
    return {}


def connections():
    return {'html': """<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
        <h2>Connections by Steam ID:</h2>
        <h5>Check for Connections by Steam ID</h5>
    </div>

    <div class="form-group col-md-2" id='con'>
        <label for="steam-id" id="label-steam-id">Steam ID</label>
        <input type="text" class="form-control" aria-roledescription="steam-id-help" id="steam-id" 
        placeholder="Enter steam ID">
        <small id="steam-id-help" class="form-text text-muted">Enter Steam Id</small>
        <button class='btn btn-success mt-3' id='conns'>Get Connections</button>
    </div>

    <div id="run-code" hidden class='mt-3'>
        <label for="text-streaming">Checking for Connections...</label>
        <textarea class="form-control btn-dark" id="text-streaming" style='height: 50vh;' disabled></textarea>
    </div>

    <script>
        $(document).ready(function() {
            let textarea = $('#text-streaming');
            let conns = $('#conns');
            let steam_id = $('#steam-id');

            conns.click(function () {       
                $.ajax({
                    url: 'api/v1/func/get/connections',
                    method: 'get',
                    data: {
                        'steam_id': steam_id.val(),
                    },
                    success: function (data) {
                        $('#con').attr('hidden', '');
                        $('#run-code').removeAttr('hidden');
                        textarea.html(data['html']);
                    }
                });

            })
        });"""}


def team_details():
    tmp_team_details_xlsx_ = handler.config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER] + 'team_details.xlsx'
    writer = pd.ExcelWriter(tmp_team_details_xlsx_, engine=pC.XLSX_ENGINE)

    teams = handler.dataHelper.get_teams()
    players = handler.dataHelper.get_players()
    for team in teams:
        team_name = handler.dataHelper.get_team_name_by_steam_id(team)
        team_name = re.sub(pC.REGEX_TO_REMOVE_UNWANTED_CHARS, sC.EMPTY_STRING, team_name)[:31]
        player_dict = {}
        count = 1

        for player in teams[team][sC.PLAYERS]:
            player_dict[count] = {
                "Steam ID": players[player][sC.S_STEAM_ID],
                "Name": players[player][sC.NAME],
                "Nick": players[player][sC.STEAM_NICK],
            }
            count += 1
        players_ = pd.DataFrame.from_dict(player_dict, orient=sC.ORIENT)
        players_.to_excel(writer, sheet_name=team_name)

    writer.save()
    writer.close()

    handler.cloudStorageHelper.upload_file(handler.config[sC.FILE_LOCATIONS][sC.TEAM_DETAILS_XLSX],
                                           tmp_team_details_xlsx_)
    os.remove(tmp_team_details_xlsx_)

    return dict(html="""<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">
            <h1>Team Details saved successfully</h1>
            <h3>Click to download team details: <a target='_blank' href='https://storage.cloud.google.com/ncl/{}'>Team Details</a></h3>
        </div>""".format(handler.config[sC.FILE_LOCATIONS][sC.TEAM_DETAILS_XLSX]))


def vac_bans():
    return {'html': """<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h2>VAC Bans</h2>
    <h5>Check for VAC Banned IDs in the registered player list</h5>
</div>

<button class='btn btn-success' id='vac-bans'>Get VAC Bans</button>

<div id="run-code" hidden class='mt-3'>
    <label for="text-streaming">Checking for VAC Bans...</label>
    <textarea class="form-control btn-dark" id="text-streaming" style='height: 50vh;' disabled></textarea>
</div>

<script>
    $(document).ready(function() {
        let textarea = $('#text-streaming');
        let vac_bans = $('#vac-bans');

        vac_bans.click(function () {          
            $.ajax({
                url: 'api/v1/func/get/vac_bans',
                method: 'get',
                data: {},
                success: function (data) {
                    vac_bans.attr('hidden', '');
                    $('#run-code').removeAttr('hidden');
                    textarea.html(data['html']);
                }
            });

        })
    });"""}


def team_list():
    TeamList.clear()
    handler.fireStoreHelper.util.load_team_data()

    return {'html':
                """<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">
        <h1>Team List updated successfully</h1>
    </div>""", 'data': TeamList}


def player_list():
    PlayerList.clear()
    handler.fireStoreHelper.util.load_player_data()

    return {'html': """<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">
    <h1>Player List updated successfully</h1>
    </div>""", 'data': SteamList}


def server_list():
    ServerList.clear()
    handler.fireStoreHelper.util.load_server_data()

    return {'html':
                """<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">
        <h1>Server List updated successfully</h1>
    </div>""", 'data': ServerList}


def match_list():
    MatchList.clear()
    handler.fireStoreHelper.util.load_match_data()

    return {'html':
                """<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">
        <h1>Server List updated successfully</h1>
    </div>""", 'data': MatchList}


def steam_ids_db():
    """
    Add players in teams to MySQL DB

    """

    mysql_ = handler.mySQLHelper
    query = sC.DROP_TABLE_IF_EXISTS.format(sC.TEAMS)
    mysql_.execute_query(query)

    create_table_teams = sC.TABLE_TEAMS.format(sC.TEAMS)
    for i in range(1, int(32)):
        create_table_teams += sC.TABLE_TEAMS_PL1.format(i)
    create_table_teams += sC.TABLE_TEAMS_PL2.format(32)
    mysql_.execute_query(create_table_teams)

    for team in handler.dataHelper.get_teams():
        query = sC.INSERT_INTO_TEAMS_VALUES_.format(team)
        for i in range(32):
            query += sC.INSERT_VALUE_.format(handler.dataHelper.get_steam_id(i, team))
        query = query[:-2] + sC.CLOSE_CIRCULAR_BRACE_

        mysql_.execute_query(query)

    return {'html': '<div style="text-align: center; margin-top: 10vh; background: rgb(0,0,0,.25); padding: 4vh;">'
                    '<h1>Updated MySQL Database with latest values from TeamList</h1>'
                    '<h3>Click Team List on left menu to update TeamList</h3></div>'}


def participation_certificates():
    return {}


def access_list():
    handler.adminHelper.truncate_admin_table()
    handler.adminHelper.add_server_admins()

    teams = handler.dataHelper.get_teams()
    for team in teams:
        try:
            handler.adminHelper.add_admin(teams[team][sC.CAPTAIN_1])
            handler.adminHelper.add_admin(teams[team][sC.CAPTAIN_2])
        except KeyError:
            pass

    response = """<div class="pt-2 pb-1 mb-2" style="border-bottom: 1px solid;">
    <h1>Access strings for all captains</h1>
    <h3 class='mb-3'>You need to add captains manually to Team List</h3>
    </div>
    <h3>Access for captains updated in database!</h3>
    """
    return {'html': response}
