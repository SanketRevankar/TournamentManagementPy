""" --------------------------------------------------------------------------------------------------------------------
                                            STRINGS USED FOR LOGGING PURPOSES
-------------------------------------------------------------------------------------------------------------------- """

""" --------------------------------------------------------------------------------------------------------------------
    CertificateHelper.py
-------------------------------------------------------------------------------------------------------------------- """
CERTIFICATES_CREATED = 'Certificates created'
CERTIFICATES_FOR_ = 'Printing Certificates for {}'
STORE_CERTIFICATES = 'Creating Folder to store Certificates'

""" --------------------------------------------------------------------------------------------------------------------
    CloudServerHelper.py
-------------------------------------------------------------------------------------------------------------------- """
MATCH_SERVER_IP_ = "Match Server IP: {}"
HLTV_SERVER_IP_ = "Match Server IP: {}"
STARTING_SERVER_ = 'Starting server: {}'
SERVER_STATUS_ = 'Server {} [Status: {}]'

""" --------------------------------------------------------------------------------------------------------------------
    FTPHelper.py
-------------------------------------------------------------------------------------------------------------------- """
CURRENT_FOLDER_ = 'Current Folder: {}'
DOWNLOADING_DATA = 'Downloading data'
FOR_FTP_TRANSFER_ = 'Setting Source and Destination Folders for FTP Transfer.'
PASSIVE_MODE_FOR_FTP = 'Setting Passive mode for FTP'
USERNAME_AND_PASSWORD_ = 'Login to FTP using Username: {} and Password: {}'
CONNECTING_TO_ = 'Connecting to {}'
FTP_CONNECTION = 'Getting FTP Connection'

""" --------------------------------------------------------------------------------------------------------------------
    LocalDataHelper.py
-------------------------------------------------------------------------------------------------------------------- """
NO_IP_MATCHES_FOUND = 'No IP Matches found'
PRINTED_IP_MATCHES = 'Printed IP Matches'
WITH_FOR_EACH_PLAYER = 'Stats loaded with 0 for each player'
STEAM_ID_NOT_FOUND_ = 'Steam id not found: {}'
CLEARING_PREVIOUS_DATA = 'Creating files to store IP data and clearing previous data'
SAVING_IP_DATA_TO_ = 'Saving IP Data to {}'
WRITTEN_SUCCESSFULLY = 'Files written successfully'
ATTRIBUTE_ERROR_ = 'AttributeError: {}'
KEY_ERROR_ = 'KeyError: {}'
VALUE_ERROR_ = 'ValueError: {}'
FOR_TEAM_SAY_LOGS = 'Creating a file for team_say logs'
FILE_FOR_SAY_LOGS_ = 'Creating a file for say logs: {}'
FILE_ = 'File: {}'
SAVING_LOGS_FOR_MATCH_ = 'Saving logs for Match {}'
LOADING_STATS_COMPLETED = 'Loading stats completed'
NOT_FOUND_ = 'Not found: {}'
LOADING_STATS_FROM_ = 'Loading stats from {}'
INITIALIZING_STATS = 'Initializing stats'
LOADING_IP_DATA_OF_ = 'Loading IP data of {}'
IP_DETAILS_FROM_ = 'Fetching IP Details from {}'
IP_DATA_FROM_MATCH_LOGS = 'Loading IP data from match logs'
LOADING_STATS_FOR_ = 'Loading stats for: {}'
LOADING_MATCHES_FROM_ = 'Loading matches from: {}'
LOADING_DATA_FOR_ = 'Loading data for {}'
THE_DATA_IS_STORED = 'Getting files where the data is stored'
FOLDER_NAME_ = '{} - Folder Name: {}'
LOADING_CONNECTIONS_OF_ = 'Loading connections of {}'
NO_CONNECTIONS_FOUND = 'No Connections of the player found'
FOUND_CONNECTIONS = 'Found {} Connections'

""" --------------------------------------------------------------------------------------------------------------------
    MySQLHelper.py
-------------------------------------------------------------------------------------------------------------------- """
SQL_CONNECTION = 'Closing MySQL connection'
TEAM_ID_PLAYERS_ = 'Adding Team Id: {} Players: {}'
CURRENT_PLAYER_DATA = 'Adding current Player data'
PREVIOUS_PLAYER_DATA = 'Clearing previous Player data'
ADDED_SUCCESSFULLY = 'Match added successfully in Datastore'
MY_SQL_CONNECTION = 'Getting MySQL Connection'
EXECUTING_QUERY_ = 'Executing Query: {}'
QUERY_FAILED_ = 'Query Failed: {}'

