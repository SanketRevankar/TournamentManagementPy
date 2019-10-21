""" --------------------------------------------------------------------------------------------------------------------
    Printing terminal messages
-------------------------------------------------------------------------------------------------------------------- """
from constants import StringConstants as sC

""" --------------------------------------------------------------------------------------------------------------------
    Giant Messages
-------------------------------------------------------------------------------------------------------------------- """
PARSING_LOGS_MSG = r"""
+---------------------------------------------------------------------------------------------------------------------+
|                      ____                    _                   _                                                  |
|                     |  _ \  __ _  _ __  ___ (_) _ __    __ _    | |     ___    __ _  ___                            |
|                     | |_) |/ _` || '__|/ __|| || '_ \  / _` |   | |    / _ \  / _` |/ __|                           |
|                     |  __/| (_| || |   \__ \| || | | || (_| |   | |___| (_) || (_| |\__ \                           |
|                     |_|    \__,_||_|   |___/|_||_| |_| \__, |   |_____|\___/  \__, ||___/                           |
|                                                        |___/                  |___/                                 |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+                                                                       
"""

SAVE_PLAYER_SCORES_MSG = r"""
+---------------------------------------------------------------------------------------------------------------------+
|  ____                 _                   ____   _                               ____                               |
| / ___|   __ _ __   __(_) _ __    __ _    |  _ \ | |  __ _  _   _   ___  _ __    / ___|   ___  ___   _ __  ___  ___  |
| \___ \  / _` |\ \ / /| || '_ \  / _` |   | |_) || | / _` || | | | / _ \| '__|   \___ \  / __|/ _ \ | '__|/ _ \/ __| |
|  ___) || (_| | \ V / | || | | || (_| |   |  __/ | || (_| || |_| ||  __/| |       ___) || (__| (_) || |  |  __/\__ \ |
| |____/  \__,_|  \_/  |_||_| |_| \__, |   |_|    |_| \__,_| \__, | \___||_|      |____/  \___|\___/ |_|   \___||___/ |
|                                 |___/                      |___/                                                    |
|                       _               ____          _          ____   _                                             |
|                      | |_  ___       |  _ \   __ _ | |_  __ _ / ___| | |_  ___   _ __  ___                          |
|                      | __|/ _ \      | | | | / _` || __|/ _` |\___ \ | __|/ _ \ | '__|/ _ \                         |
|                      | |_| (_) |     | |_| || (_| || |_| (_| | ___) || |_| (_) || |  |  __/                         |
|                       \__|\___/      |____/  \__,_| \__|\__,_||____/  \__|\___/ |_|   \___|                         |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+                                                                       
"""

SAVE_MAP_SCORES_MSG = r"""
+---------------------------------------------------------------------------------------------------------------------+
|             ____                         __  __                   ____                                              |
|            / ___|   __ _ __   __ ___    |  \/  |  __ _  _ __     / ___|   ___  ___   _ __  ___  ___                 |
|            \___ \  / _` |\ \ / // _ \   | |\/| | / _` || '_ \    \___ \  / __|/ _ \ | '__|/ _ \/ __|                |
|             ___) || (_| | \ V /|  __/   | |  | || (_| || |_) |    ___) || (__| (_) || |  |  __/\__ \                |
|            |____/  \__,_|  \_/  \___|   |_|  |_| \__,_|| .__/    |____/  \___|\___/ |_|   \___||___/                |
|                                                        |_|                                                          |
|                      _               ____          _          ____   _                                              |
|                     | |_  ___       |  _ \   __ _ | |_  __ _ / ___| | |_  ___   _ __  ___                           |
|                     | __|/ _ \      | | | | / _` || __|/ _` |\___ \ | __|/ _ \ | '__|/ _ \                          |
|                     | |_| (_) |     | |_| || (_| || |_| (_| | ___) || |_| (_) || |  |  __/                          |
|                      \__|\___/      |____/  \__,_| \__|\__,_||____/  \__|\___/ |_|   \___|                          |
|                                                                                                                     |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+                                                                       
"""

