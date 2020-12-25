""" --------------------------------------------------------------------------------------------------------------------
    Strings Used to print information
-------------------------------------------------------------------------------------------------------------------- """

""" --------------------------------------------------------------------------------------------------------------------
    Saving characters to print
-------------------------------------------------------------------------------------------------------------------- """
SPACE = " "
UNDERSCORE = "_"
DOT = "."
SEPARATOR = "/"
N = "n"
Y = "Y"
SINGLE_QUOTE = "'"
CLOSE_SQ_BRACE = "]"
OPEN_SQ_BRACE = "["
CLOSE_CIRCULAR_BRACE_ = ")"
COMMA = ","
COLON = ":"
DASH = "-"
PLUS = "+"
STAR = "*"
SEMI_COLON = ";"
HASH = "#"
EMPTY_STRING = ""
PIPE = "|"
EQUALS = "="
GREATER_THAN = ">"
DOUBLE_QUOTE = '"'
UNIX_SEPARATOR = "\\"
NEW_LINE = "\n"
TAB = "    "
TAB_ = "\t"
QUESTION_MARK = "?"
CLOSE_CURL_BRACE = r"}"
OPEN_CURL_BRACE = r"{"
BYE = 'Bye'

""" --------------------------------------------------------------------------------------------------------------------
    Stats
-------------------------------------------------------------------------------------------------------------------- """
KILLS = "kills"
DEATHS = "deaths"
GRENADE = "grenade"
HEADSHOT = "headshot"
SUICIDE = "suicide"
BOMB_PLANT = "bomb_plant"
BOMB_DEFUSE = "bomb_defuse"
KNIFE = "knife"
MATCHES = "matches"
NAME_SMALL = "name"
NICK_SMALL = "nick"
ONE = "1"
TWO = "2"
THREE = "3"
FOUR = "4"
FIVE = "5"
SIX = "6"
SEVEN = "7"
EIGHT = '8'
NINE = '9'
TEN = '10'
D_M = "D:M"
B_C = "B:C"
S_STEAM_ID = "steam_id"
M = "M"
L = "L"
K = "K"
J = "J"
I_ = "I"
H = "H"
G = "G"
F = "F"
E = "E"
D = "D"
C = "C"
B = "B"
ORIENT = 'index'

""" --------------------------------------------------------------------------------------------------------------------
    File Formats
-------------------------------------------------------------------------------------------------------------------- """
TXT = ".txt"
LOG = ".log"
DEMO_FORMAT = ".dem"
TEXT = "txt"
JPG = ".jpg"

""" --------------------------------------------------------------------------------------------------------------------
    Status for servers
-------------------------------------------------------------------------------------------------------------------- """
RUNNING = "running"
VERSUS = "vs"
DISCARDED = "Discarded"
ACTIVE = "Active"
STATUS = "status"
MATCH = "match"
IP = "ip"
CSTRIKE = "cstrike"
MODIFY = "modify"
DIR = "dir"
TYPE = "type"
STOPPED = "stopped"
HLTV = "HLTV"
START_TIME = "start_time"
END_TIME = "end_time"
SERVER_STATUS_STOP = 'stop'
SERVER_STATUS_START = 'start'

""" --------------------------------------------------------------------------------------------------------------------
    Team constants
-------------------------------------------------------------------------------------------------------------------- """
TEAM_NAME_ = "Team Name"
TEAM_NAME = "team_name"
TEAM_TAG_ = "Team Tag"
TEAM_TAG = "team_tag"
TEAM_NAME_OG = "Team Name Og"
TEAM_2_ID = "team2_id"
TEAM_1_ID = "team1_id"
TEAM_TAG_2_ = "team_tag2"
TEAM_TAG_1_ = "team_tag1"
TEAM_2_ = "team2"
TEAM_1_ = "team1"
CAPTAINS_NAME = "Captains Name"
TEAMS = "teams"
CAPTAIN_2 = 'vice_captain'
CAPTAIN_1 = 'captain'

""" --------------------------------------------------------------------------------------------------------------------
    Player constants
-------------------------------------------------------------------------------------------------------------------- """
EMAIL = "Email"
ID = "ID"
NO_PLAYER = "EMPTY_NO_PLAYER"
STEAM_ID = "Steam ID"
STEAM_URL_ID = "steam_url_id"
NICK_ = "Nick"
NAME_ = "Name"
NAME = "name"
STEAM_NICK = "username"
JOIN_TEAM = "join_team"
REG_TIME = "reg_time"
FB_LINK = "fb_link"
TEAM = 'team'