""" --------------------------------------------------------------------------------------------------------------------
    UserInputHelper.py
-------------------------------------------------------------------------------------------------------------------- """
SCORE_FORMAT = 'Score format: [Score of team 1]-[Score of team 2] eg. 16-10'
SCORE_FORMAT_MISMATCH = 'Input score {} does not match the score format'
VALID_INPUTS_ = 'Valid inputs: {}'
INVALID_INPUT = 'Invalid input for Match ID: {}'

""" --------------------------------------------------------------------------------------------------------------------
    WorkbookHelper.py
-------------------------------------------------------------------------------------------------------------------- """
WRITING_DATA_FOR_TEAM_ = 'Writing data for Team {}'

""" --------------------------------------------------------------------------------------------------------------------
    CreateNewMatch.py
-------------------------------------------------------------------------------------------------------------------- """
MATCH_WITH_ID_SUCCESSFUL = "Adding match with ID {} successful"
MATCH_BTWN = """
                Match to be set between:
                    {} [{}] va {} [{}]
        """
TEAM_WITH_ID_SELECTED = 'Team with ID {} selected'
IP_SELECTED = 'IP: {} selected'

""" --------------------------------------------------------------------------------------------------------------------
    EndMatch.py
-------------------------------------------------------------------------------------------------------------------- """
LOGS_PARSED_SUCCESSFULLY = 'IP Logs parsed successfully'
PARSING_IP_LOGS = 'Parsing IP Logs'
PLAYER_SCORES_SAVED_SUCCESSFULLY = 'Player scores saved successfully'
SAVING_PLAYER_SCORES = 'Saving player scores'
MATCH_SCORES_SAVED_SUCCESSFULLY = 'Match scores saved successfully'
SAVING_MATCH_SCORES = 'Saving match scores'
MATCH_END_IN_MY_SQL = 'Match Set as ended in MySQL'
MATCH_IN_MY_SQL_DATABASE = 'Ending Match in MySQL Database'
STOPPING_SERVERS_SUCCESSFUL = 'Stopping Servers Successful'
STOPPING_SERVERS = 'Stopping servers...'
DOWNLOAD_OF_MATCH_DATA_COMPLETE = 'Download of match data complete'
DOWNLOADING_MATCH_DATA = 'Downloading match data'
CREATING_DIR_SAVING_DATA = 'Creating directories for saving data'
LOADED_ACTIVE_MATCHES = 'Loaded {} Active Matches'
FETCHING_ACTIVE_MATCHES = "Fetching Active Matches"
IP_DATA_SAVED = 'IP Data Saved'
IP_DETAILS_FETCHED = 'IP Details Fetched'
DATA_FROM_LOGS_LOADED = 'New data from logs loaded'
LOCAL_DATA_LOADED = 'Local data loaded'
DATA_SAVED_SUCCESSFULLY = 'Data saved successfully'
SAVING_TO_DATASTORE = 'Saving to datastore'
KEY_ = 'Key: {}'
DATA_FETCHED_SUCCESSFULLY = 'Data fetched successfully'
FETCHING_DATA_FROM_LOGS = 'Fetching data from logs'
MATCH_BETWEEN_AND_ = 'Match between {} and {}'
FETCHING_MATCH_DETAILS = 'Fetching match details'
HLTV_SERVER_SUCCESSFULLY = 'Stopped HLTV Server Successfully'
STOPPING_HLTV_SERVER = 'Stopping HLTV Server'
SERVER_SUCCESSFULLY = 'Stopped Match Server Successfully'
STOPPING_MATCH_SERVER = 'Stopping Match Server'
MATCH_DEMOS_FROM_FTP = 'Match demos downloaded from FTP'
STARTING_HLTV_FOR_DOWNLOAD = 'HLTV Server Started for data download'
VERIFYING_AND_STARTING_HLTV = 'Verifying and starting HLTV server for data download'
MATCH_DATA_DOWNLOADED_FROM_FTP = 'Match data downloaded from FTP'
SERVER_STARTED_FOR_DOWNLOAD = 'Server Started for data download'
VERIFY_SERVER_FOR_DATA_DOWNLOAD = 'Verifying and starting server for data download'
CONFIRMING_DATE = 'Confirming date'

""" --------------------------------------------------------------------------------------------------------------------
    LoadSteamIDs.py
-------------------------------------------------------------------------------------------------------------------- """
CAPTAIN_DETAILS_FORMAT = """ Format: 
                                            'Captain 1': '[Steam ID]',
                                            'Captain 2': '[Steam ID]',
                                            'Captain 1 Name': '[Name]',
                                            'Captain 2 Name': '[Name]',"""
