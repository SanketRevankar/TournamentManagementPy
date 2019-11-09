import pickle

from google.cloud import firestore_v1

from TournamentManagementPy import handler
from constants import StringConstants as sC
from firestore_data import PlayerData, TeamData, ServerData
from firestore_data.MatchData import MatchList


class FireStoreUtil:
    def __init__(self, config):
        """
        Initiate FireStore Util.
        This Class contains utilities for helping with FireStore operations

        :param config: Config object
        """

        self.db = firestore_v1.Client()
        self.MATCHES = u'matches'
        self.SERVERS = u'servers'
        self.PLAYERS = u'players'
        self.TEAMS = u'teams'
        self.temp = config[sC.FOLDER_LOCATIONS][sC.TEMP_APP_ENGINE_FOLDER]

        print('{} - Initialized'.format(__name__))

    def get_collection(self, collection):
        """
        Get Collection Reference by name

        :param collection: Collection Name
        :return: Collection Reference
        """

        return self.db.collection(collection)

    def get_doc_by_id_collection(self, collection_name, document_id):
        """
        Get Document Reference by id and collection name

        :param collection_name: Collection Name
        :param document_id: Id of the document
        :return: Document Reference
        """

        return self.get_collection(collection_name).document(document_id)

    def get_team_ref_by_team_id(self, team_id):
        """
        Get Team Reference by team id

        :param team_id: Team id
        :return: Team Reference
        """

        return self.get_doc_by_id_collection(self.TEAMS, team_id)

    def get_player_ref_by_player_id(self, player_id):
        """
        Get Player Reference by team id

        :param player_id: Player id
        :return: Player Reference
        """

        return self.get_doc_by_id_collection(self.PLAYERS, player_id)

    def update_document(self, collection, document, update_dict):
        """
        Function to update a Document using Collection Name, Document id and Dict Object to update

        :param collection: Collection Name
        :param document: Document id
        :param update_dict: Dict Object to update
        """

        self.db.collection(collection).document(document).update(update_dict)

    def clear_join_team_for_player(self, player_id):
        """
        Clear Join Team in FireStore for player with given id

        :param player_id: Id of the Player
        :return: Join Team Array before clearing it
        """

        player_ref = self.get_player_ref_by_player_id(player_id)
        join_team = player_ref.get(['join_team']).get('join_team')
        player_ref.update({'join_team': []})
        return join_team

    def remove_player_id_from_all_teams_requests(self, join_team, player_id):
        """
        Remove Player Id from Join Requests based on Join Team array of the player

        :param join_team: Join Team array of the player
        :param player_id: Id of the Player
        """

        for team in join_team:
            team_ref_cur = self.get_team_ref_by_team_id(team)
            players_cur = team_ref_cur.get(['join_requests']).get('join_requests')
            players_cur.remove(player_id)
            team_ref_cur.update({'join_requests': players_cur})

    def fsh_get_teams(self):
        """
        Get team data from FireStore

        :return: Team data as Dict Object
        """

        docs = self.db.collection(self.TEAMS).stream()
        teams = {}
        for doc in docs:
            teams[doc.id] = doc.to_dict()

        return teams

    def fsh_get_servers(self):
        """
        Get servers data from FireStore

        :return: Servers data as Dict Object
        """

        docs = self.db.collection(self.SERVERS).stream()
        servers = {}
        for doc in docs:
            servers[doc.id] = doc.to_dict()

        return servers

    def fsh_get_players(self):
        """
        Get players data from FireStore

        :return: Players data as Dict Object
        """

        docs = self.db.collection(self.PLAYERS).stream()
        players = {}
        for doc in docs:
            players[doc.id] = doc.to_dict()

        return players

    def fsh_get_player_data_by_id(self, player_id):
        """
        Get Player Data as Dict Object using Player Id

        :param player_id: Id of the Player
        :return: Player Data as Dict Object
        """

        return self.get_player_ref_by_player_id(player_id).get().to_dict()

    def fsh_get_team_data_by_id(self, team_id):
        """
        Get Team Data as Dict Object using Team Id

        :param team_id: Id of the Team
        :return: Team Data as Dict Object
        """

        return self.get_team_ref_by_team_id(team_id).get().to_dict()

    def fsh_get_team_id_by_player_id(self, player_id):
        """
        Get Team Id using Player Id if Player is in a Team or else return None

        :param player_id: Id of the Player
        :return: Id of the Team or None
        """

        try:
            return self.get_player_ref_by_player_id(player_id).get(['team']).get('team')
        except KeyError:
            return None

    def get_join_team_for_player_id(self, player_id):
        """
        Get Join Team array of a player using id

        :param player_id: Id of the Player
        :return: Join Team array
        """

        return self.get_player_ref_by_player_id(player_id).get(['join_team']).get('join_team')

    def get_join_requests_by_team_id(self, team_id):
        """
        Get Join Requests array of a team using id

        :param team_id: Id of the Team
        :return: Join Requests array
        """

        return self.get_team_ref_by_team_id(team_id).get(['join_requests']).get('join_requests')

    def load_player_data(self):
        """
        Load Player Data from Cloud Storage if exists or load from FireStore and Save to Cloud Storage
        PlayerList -> Save Player Data Dict Object
        SteamList -> Mapping from Steam Id to Player Id

        :return: None
        """

        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/player_list.pk')
        steam_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/steam_list.pk')
        if player_data_blob.exists() and steam_data_blob.exists():
            PlayerData.PlayerList.update(pickle.loads(player_data_blob.download_as_string()))
            PlayerData.SteamList.update(pickle.loads(steam_data_blob.download_as_string()))
            return

        print('Loading Player List from FireStore')
        collection_ref = self.get_collection(self.PLAYERS)
        docs = collection_ref.stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            if 'steam_id' not in doc_dict or 'team' not in doc_dict:
                continue
            PlayerData.PlayerList[doc.id] = doc_dict
            PlayerData.SteamList[doc_dict['steam_id']] = doc.id

        file_path = self.temp + 'player_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(PlayerData.PlayerList, f)
        handler.cloudStorageHelper.upload_file('resources/player_list.pk', file_path)

        file_path = self.temp + 'steam_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(PlayerData.SteamList, f)
        handler.cloudStorageHelper.upload_file('resources/steam_list.pk', file_path)

    def load_team_data(self):
        """
        Load Team Data from Cloud Storage if exists or load from FireStore and Save to Cloud Storage
        TeamList -> Save Team Data Dict Object

        :return: None
        """

        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/team_list.pk')
        if player_data_blob.exists():
            TeamData.TeamList.update(pickle.loads(player_data_blob.download_as_string()))
            return

        print('Loading Team List from FireStore')
        collection_ref = self.get_collection(self.TEAMS)
        docs = collection_ref.stream()
        for doc in docs:
            TeamData.TeamList[doc.id] = doc.to_dict()

        file_path = self.temp + 'team_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(TeamData.TeamList, f)

        handler.cloudStorageHelper.upload_file('resources/team_list.pk', file_path)

    def load_server_data(self):
        """
        Load Server Data from Cloud Storage if exists or load from FireStore and Save to Cloud Storage
        ServerList -> Save Server Data Dict Object

        :return: None
        """

        player_data_blob = handler.cloudStorageHelper.get_blob_with_path('resources/server_list.pk')
        if player_data_blob.exists():
            ServerData.ServerList.update(pickle.loads(player_data_blob.download_as_string()))
            return

        print('Loading Server List from FireStore')
        collection_ref = self.get_collection(self.SERVERS)
        docs = collection_ref.stream()
        for doc in docs:
            ServerData.ServerList[doc.id] = doc.to_dict()

        file_path = self.temp + 'server_list.pk'
        with open(file_path, 'wb+') as f:
            pickle.dump(ServerData.ServerList, f)

        handler.cloudStorageHelper.upload_file('resources/server_list.pk', file_path)

    def load_match_data(self):
        """
        Load Match Data from Cloud Storage if exists or load from FireStore and Save to Cloud Storage
        MatchList -> Save Match Data Dict Object

        """

        collection_ref = self.get_collection(self.MATCHES)
        docs = collection_ref.stream()
        for doc in docs:
            MatchList[doc.id] = doc.to_dict()

    def get_matches(self, status=None):
        """
        Get Matches Data from FireStore

        :param status: Status can be in (Completed, Started, Created) or None to get All matches
        :return: Match Data as Dict Object
        """

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
        """
        Get Match Server and HLTV Server used for Match Id

        :param match_id: Id of the Match
        :return: Match Server and HLTV Server
        """

        match_ref = self.db.collection(self.MATCHES).document(match_id)
        servers = match_ref.get(['match_server', 'hltv_server'])
        return servers.get('match_server'), servers.get('hltv_server')

    def get_match_data_by_id(self, match_id):
        """
        Get Matches Data from FireStore using Id

        :param match_id: Id of the Match
        :return: Match Data as Dict Object
        """

        match_ref = self.db.collection(self.MATCHES).document(match_id)
        return match_ref.get().to_dict()

    def check_team_with_id_exists(self, team_id):
        """
        Check if Team with given Id exists

        :param team_id: Id of the Team
        :return: True or False
        """

        for docs in self.db.collection(self.TEAMS).list_documents():
            if docs.id == team_id:
                return True
        return False