""" --------------------------------------------------------------------------------------------------------------------
    Queries
-------------------------------------------------------------------------------------------------------------------- """
DELETE_FROM_MATCHES_WHERE_ID_ = "DELETE FROM `matches` WHERE `id` = {}"
DELETE_FROM_ADMINS_WHERE_ID_ = "DELETE FROM `{}` WHERE `auth` = '{}'"
INSERT_MATCHES_VALUES_ = "INSERT INTO `matches` VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
INSERT_ADMINS_VALUES_ = "INSERT INTO `{}` VALUES ('{}', '', '{}', 'ce')"
UPDATE_ADMINS_ACCESS_ = "UPDATE `{}` SET `access` = '{}' WHERE `auth` = '{}'"
UPDATE_DONE_WHERE_MATCHES_ID_ = "UPDATE `matches` SET `ip` = '{}_done' WHERE `matches`.`id` = {}"
INSERT_VALUE_ = "'{}', "
INSERT_INTO_TEAMS_VALUES_ = "INSERT INTO `teams` VALUES('{}', "
SELECT_MATCHES_WHERE_IP_ = "SELECT * FROM `matches` WHERE `ip` = '{}'"
TRUNCATE_TABLE_ = "truncate table {}"
DROP_TABLE_IF_EXISTS = "DROP TABLE IF EXISTS {}"
TABLE_TEAMS_PL2 = "player_{} varchar(35));"
TABLE_TEAMS_PL1 = "player_{} varchar(35),"
TABLE_TEAMS = "create table if not exists {} (id varchar(20) not null primary key,"
TABLE_MATCHES = "create table if not exists `{}` (id int not null primary key, team1 varchar(35), team2 varchar(35), team_tag1 varchar(35), team_tag2 varchar(35), ip varchar(35), team1_id varchar(35), team2_id varchar(35), time timestamp);"
CREATE_DATABASE = "create database if not exists {};"
TABLE_ADMINS = "CREATE TABLE if not exists `{}` (`auth` varchar(32) NOT NULL, `password` varchar(32) NOT NULL, `access` varchar(32) NOT NULL, `flags` varchar(32) NOT NULL)"

""" --------------------------------------------------------------------------------------------------------------------
    Server constants
-------------------------------------------------------------------------------------------------------------------- """
SERVER_NAME = "Server Name"
SERVER_IP = "Server IP"
HLTV_SERVER_NAME = "HLTV Server Name"
PORT = "Port"
HLTV_IP = "HLTV IP"
HLTV_PASSWORD = "HLTV_Password"
PASSWORD = "Password"
USERNAME = "Username"
HLTV_USERNAME = "HLTV_Username"
INSTANCE_NAME = "Instance Name"
HLTV_NAME = "HLTV Name"
MATCH_SERVER = "Match Server"

""" --------------------------------------------------------------------------------------------------------------------
    Team Names
-------------------------------------------------------------------------------------------------------------------- """
TERRORIST = "T"
COUNTER_TERRORIST = "CT"

""" --------------------------------------------------------------------------------------------------------------------
    Logging
-------------------------------------------------------------------------------------------------------------------- """
DATE = "date"
DATE_ = "date_"
ORG = "org"
ISP = "isp"
CITY = "city"
REGION_NAME = "regionName"
UNKNOWN = "Unknown"
SAY_TEAM = "say_team"
STEAM = "STEAM"
TSAY = "tsay"
SAY = "say"
SAY_TEAM_LOGS_TXT = "say_team_logs.txt"
SAY_LOGS_TXT = "say_logs.txt"
L_ = "L20"
NS_NAME = "name"
RETR_ = "RETR "
D_M_Y = "%d-%m-%Y"

""" --------------------------------------------------------------------------------------------------------------------
    File modes
-------------------------------------------------------------------------------------------------------------------- """
READ_MODE = "r"
WB_MODE = "wb"
W_PLUS_MODE = "w+"
WRITE_MODE = "w"
READ_PLUS_MODE = "r+"

""" --------------------------------------------------------------------------------------------------------------------
    VAC Banned
-------------------------------------------------------------------------------------------------------------------- """
STEAM_ID_ = "SteamId"
T_TEAM = "Team"
ECONOMY_BAN = "EconomyBan"
COMMUNITY_BANNED = "CommunityBanned"
NUMBER_OF_VAC_BANS = "NumberOfVACBans"
DAYS_SINCE_LAST_BAN = "DaysSinceLastBan"
VAC_BANNED = "VACBanned"
STATS = "Stats"
PLAYERS = "players"
EMPTY_RAW_STRING = r""

""" --------------------------------------------------------------------------------------------------------------------
    Match constants
-------------------------------------------------------------------------------------------------------------------- """
TEAM_LIST = "team_list"
COUNT = "count"
USERS = "users"
CREATED = "Created"
COMPLETED = "Completed"
STARTED = "Started"