WELCOME_MSG = """
+---------------------------------------------------------------------------------------------------------------------+
|                          __        __     _                                  _                                      |
|                          \ \      / /___ | |  ___  ___   _ __ ___    ___    | |                                     |
|                           \ \ /\ / // _ \| | / __|/ _ \ | '_ ` _ \  / _ \   | |                                     |
|                            \ V  V /|  __/| || (__| (_) || | | | | ||  __/   |_|                                     |
|                             \_/\_/  \___||_| \___|\___/ |_| |_| |_| \___|   (_)                                     |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
"""

TOURNEY_MANAGER_MSG = """
+---------------------------------------------------------------------------------------------------------------------+
|                            Choose From the below options. Press any other key to exit.                              |
|   1.  Create a New Match                                                                                            |
|   2.  Start Match                                                                                                   |
|   3.  End Match                                                                                                     |
|   4.  Get Match Data                                                                                                |
|   5.  Get Player List                                                                                               |
|   6.  Get Team List                                                                                                 |
|   7.  Add Steam IDs to MySQL DB                                                                                     |
|   8.  Create Participation certificates for players                                                                 |
|   9.  Convert Steam Ids to community Ids for Ban check                                                              |
|   10. Get Access list for captains                                                                                  |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
"""

GET_MATCH_DATA_MSG = """
+---------------------------------------------------------------------------------------------------------------------+
|                          __        __     _                                  _                                      |
|                          \ \      / /___ | |  ___  ___   _ __ ___    ___    | |                                     |
|                           \ \ /\ / // _ \| | / __|/ _ \ | '_ ` _ \  / _ \   | |                                     |
|                            \ V  V /|  __/| || (__| (_) || | | | | ||  __/   |_|                                     |
|                             \_/\_/  \___||_| \___|\___/ |_| |_| |_| \___|   (_)                                     |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
|                                                                                                                     |
|   1.  Save Team-wise Player Stats to Excel File.                                                                    |
|   2.  Get Players with Highest Stats.                                                                               |
|   3.  Show Match Scores of all Matches.                                                                             |
|   4.  Get IP matches for every Player.                                                                              |
|   5.  Get Connections of a Player by his Steam ID.                                                                  |
|   6.  Save Team Details (Players in a team) to Excel File.                                                          |
|   7.  Check VAC Bans of Players Registered.                                                                         |
|                                                                                                                     |
+---------------------------------------------------------------------------------------------------------------------+
"""

""" --------------------------------------------------------------------------------------------------------------------
    Prints for Server
-------------------------------------------------------------------------------------------------------------------- """
ADDED_ = "Added"
NOT_START_SUCCESSFULLY_ = "Server did not start successfully."
SERVER_STARTED_ = "Server Started"
STARTING_SERVER___ = "Starting Server..."
START_THE_SERVER_Y_N_ = "Do you want to start the server? [Y/n]"
ENTER_MATCH_ID_TO_START_ = "Enter Match id: "
SERVER_TO_GET_IP = "Start server to get ip"
ALREADY_STOPPED = "Already Stopped"
ALREADY_RUNNING = "Already Running"
SERVER_STATUS_ = "Server Status"
CHANGE_DATE_Y_N_ = "Change date? [Y/n]"
DATE_SET_TO_ = "Date set to"
SERVER_FOUND_ = "Server Found"
ASSOCIATED_SERVERS___ = "Finding Associated Servers..."
MATCH_SELECTED_ = "Match Selected"
CREATING_FOLDER_ = "Creating Folder"
FOLDER_EXISTS = "Folder Exists"

""" --------------------------------------------------------------------------------------------------------------------
    Prints for match information
-------------------------------------------------------------------------------------------------------------------- """
MATCH_SET_ = "Match Set"
COVER = "-------------------------------------------------------------"
YOU_TUBE_MATCH_VS_ = "YouTube: Match-{} {} vs {}"
FOLDER_MATCH_VS_ = "Folder: Match-{} {} vs {}"
INSTANCE_NAME_ = "Instance Name: {}"
HLTV_IP_ = "HLTV IP: {}"
SERVER_NAME_ = "Server Name: {}"
SERVER_IP_ = "Server IP: {}"
CT_CAPTAIN_ = "Team CT Captain: {} [{}]"
TEAM_CT_ = "Team CT: {} [{}]"
T_CAPTAIN_ = "Team T Captain: {} [{}]"
TEAM_T_ = "Team T: {} [{}]"
MATCH_ID_ = "Match ID: {}"
MATCH_VS_ = "Match-{} {} vs {}"
NO_ACTIVE_MATCHES_FOUND_ = "No Active matches found."
START_MATCH_INFO = '''
Tournament Match {}
{} vs {}
HLTV IP: {}
'''

