import pickle

from google.cloud import firestore_v1

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data import PlayerData, TeamData, ServerData
from firestore_data.MatchData import MatchList


class FireStoreUtil:
    def __init__(self, config):
        self.db = firestore_v1.Client()
        self.MATCHES = u'matches'
        self.SERVERS = u'servers'
        self.PLAYERS = u'players'
        self.TEAMS = u'teams'
        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]

        print('{} - Initialized'.format(__name__))

    def get_collection(self, collection_path):
        return self.db.collection(collection_path)

    def get_doc_by_id_collection(self, collection_name, document_id):
        return self.get_collection(collection_name).document(document_id)

    @staticmethod
    def get_full_function_name(function_name):
        return __name__ + function_name

    def get_team_ref_by_team_id(self, team_id):
        return self.get_doc_by_id_collection(self.TEAMS, team_id)

    def get_player_ref_by_player_id(self, player_id):
        return self.get_doc_by_id_collection(self.PLAYERS, player_id)

    def update_document(self, collection, document, update_dict):
        self.db.collection(collection).document(document).update(update_dict)

    def clear_join_team_for_player(self, player_id):
        player_ref = self.get_player_ref_by_player_id(player_id)
        join_team = player_ref.get(['join_team']).get('join_team')
        player_ref.update({'join_team': []})
        return join_team

    def remove_player_id_from_all_teams_requests(self, join_team, player_id):
        for team in join_team:
            team_ref_cur = self.get_team_ref_by_team_id(team)
            players_cur = team_ref_cur.get(['join_requests']).get('join_requests')
            players_cur.remove(player_id)
            team_ref_cur.update({'join_requests': players_cur})

    def fsh_get_teams(self): 
        docs = self.db.collection(self.TEAMS).stream()
        teams = {}
        for doc in docs:
            teams[doc.id] = doc.to_dict()

        return teams

    def fsh_get_servers(self):
        docs = self.db.collection(self.SERVERS).stream()
        servers = {}
        for doc in docs:
            servers[doc.id] = doc.to_dict()

        return servers

    def fsh_get_players(self):
        docs = self.db.collection(self.PLAYERS).stream()
        players = {}
        for doc in docs:
            players[doc.id] = doc.to_dict()

        return players

    def fsh_get_player_data_by_id(self, player_id):
        return self.get_player_ref_by_player_id(player_id).get().to_dict()

    def fsh_get_team_data_by_id(self, team_id):
        return self.get_team_ref_by_team_id(team_id).get().to_dict()

    def fsh_get_team_id_by_player_id(self, player_id):
        try:
            return self.get_player_ref_by_player_id(player_id).get(['team']).get('team')
        except KeyError:
            return None

    def get_join_team_for_player_id(self, player_id):
        return self.get_player_ref_by_player_id(player_id).get(['join_team']).get('join_team')

    def get_join_requests_by_team_id(self, team_id):
        return self.get_team_ref_by_team_id(team_id).get(['join_requests']).get('join_requests')

    def load_player_data(self):
        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/player_list.pk')
        steam_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/steam_list.pk')
        if player_data_blob.exists() and steam_data_blob.exists():
            PlayerData.PlayerList.update(pickle.loads(player_data_blob.download_as_string()))
            PlayerData.SteamList.update(pickle.loads(steam_data_blob.download_as_string()))
            return

        collection_ref = self.get_collection(self.PLAYERS)
        docs = collection_ref.stream()
        for doc in docs:
            PlayerData.PlayerList[doc.id] = doc.to_dict()
            PlayerData.SteamList[PlayerData.PlayerList[doc.id]['steam_id']] = doc.id

        file_path = self.temp + 'player_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(PlayerData.PlayerList, f)
        handler.cloudStorageHelper.upload_file('resources/player_list.pk', file_path)

        file_path = self.temp + 'steam_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(PlayerData.SteamList, f)
        handler.cloudStorageHelper.upload_file('resources/steam_list.pk', file_path)

    def load_team_data(self):
        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/team_list.pk')
        if player_data_blob.exists():
            TeamData.TeamList.update(pickle.loads(player_data_blob.download_as_string()))
            return

        collection_ref = self.get_collection(self.TEAMS)
        docs = collection_ref.stream()
        for doc in docs:
            TeamData.TeamList[doc.id] = doc.to_dict()

        file_path = self.temp + 'team_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(TeamData.TeamList, f)

        handler.cloudStorageHelper.upload_file('resources/team_list.pk', file_path)

    def load_server_data(self):
        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/server_list.pk')
        if player_data_blob.exists():
            ServerData.ServerList.update(pickle.loads(player_data_blob.download_as_string()))
            return

        collection_ref = self.get_collection(self.SERVERS)
        docs = collection_ref.stream()
        for doc in docs:
            ServerData.ServerList[doc.id] = doc.to_dict()

        file_path = self.temp + 'server_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(ServerData.ServerList, f)

        handler.cloudStorageHelper.upload_file('resources/server_list.pk', file_path)

    def load_match_data(self):
        collection_ref = self.get_collection(self.MATCHES)
        docs = collection_ref.stream()
        for doc in docs:
            MatchList[doc.id] = doc.to_dict()

    def get_matches(self, status=None):
        collection_ref = self.db.collection(self.MATCHES)
        if status:
            docs = collection_ref.where(u'status', u'==', status).stream()
        else:
            docs = collection_ref.stream()

        matches = {}
        for doc in docs:
            matches[doc.id] = doc.to_dict()
        return matches

    def get_servers_by_match_id(self, match_id):
        match_ref = self.db.collection(self.MATCHES).document(match_id)
        servers = match_ref.get(['match_server', 'hltv_server'])
        return servers.get('match_server'), servers.get('hltv_server')

    def get_match_data_by_id(self, match_id):
        match_ref = self.db.collection(self.MATCHES).document(match_id)
        return match_ref.get().to_dict()

    def check_team_with_id_exists(self, team_id):
        for docs in self.db.collection(self.TEAMS).list_documents():
            if docs.id == team_id:
                return True
        return False