""" --------------------------------------------------------------------------------------------------------------------
    Helper constants
-------------------------------------------------------------------------------------------------------------------- """
WORKBOOK_HELPER = "workbook_helper"
USER_INPUT_HELPER = "user_input_helper"
PRINT_HELPER = "print_helper"
SQL_HELPER = "my_sql_helper"
LOCAL_DATA_HELPER = "local_data_helper"
FTP_HELPER = "ftp_helper"
DATA_STORE_HELPER = "data_store_helper"
CLOUD_SERVER_HELPER = "cloud_server_helper"
CONFIG_HELPER = 'config_helper'
CERTIFICATE_HELPER = 'certificate_helper'
LOG_HELPER = "log_helper"

""" --------------------------------------------------------------------------------------------------------------------
    Config Constants
-------------------------------------------------------------------------------------------------------------------- """
MY_SQL = 'MySQL'
USER_NAME = 'USERNAME'
PASS_WORD = 'PASSWORD'
DATABASE = 'DATABASE'
HOSTNAME = 'HOSTNAME'
ADMIN_TABLE = 'ADMIN_TABLE'

PROJECT_DETAILS = 'Project Details'
SERVICE_ACCOUNT_KEY_PATH = 'SERVICE_ACCOUNT_KEY_PATH'
SERVICE_ACCOUNT_EMAIL = 'SERVICE_ACCOUNT_EMAIL'
PROJECT_ID = 'PROJECT_ID'
STEAM_API_KEY = 'STEAM_API_KEY'
STEAM_USER_API = 'STEAM_USER_API'
MAX_PLAYERS = 'MAX_PLAYERS'
ADMIN_IDS = 'ADMIN_IDS'
DISPLAY_NAME = 'DISPLAY_NAME'
MODE = 'MODE'
FACEBOOK_API_KEY = 'FACEBOOK_API_KEY'
INITIAL_SETUP = 'INITIAL_SETUP'

FOLDER_LOCATIONS = "Folder Locations"
CSTRIKE_LOGS = 'CSTRIKE_LOGS'
ADDONS_AMXMODX_LOGS = 'ADDONS_AMXMODX_LOGS'
CONFIGS_RESULTS = 'CONFIGS_RESULTS'
TEMP_APP_ENGINE_FOLDER = 'TEMP_APP_ENGINE_FOLDER'

BUCKET_LOCATIONS = 'Bucket Locations'
FILES_HOME = 'FILES_HOME'
LOGS_STARTING = 'LOGS_STARTING'
SCORE_STARTING = 'SCORE_STARTING'
HLTV_STARTING = 'HLTV_STARTING'
IP_LOG_STARTING = 'IP_LOG_STARTING'
CERTIFICATES = 'CERTIFICATES'
RESOURCES = 'RESOURCES'
STATS_ = 'STATS'
BANNERS = "BANNERS"

FILE_LOCATIONS = "File Locations"
FONT_PATH = 'FONT_PATH'
CERT_IMG_PATH = 'CERT_IMG_PATH'
STEAM_ID_LIST_TXT = 'STEAM_ID_LIST_TXT'
STATS_FILE = 'STATS_FILE'
BANNED_USERS_FILE = 'STEAM_BANNED_USERS_FILE'
TEAM_DETAILS_XLSX = 'TEAM_DETAILS_XLSX'
BANNER_IMG = 'BANNER_IMG'
BANNER_FONT = 'BANNER_FONT'

COUNTER_STRIKE_ADMINS = 'Counter Strike Admins'
ADMINS = 'ADMINS'
APPROVERS = 'APPROVERS'
BASIC_ACCESS = 'BASIC_ACCESS'
ELITE_ACCESS = 'ELITE_ACCESS'
MANAGER_ACCESS = 'MANAGER_ACCESS'
OWNER_ACCESS = 'OWNER_ACCESS'
FULL_ACCESS = 'FULL_ACCESS'

CLOUD_FUNCTIONS_URLS = 'Cloud Function URLS'
HLTV_DEMOS_FUNC = 'HLTV_DEMOS_FUNC'
FTP_LOGS_FUNC = 'FTP_LOGS_FUNC'

FIRESTORE_COLLECTION_NAMES = "FireStore Collection Names"
FS_MATCHES = 'FS_MATCHES'
FS_GAME_SERVERS = 'FS_GAME_SERVERS'
FS_PLAYERS = 'FS_PLAYERS'
FS_TEAMS = 'FS_TEAMS'
FS_SERVERS = 'FS_SERVERS'