""" --------------------------------------------------------------------------------------------------------------------
    Prints for match score
-------------------------------------------------------------------------------------------------------------------- """
CONFIRM_UPDATE_Y_N_ = "Confirm Update? [Y/n]"
WINNER_ = " Winner"
ENTER_MAP_SCORE_ = "Enter Map {} score"
MATCH_ = "Match"
MAP__SCORE = "map{}_score"
MAP_ = "map{}"
S_MAP_ = "Map"
ENTER_MAP_NAME_ = "Enter Map {}"
SCORE_OF_ = "Score of {} - {}"
ENTER_NO_OF_MAPS_ = "Enter No Of Maps"
COMPLETED_YET_ = 'No matches are completed yet.'
MATCH_ID_FROM_GIVEN_LIST = 'Enter valid match id from given list'
NO_TEAMS_FOUND = 'No teams found'

""" --------------------------------------------------------------------------------------------------------------------
    Prints for Adding a new match
-------------------------------------------------------------------------------------------------------------------- """
REMOVE_THE_PREVIOUS_MATCH_Y_N_ = "Do you want to remove the previous match? [Y/n]"
MATCH_ALREADY_SET_FOR_ = "Server has match set for Match #{} {} vs {}"
PREVIOUS_MATCH_Y_N_ = "Delete Previous Match? [Y/n]"
MATCH_ID_ALREADY_EXISTS = " Match id : {} Already exists"
ENTER_ID_OF_TEAM_2_ = "Enter id of team 2"
ENTER_ID_OF_TEAM_1_ = "Enter id of team 1"
ENTER_ID_OF_THE_SERVER_ = "Enter id of the server"
ENTER_MATCH_ID_ = "Enter Match ID"
PRINT_TEAM_DETAILS_ = "[{}] {}"
PRINT_SERVER_DETAILS_ = "{}. {} [{}]"
ALREADY_EXISTS = 'Already Exists'

""" --------------------------------------------------------------------------------------------------------------------
    Prints for HLTV
-------------------------------------------------------------------------------------------------------------------- """
HLTV_NOT_STOPPED_ = "HLTV did not stop successfully."
HLTV_STOPPED_ = "HLTV Stopped"
STOPPING_HLTV___ = "Stopping HLTV..."
HLTV_STATUS_ = "HLTV Status"
INSTANCE_HLTV = "instance-hltv"
NOT_STOP_SUCCESSFULLY_ = "Server did not stop successfully."
SERVER_STOPPED_ = "Server Stopped"
STOPPING_SERVER___ = "Stopping Server..."
STOP_THE_SERVER_Y_N_ = "Do you want to stop the server? [Y/n]"
SERVER_STATUS = "Server Status"
DOWNLOADING_HLTV_DEMOS = "Downloading HLTV Demos"
HLTV_NOT_START_SUCCESSFULLY_ = "HLTV did not start successfully."
HLTV_STARTED_ = "HLTV Started"
STARTING_HLTV___ = "Starting HLTV..."
HLTV_ = "HLTV:"

""" --------------------------------------------------------------------------------------------------------------------
    Prints for match info
-------------------------------------------------------------------------------------------------------------------- """
MATCH_INFO_ = "{}. {} vs {}"
MATCH__ = "Match-"
Z_MATCH__VS_ = "zMatch_#{} '{}' vs '{}'"
NO_MATCHES_FOUND_ = 'No matches found.'