MANUALLY_TO_TEAM_LIST = 'You need to add captains manually to Team List'
ACCESS_FOR_ALL_CAPTAINS = 'Printing access strings for all captains'
TEAM_DATA_WRITTEN_TO_ = 'Team Data successfully written to: '
FETCHING_DATA_FOR_TEAM_ = 'Fetching data for team {}'
WRITING_TEAM_DATA_TO_ = 'Writing Team Data to '
FETCHING_TEAM_LIST = 'Fetching team list'
CONVERT_IDS_SUCCESSFULLY = 'Converted Ids successfully'
WRITING_CONVERTED_IDS_TO_ = 'Writing converted Ids to {}'
STEAM_ID_TO_COMMUNITY_ID = 'Converting Steam ID to Community ID'
PLAYER_DATA_SUCCESSFULLY_WRITTEN_TO_ = 'Player Data successfully written to: {}'
FETCHING_PLAYERS_IN_TEAM_ = 'Fetching players in team {}'
WRITING_PLAYER_DATA_TO_ = 'Writing Player Data to {}'
TEAMS_FROM_DATASTORE = 'Fetching teams from datastore'

""" --------------------------------------------------------------------------------------------------------------------
    GetMatchData.py
-------------------------------------------------------------------------------------------------------------------- """
COMPLETED_SUCCESSFULLY = 'Operation completed successfully'
YOU_CHOSE_ = 'You chose [{}]'
LOADING_OPERATIONS_ = 'Loading Operations'
ABOUT_MATCHES = 'Get Information about Matches'
STEAM_IDS_FOR_VAC_BANS = 'Checking player Steam Ids for VAC Bans'
FILE_SAVED_ = 'File saved: {}'
SAVING_FILE_ = 'Saving file.'
WRITING_TEAM_DETAILS_OF_ = 'Writing team details of {}'
WRITING_TO_FILE_ = 'Writing to file: {}'
INITIATING_EXCEL_WRITER = 'Initiating ExcelWriter'
STEAM_ID_ = 'Steam ID: {}'
CONNECTIONS_OF_A_USER = 'Load connections of a user'
PRINTING_IP_MATCHES = 'Printing IP Matches'
LOADED_TIME_FROM_IP_DATA = 'Loaded Time from IP Data'
LOAD_TIME_FROM_IP_DATA = 'Load Time from IP data'
LOADED_IP_DATA = 'Loaded IP data'
IP_DATA_FROM_LOGS = 'Loading IP data from logs'
MATCH_SCORES_ARE_PRINTED = 'All match scores are printed'
PRINTING_MATCH_SCORES = 'Printing match scores'
MATCH_SCORES_LOADED = 'Match scores loaded'
FETCHING_MATCH_SCORES = 'Fetching Match Scores'
PRINTING_TOP_STATS = 'Printing Top stats'
NUMBER_OF_MATCHES_PLAYED = 'Stats will be average by number of matches played'
AVG_STATS_ARE_CONFIGURED_ = 'Average stats are configured.'
WORKBOOK_CLOSED = 'Workbook Closed'
STATS_WRITTEN_TO_ = 'Stats written to: {}'
WRITING_STATS_TO_FILE_ = 'Writing stats to file {}'
LOADED_STATS_FROM_LOGS = 'Loaded stats from logs'
LOADING_STATS_FROM_LOGS = 'Loading stats from logs'
WORKBOOK_CREATED_AT_ = 'Workbook created at: {}'
WORKBOOK_TO_SAVE_DATA = 'Creating workbook to save data'

""" --------------------------------------------------------------------------------------------------------------------
    StartMatch.py
-------------------------------------------------------------------------------------------------------------------- """
MATCH_STARTED_SUCCESSFULLY = 'Match {} started successfully'
SERVER_STARTED_SUCCESSFULLY = 'Server {} started successfully'
HLTV_INSTANCE_NAME_ = 'HLTV Server Instance name: {}'
INSTANCE_NAME_ = 'Match Server Instance name: {}'
SERVER_ID_ = 'Server ID {}'
MATCH_ID_SELECTED = 'Match ID [{}] selected'
LOADED___MATCHES = 'Loaded {} Matches'
FETCHING_CREATED_MATCHES = "Fetching Created Matches"
FETCHING_STARTED_MATCHES = "Fetching Started Matches"
