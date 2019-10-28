import json
import os
from time import sleep

import requests

from TournamentManagementPy import handler
from constants import StringConstants as sC, PrintStrings as pS, PyConstants as pC, LogStrings as lS
from firestore_data.PlayerData import PlayerList
from firestore_data.TeamData import TeamList


class LocalDataHelper:
    def __init__(self, config):
        """
        Initialize the Local Data Helper
        This Class contains Local Data related Functions

        :param config: Config object
        """

        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]
        self.ip_log_starting_ = config[sC.BUCKET_LOCATIONS][sC.IP_LOG_STARTING]
        self.hltv_starting_ = config[sC.BUCKET_LOCATIONS][sC.HLTV_STARTING]
        self.score_starting_ = config[sC.BUCKET_LOCATIONS][sC.SCORE_STARTING]
        self.logs_starting_ = config[sC.BUCKET_LOCATIONS][sC.LOGS_STARTING]
        self.steam_api_key = config[sC.PROJECT_DETAILS][sC.STEAM_API_KEY]
        self.steam_user_api_ = config[sC.PROJECT_DETAILS][sC.STEAM_USER_API]
        self.banned_users_file_ = config[sC.FILE_LOCATIONS][sC.BANNED_USERS_FILE]

        print('{} - Initialized'.format(__name__))

    @staticmethod
    def count_wins(i, scores):
        """
        Count wins

        :param i: Which team to count wins
        :param scores: Scores Dict Object
        :return: Wins of team
        """

        print(pS.MATCH_ + sC.COLON, i)
        print(sC.TAB, scores[i][sC.TEAM_1_], sC.VERSUS,
              scores[i][sC.TEAM_2_])

        win = 0
        for m in range(0, 5):
            try:
                score = scores[i][pS.MAP__SCORE.format(m + 1)]
                print(sC.TAB + sC.TAB + sC.STAR,
                      scores[i][pS.MAP_.format(m + 1)].ljust(10), score.rjust(pC.PADDING))
                score_split = score.split(sC.DASH)
                if int(score_split[0].strip()) < int(score_split[1].strip()):
                    win += 1
                else:
                    win -= 1
            except KeyError:
                break
        return win

    @staticmethod
    def add_team_count(count_matches, file_split):
        """
        Count matches played by teams from logs

        :param count_matches: Dict to store matches played by teams
        :param file_split: File name as split to get team names
        """

        if file_split[1] not in count_matches:
            count_matches[file_split[1]] = 0
        count_matches[file_split[1]] += 1
        if file_split[3] not in count_matches:
            count_matches[file_split[3]] = 0
        count_matches[file_split[3]] += 1

    def create_dirs_for_match_data(self, folder):
        """
        Create Folders in Cloud Storage for storing match data

        :param folder: Folder name
        """

        handler.cloudStorageHelper.create_folder(self.logs_starting_ + folder + '/')
        handler.cloudStorageHelper.create_folder(self.score_starting_ + folder + '/')
        handler.cloudStorageHelper.create_folder(self.hltv_starting_ + folder + '/')

    def get_ip_data(self):
        """
        Load previous IP Data from local system

        :return: Dict of IP Data
        """

        steam_id = {}

        print(lS.THE_DATA_IS_STORED)
        files = self.get_saved_log_files()

        c_steam = sC.UNKNOWN
        c_ip = sC.UNKNOWN

        for file in files:
            for line in files[file]:
                if line[0] == sC.HASH:
                    steam_id_ = line[line.index(sC.STEAM):].strip()
                    c_steam = steam_id_

                if sC.SEMI_COLON in line and line[0] != sC.HASH:
                    line_split = line.split(sC.SEMI_COLON)
                    c_ip = line_split[0].strip()
                    details = line_split[1].split(sC.TAB)

                    if c_steam not in steam_id:
                        steam_id[c_steam] = {}
                    steam_id[c_steam][c_ip] = {
                        sC.REGION_NAME: details[0].strip(),
                        sC.CITY: details[1].strip(),
                        sC.ISP: details[2].strip(),
                        sC.ORG: details[3].strip()
                    }

                if sC.DATE in line:
                    line_split = line.split()
                    c = 0
                    date = sC.UNKNOWN

                    for line_c in line_split:
                        if c == 0:
                            c += 1
                            steam_id[c_steam][c_ip][line_c] = []
                            date = line_c
                        else:
                            steam_id[c_steam][c_ip][date] \
                                .append(line_c.replace(sC.SINGLE_QUOTE, sC.EMPTY_STRING)
                                        .replace(sC.OPEN_SQ_BRACE, sC.EMPTY_STRING)
                                        .replace(sC.CLOSE_SQ_BRACE, sC.EMPTY_STRING)
                                        .replace(sC.COMMA, sC.EMPTY_STRING))

        return steam_id

    def load_stats_from_logs(self, stats):
        """
        Load stats from logs stored locally

        :param stats: Dict of stats for all players
        """

        starting_ = self.score_starting_

        for file in os.listdir(starting_):
            temp_ids = []

            for file_ip in os.listdir(starting_ + file):
                if sC.TEXT not in file_ip:
                    continue

                with open(starting_ + file + sC.SEPARATOR + file_ip) as f:
                    for line in f:
                        stat = line.strip().split()
                        team, nick, name = handler.dataHelper.get_team_nick_name_by_s_id(stat[0])

                        if stat[0] not in temp_ids:
                            temp_ids.append(stat[0])
                            stats[team][stat[0]][sC.MATCHES] += 1
                        stats[team][stat[0]][stat[1]] += 1

    def get_saved_log_files(self):
        """
        Get list of files to store IP data

        :return: Dict of files
        """

        files = {}
        for team in TeamList:
            file_name = self.ip_log_starting_ + handler.dataHelper.get_clean_team_name(TeamList[team][sC.TEAM_NAME]) +\
                        sC.TXT
            if os.path.exists(file_name):
                files[team] = open(file_name, sC.READ_MODE, encoding=pC.ENCODING)
        return files

    def get_data_from_logs(self, steam_id):
        """
        Get IP Data from logs of current match

        :param steam_id: List of all steam IDs
        """

        print(lS.IP_DATA_FROM_MATCH_LOGS)
        for file_a in os.listdir(self.logs_starting_):
            for file in os.listdir(self.logs_starting_ + file_a):
                if pS.IP_ + sC.UNDERSCORE in file:
                    date = file.strip().replace(pS.IP_ + sC.UNDERSCORE, sC.EMPTY_STRING).replace(
                        sC.TXT, sC.EMPTY_STRING)
                    with open(self.logs_starting_ + sC.UNIX_SEPARATOR + file_a +
                              sC.UNIX_SEPARATOR + file, encoding=pC.ENCODING) as f:
                        for line in f:
                            log = line.strip().split(sC.TAB_)

                            try:
                                _ = handler.dataHelper.get_team_by_steam_id(log[2])
                            except TypeError:
                                continue

                            if log[2] not in steam_id:
                                steam_id[log[2]] = {}

                            if log[3] not in steam_id[log[2]]:
                                steam_id[log[2]][log[3]] = {}

                            if sC.DATE_ + date not in steam_id[log[2]][log[3]]:
                                steam_id[log[2]][log[3]][sC.DATE_ + date] = []

                            steam_id[log[2]][log[3]][sC.DATE_ + date].append(log[0])

        return steam_id

    @staticmethod
    def get_connections(blob_str, steam):
        """
        Returns connection to server by players

        :param blob_str: String of file contents
        :param steam: steam Id of the player
        """

        resp = ''
        count = 0
        for line in blob_str.split('\n'):
            line_split = line.split(sC.DOUBLE_QUOTE)

            if pS.CONNECTED in line or pS.WAS_KICKED_BY_CONSOLE_ in line or pS.ENTERED_THE_GAME in line:
                try:
                    pos_steam = line_split[1].index(sC.STEAM)
                except ValueError:
                    continue
                steam_id = line_split[1][pos_steam:line_split[1].index(sC.GREATER_THAN, pos_steam)]
                if steam_id == steam:
                    resp += '{} {}\n'.format(sC.TAB, line.strip())
                    count += 1

        if count == 0:
            resp += lS.NO_CONNECTIONS_FOUND + sC.NEW_LINE
        else:
            resp += lS.FOUND_CONNECTIONS.format(count) + sC.NEW_LINE

        return resp

    @staticmethod
    def get_info(community_id):
        """
        Get player information

        :param community_id: Community id of the player
        """

        for player in PlayerList:
            if PlayerList[player][sC.STEAM_URL_ID] == community_id:
                return PlayerList[player][sC.TEAM] if sC.TEAM in PlayerList[player] else \
                    '' + sC.NEW_LINE + sC.TAB + sC.STEAM_ID + sC.COLON + sC.SPACE + PlayerList[player][sC.STEAM_URL_ID]\
                    + sC.NEW_LINE + sC.TAB + sC.NAME_ + sC.COLON + sC.SPACE + PlayerList[player][sC.NAME] + \
                    sC.NEW_LINE + sC.TAB + sC.NICK_ + sC.COLON + sC.SPACE + PlayerList[player][sC.STEAM_NICK]

    def get_data(self, ac):
        """
        Fetch data from Steam API

        :return: 0 for failure
        """

        url_final = self.steam_user_api_ + self.steam_api_key + pC.STEAM_API_ADDRESS + ac.read(1800)
        data_from_site = requests.get(url_final)

        file = open(self.banned_users_file_, sC.WRITE_MODE)
        file.write(str(data_from_site.text))
        file.close()

        if str(data_from_site)[11:14] != pC.MAX_USERS_TO_CHECK_FOR_BANS:
            print(pS.DOWNLOAD_ERROR_N_CODE_ + str(data_from_site))
            return 0

    @staticmethod
    def get_ip_details(steam_id):
        """
        Fetch details of IP from APIs

        :param steam_id: List of all steam IDs
        """

        url = pC.IP_API_URL
        print(lS.IP_DETAILS_FROM_.format(url))

        for steam in steam_id:
            for c_ip in steam_id[steam]:
                try:
                    _ = steam_id[steam][c_ip][sC.REGION_NAME]
                    continue
                except KeyError:
                    pass

                url_c = url + c_ip
                print(pS.FETCHING_DETAILS_OF_ + sC.COLON + sC.SPACE + c_ip)
                response = requests.get(url_c)
                resp = json.loads(response.text)
                steam_id[steam][c_ip][sC.REGION_NAME] = resp[sC.REGION_NAME]
                steam_id[steam][c_ip][sC.CITY] = resp[sC.CITY]
                steam_id[steam][c_ip][sC.ISP] = resp[sC.ISP]
                steam_id[steam][c_ip][sC.ORG] = resp[sC.ORG]
                sleep(pC.SLEEP_TIME)

        return steam_id

    def get_max(self, stat_current, ids, stats, count_matches):
        """
        Get player data with highest given stat

        :param count_matches: Dict containing matches played by teams
        :param stats: Dict containing stats for all players
        :param stat_current: Stat to find highest for
        :param ids: List of IDs not to check
        :return: Data of player with highest stat
        """

        max_stat = {stat_current: 0}

        for steam_id in stats:
            if steam_id not in ids:
                if stats[steam_id][stat_current] > max_stat[stat_current]:
                    max_stat[stat_current] = stats[steam_id][stat_current]
                    max_stat[sC.S_STEAM_ID] = steam_id

        try:
            team_name, nick_name, name_this = handler.dataHelper.get_team_nick_name_by_s_id(max_stat[sC.S_STEAM_ID])
        except KeyError:
            return

        return max_stat[sC.S_STEAM_ID], sC.PIPE + sC.SPACE + \
               str(max_stat[sC.S_STEAM_ID]).ljust(25) + sC.PIPE + \
               str(max_stat[stat_current]).center(7) + sC.PIPE + sC.SPACE + \
               name_this.ljust(30) + sC.PIPE + sC.SPACE + \
               str(count_matches[handler.dataHelper.get_clean_team_name(team_name)]) + sC.SPACE + sC.SPACE + \
               sC.PIPE + sC.SPACE + team_name.ljust(37) + sC.PIPE + \
               sC.SPACE + nick_name.ljust(40) + sC.PIPE

    def load_stats_from_local(self, matches):
        """
        Get stats from Logs stored locally

        :param matches: Dict containing all the matches played
        :return: Dict containing stats of all players
        """

        stats = {}
        for match in matches:
            for file in os.listdir(self.score_starting_ + sC.UNIX_SEPARATOR +
                                   matches[match][sC.NAME_]):

                if sC.TXT not in file:
                    continue

                with open(sC.EMPTY_RAW_STRING + self.score_starting_ + sC.UNIX_SEPARATOR +
                          matches[match][sC.NAME_] + sC.UNIX_SEPARATOR + file) as f:
                    for line in f:
                        stat = line.strip().split()

                        if stat[0] not in stats:
                            team, nick, name = handler.dataHelper.get_team_nick_name_by_s_id(stat[0])
                            stats[stat[0]] = {
                                sC.KILLS: 0,
                                sC.DEATHS: 0,
                                sC.GRENADE: 0,
                                sC.HEADSHOT: 0,
                                sC.SUICIDE: 0,
                                sC.BOMB_PLANT: 0,
                                sC.BOMB_DEFUSE: 0,
                                sC.KNIFE: 0,
                                sC.NAME_SMALL: name,
                                sC.NICK_SMALL: nick,
                            }

                        stats[stat[0]][stat[1]] += 1
        return stats

    @staticmethod
    def load_time_from_data(steam_id_):
        """
        Get Time of first and last login

        :param steam_id_: Steam Id of the player
        :return: Dict of Ips of players
        """

        ips = {}
        for steam_id in steam_id_:
            for ip in steam_id_[steam_id]:
                if ip not in ips:
                    ips[ip] = {}
                if steam_id not in ips[ip]:
                    ips[ip][steam_id] = {
                        sC.START_TIME: steam_id_[steam_id][ip][sC.START_TIME],
                        sC.END_TIME: steam_id_[steam_id][ip][sC.END_TIME],
                    }
        return ips

    def get_top_n(self, stat_current, number, stats, count_matches):
        """
        Get top players for each stat

        :param stats:
        :param count_matches:
        :param stat_current: Name of the stat
        :param number: Number of players to print
        """

        line_separator = sC.PLUS + sC.DASH * 26 + sC.PLUS + \
                         sC.DASH * 7 + sC.PLUS + sC.DASH * 31 + \
                         sC.PLUS + sC.DASH * 5 + sC.PLUS + \
                         sC.DASH * 38 + sC.PLUS + sC.DASH * 41 + \
                         sC.PLUS

        stats_header = sC.PIPE + sC.SPACE + sC.STEAM_ID.center(24) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.STATS.center(5) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.NAME_.center(29) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.M.center(3) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.T_TEAM.center(36) + \
                       sC.SPACE + sC.PIPE + sC.SPACE + sC.NICK_.center(39) + \
                       sC.SPACE + sC.PIPE

        print(line_separator)
        print(stats_header)
        print(line_separator)

        c_stat = []
        for i in range(number):
            try:
                steam_id, to_print = self.get_max(stat_current, c_stat, stats, count_matches)
            except TypeError:
                continue

            c_stat.append(steam_id)
            print(to_print)

        print(line_separator)

    def get_ip_data_from_logs(self):
        """
        Get player login from logs

        """

        steam_id = {}

        for file_ac in os.listdir(self.logs_starting_):
            print(lS.LOADING_IP_DATA_OF_.format(file_ac))
            for file_c in os.listdir(self.logs_starting_ + file_ac):
                if pS.IP_ + sC.UNDERSCORE in file_c:
                    date_c = file_c.strip().replace(pS.IP_ + sC.UNDERSCORE, sC.EMPTY_STRING) \
                        .replace(sC.TXT, sC.EMPTY_STRING)

                    with open(self.logs_starting_ + sC.UNIX_SEPARATOR + file_ac +
                              sC.UNIX_SEPARATOR + file_c, encoding=pC.ENCODING) as f_c:
                        for line_c in f_c:
                            log_c = line_c.strip().split(sC.TAB_)

                            try:
                                _ = handler.dataHelper.get_team_by_steam_id(log_c[2])
                            except TypeError:
                                continue

                            if log_c[2] not in steam_id:
                                steam_id[log_c[2]] = {}

                            if log_c[3] not in steam_id[log_c[2]]:
                                steam_id[log_c[2]][log_c[3]] = {}
                                steam_id[log_c[2]][log_c[3]][sC.START_TIME] = date_c + sC.SPACE + log_c[0]
                                steam_id[log_c[2]][log_c[3]][sC.END_TIME] = date_c + sC.SPACE + log_c[0]
                            else:
                                steam_id[log_c[2]][log_c[3]][sC.END_TIME] = date_c + sC.SPACE + log_c[0]
            return steam_id

    def get_stats_from_logs(self, match_name):
        """
        Get stats from Logs stored locally

        :param match_name: Name of the match folder
        :return: Dict of stats of given match
        """

        stats = {}
        starting_match_name = self.score_starting_ + match_name

        for blob in handler.cloudStorageHelper.get_blobs_by_prefix(starting_match_name):
            if blob.name[-1] == '/':
                continue

            b_str = blob.download_as_string().decode()

            for line in b_str.split('\n'):
                stat = line.strip().split()
                if stat.__len__() != 2:
                    continue

                try:
                    team, nick, name = handler.dataHelper.get_team_nick_name_by_s_id(stat[0])
                except TypeError:
                    print('[Exception]' + lS.NOT_FOUND_.format(stat[0]))
                    continue

                if team not in stats:
                    stats[team] = {}

                if stat[0] not in stats[team]:
                    stats[team][stat[0]] = {
                        sC.KILLS: 0,
                        sC.DEATHS: 0,
                        sC.GRENADE: 0,
                        sC.HEADSHOT: 0,
                        sC.SUICIDE: 0,
                        sC.BOMB_PLANT: 0,
                        sC.BOMB_DEFUSE: 0,
                        sC.KNIFE: 0,
                        sC.NS_NAME: name,
                        sC.NICK_SMALL: nick,
                    }

                stats[team][stat[0]][stat[1]] += 1

        print(stats)
        return stats

    def save_logs(self, match_name):
        """
        Parse various logs of the match

        :param match_name:
        """

        file_split = match_name.split()
        team_len = max(file_split[1].__len__(), file_split[3].__len__()) + 2

        logs_starting_match = self.logs_starting_ + match_name
        say_logs_txt = logs_starting_match + sC.SEPARATOR + sC.SAY_LOGS_TXT
        tmp_say_logs_txt = self.temp + sC.SAY_LOGS_TXT
        write_file = open(tmp_say_logs_txt, sC.W_PLUS_MODE, encoding=pC.ENCODING)

        say_team_logs_txt = logs_starting_match + sC.SEPARATOR + sC.SAY_TEAM_LOGS_TXT
        tmp_say_team_logs_txt = self.temp + sC.SAY_TEAM_LOGS_TXT
        write_file_team = open(tmp_say_team_logs_txt, sC.W_PLUS_MODE, encoding=pC.ENCODING)

        for blob in handler.cloudStorageHelper.get_blobs_by_prefix(logs_starting_match):
            if sC.LOG not in blob.name:
                continue

            if sC.L_ in blob.name:
                continue

            write_file.write(sC.STAR + sC.SPACE + logs_starting_match + sC.NEW_LINE)
            write_file_team.write(sC.STAR + sC.SPACE + logs_starting_match + sC.NEW_LINE)

            b_str = blob.download_as_string().decode()

            for line in b_str.split('\n'):
                if sC.SAY in line and sC.TSAY not in line:
                    line_split = line.split(sC.DOUBLE_QUOTE)

                    try:
                        pos_steam = line_split[1].index(sC.STEAM)
                    except ValueError:
                        print('[Exception]' + lS.VALUE_ERROR_.format(line_split[1]))
                        continue

                    steam_id = line_split[1][pos_steam:line_split[1].index(sC.GREATER_THAN, pos_steam)]

                    try:
                        nick = handler.dataHelper.get_username_by_steam_id(steam_id)
                    except AttributeError:
                        print('[Exception]' + lS.ATTRIBUTE_ERROR_.split(steam_id))
                        nick = steam_id

                    try:
                        team = handler.dataHelper.get_team_name_by_steam_id(steam_id)
                    except AttributeError:
                        print('[Exception]' + lS.ATTRIBUTE_ERROR_.split(steam_id))
                        team = steam_id

                    if sC.SAY_TEAM not in line:
                        write_file.write(sC.TAB + str(team).ljust(team_len) + str(nick).ljust(38) + sC.COLON +
                                         sC.SPACE + line_split[3] + sC.NEW_LINE)
                    else:
                        write_file_team.write(sC.TAB + str(team).ljust(team_len) + str(nick).ljust(38) + sC.COLON +
                                              sC.SPACE + line_split[3] + sC.NEW_LINE)

        write_file.close()
        write_file_team.close()

        handler.cloudStorageHelper.upload_file(say_logs_txt, tmp_say_logs_txt)
        handler.cloudStorageHelper.upload_file(say_team_logs_txt, tmp_say_team_logs_txt)

    def save_to_file(self, steam_id):
        """
        Save the current IP data

        :param steam_id: Steam id of the player
        """

        ip_log_starting_ = self.ip_log_starting_
        files = {}

        for team in TeamList:
            files[team] = open(ip_log_starting_ + handler.dataHelper.get_clean_team_name(TeamList[team][sC.TEAM_NAME])
                               + sC.TXT, sC.W_PLUS_MODE, encoding=pC.ENCODING)

        for steam in steam_id:
            try:
                team, nick, name = handler.dataHelper.get_team_nick_name_by_s_id(steam)
            except TypeError:
                print('[Exception] ' + lS.STEAM_ID_NOT_FOUND_.format(steam))
                continue

            files[team].write((sC.NEW_LINE + pS.PRINT_PLAYER_INFO + sC.NEW_LINE).format(name, nick, steam.strip()))

            for c_ip in steam_id[steam]:
                files[team].write(sC.TAB + str(c_ip).ljust(15) + sC.SPACE + sC.SEMI_COLON +
                                  steam_id[steam][c_ip][sC.REGION_NAME] + sC.TAB + steam_id[steam][c_ip][sC.CITY] +
                                  sC.TAB + steam_id[steam][c_ip][sC.ISP] + sC.TAB + steam_id[steam][c_ip][sC.ORG] +
                                  sC.NEW_LINE)

                for date in steam_id[steam][c_ip]:
                    if sC.DATE in date:
                        files[team].write(sC.TAB + sC.TAB + date + sC.SPACE + str(steam_id[steam][c_ip][date]) +
                                          sC.NEW_LINE)

    @staticmethod
    def init_stats():
        """
        Initial stats values to 0

        :return: Dict of stats
        """

        stats = {}

        for player in PlayerList:
            if sC.TEAM not in PlayerList[player]:
                continue
            team = PlayerList[player][sC.TEAM]
            if team not in stats:
                stats[team] = {}
            if PlayerList[player][sC.S_STEAM_ID] not in stats[team]:
                stats[team][PlayerList[player][sC.S_STEAM_ID]] = {
                    sC.KILLS: 0,
                    sC.DEATHS: 0,
                    sC.GRENADE: 0,
                    sC.HEADSHOT: 0,
                    sC.SUICIDE: 0,
                    sC.BOMB_PLANT: 0,
                    sC.BOMB_DEFUSE: 0,
                    sC.KNIFE: 0,
                    sC.MATCHES: 0,
                    sC.NAME_SMALL: PlayerList[player][sC.NAME],
                    sC.NICK_SMALL: PlayerList[player][sC.STEAM_NICK],
                }

        print(lS.WITH_FOR_EACH_PLAYER)
        return stats

    def average_stats(self, count_matches, stats):
        """
        Average all player stats by number of matches played

        :param count_matches: Number of matches played
        :param stats: Dict of stats
        """

        for steam in stats:
            for stat in stats[steam]:
                if stat == sC.NAME_SMALL or stat == sC.NICK_SMALL:
                    continue

                team = handler.dataHelper.get_team_name_by_steam_id(steam)
                clean_team_name = handler.dataHelper.get_clean_team_name(team)
                stats[steam][stat] = round(stats[steam][stat] / count_matches[clean_team_name], 1)

    @staticmethod
    def print_ip_matches(ips):
        """
        Print Ip which match with some player

        :param ips: Dict of IPs
        """

        count = 0
        for ip in ips:
            if ips[ip].__len__() > 1:
                print(ip)
                count += 1

                for steam in ips[ip]:
                    team, nick, name = handler.dataHelper.get_team_nick_name_by_s_id(steam)
                    print(sC.TAB + sC.STAR + team[:pC.TEAM_PRINT_PADDING].ljust(pC.TEAM_PRINT_PADDING),
                          name[:pC.NAME_PRINT_PADDING].ljust(pC.NAME_PRINT_PADDING),
                          nick[:pC.NICK_PRINT_PADDING].ljust(pC.NICK_PRINT_PADDING),
                          ips[ip][steam][sC.START_TIME], ips[ip][steam][sC.END_TIME], sC.TAB, steam)

        if count > 0:
            print(lS.PRINTED_IP_MATCHES)
        else:
            print(lS.NO_IP_MATCHES_FOUND)