""" --------------------------------------------------------------------------------------------------------------------
    Prints for Logging
-------------------------------------------------------------------------------------------------------------------- """
SAVING_DATA = "Saving Data"
PRINT_PLAYER_INFO = "# {} [{}] - {}"
FETCHING_IP_DETAILS = "Fetching IP Details"
FETCHING_DETAILS_OF_ = " Fetching Details of"
NEW_DATA_FROM_LOGS = "Loading New Data from Logs"
IP_ = "IP"
LOADING_SAVED_DATA = "Loading Local Data"
ENTER_DATE_DD_MM_YYYY_ = "Enter Date: (dd-mm-yyyy)"
LOGS_PARSED_ = "Logs parsed."
SCORES_SAVED__N = "Scores saved."

""" --------------------------------------------------------------------------------------------------------------------
    Prints for stats
-------------------------------------------------------------------------------------------------------------------- """
KNIFES = "Knifes"
DEFUSES = "Defuses"
PLANTS = "Plants"
HS = "HS"
P_SUICIDE = "Suicide"
P_GRENADE = "Grenade"
P_DEATHS = "Deaths"
P_KILLS = "Kills"
P_MATCHES = "Matches"
P_STEAM_ID = "Steam ID"
NO_SCORE_FOUND = "No Score Found"
MAX_BOMB_DEFUSE_ = "Max Bomb Defuse:"
MAX_BOMB_PLANTS_ = "Max Bomb Plants:"
MAX_SUICIDES_ = "Max Suicides:"
MAX_KNIFE_ = "Max Knife:"
MAX_GRENADE_KILLS_ = "Max Grenade Kills:"
MAX_HEADSHOT_ = "Max Headshot:"
MAX_DEATHS_ = "Max Deaths:"
MAX_KILLS_ = "Max Kills:"
LOADING_MATCHES_ = "Loading Matches:"
FILE_SAVED_ = "File Saved:"
LOADED_ = "Loaded:"
STATS_PRINT_COVER_ = sC.PLUS + sC.DASH * 22 + (sC.PLUS + sC.DASH * 9) * 9 + sC.PLUS + sC.DASH * 27 + \
                     sC.PLUS + sC.DASH * 37 + sC.PLUS
STATS_HEADER_ = sC.PIPE + sC.SPACE + P_STEAM_ID.center(20) + sC.SPACE + sC.PIPE + sC.SPACE + P_MATCHES.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + P_KILLS.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + P_DEATHS.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + P_GRENADE.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + HS.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + P_SUICIDE.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + PLANTS.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + DEFUSES.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + KNIFES.center(
    7) + sC.SPACE + sC.PIPE + sC.SPACE + sC.NAME_.center(
    25) + sC.SPACE + sC.PIPE + sC.SPACE + sC.NICK_.center(35) + sC.SPACE + sC.PIPE

""" --------------------------------------------------------------------------------------------------------------------
    Get Match data
-------------------------------------------------------------------------------------------------------------------- """
INVALID_CHOICE = "Invalid Choice"
ENTER_YOUR_CHOICE_ = "Enter Your Choice: "
P_ECONOMY_BANN = " Economy Bann"
LAST_TIME_ = "time || Last time:"
P_COMMUNITY_BANNED = " Community Banned"
TRUE = "True"
DAYS_AGO = "Days ago"
VAC_BANNED_ = " Vac Banned ||"
SAVED_ = "Saved: "
DOWNLOAD_ERROR_N_CODE_ = "Data download Failed, Error Code: "
ENTERED_THE_GAME = "entered the game"
WAS_KICKED_BY_CONSOLE_ = "was kicked by 'Console'"
CONNECTED = "connected"

""" --------------------------------------------------------------------------------------------------------------------
    Registrations
-------------------------------------------------------------------------------------------------------------------- """
REGISTRATIONS_ = "Successful Registrations:"
TOTAL_REGISTRATIONS_ = "Total Registrations:"

""" --------------------------------------------------------------------------------------------------------------------
    Prints for team, players list
-------------------------------------------------------------------------------------------------------------------- """
FORMAT_BRACES = "{}"
TEAM_LIST_ = r"TeamList = {"
SERVER_LIST_ = r"ServerList = {"
PLAYER_LIST_ = r"PlayerList = {"
