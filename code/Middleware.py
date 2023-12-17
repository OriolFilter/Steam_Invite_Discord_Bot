from Steam import SteamApi, PlayerSummary
from Classes import Configuration
from DBClient import DBClient as DBClient
# from DBClient import doomyDBClient as DBClient
from ShlinkCli import ShlinkClient


class Middleware:
    Configuration: Configuration
    SteamApi: SteamApi
    DBClient: DBClient
    ShlinkClient: ShlinkClient

    def __init__(self):
        configuration = Configuration()

        self.SteamApi = SteamApi(configuration=configuration.steam)
        self.DBClient = DBClient(configuration=configuration.database)
        self.ShlinkClient = ShlinkClient(configuration=configuration.shlink)

        self.Configuration = configuration

    def set_steam_id(self, discord_id, steam_id, *args, **kwargs):
        """
        Automatically store? Better nha?
        But how do I do confirmation :facepalm:
        """
        self.DBClient.set_steam_id(discord_id=discord_id, steam_id=steam_id)

    def unset_steam_id(self, discord_id, *args, **kwargs):
        """"
        Unlinks the accounts (aka removes the account from the DB)
        """
        self.DBClient.unset_steam_id(discord_id=discord_id)

    def set_steam_id_from_vanity(self, discord_id, vanity_url, *args, **kwargs):
        """
        Automatically store? Better nha?
        But how do I do confirmation :facepalm:
        """
        steam_id = self.SteamApi.get_id_from_vanity_url(vanity_url=vanity_url)
        self.set_steam_id(discord_id=discord_id, steam_id=steam_id)

    def get_steam_id_from_discord_id(self, discord_id, *args, **kwargs):
        steam_id = self.DBClient.get_steam_id(discord_id=discord_id)
        return steam_id

    def __get_steam_summary_steam_id(self, steam_id) -> PlayerSummary:
        return self.SteamApi.player_summary(id=steam_id)

    def __get_steam_summary_discord_id(self, discord_id) -> PlayerSummary:
        steam_id = self.get_steam_id_from_discord_id(discord_id=discord_id)
        return self.get_steam_summary(steam_id=steam_id)

    def get_steam_summary(self, *args, **kwargs) -> PlayerSummary:
        if kwargs.get('discord_id'):
            return self.__get_steam_summary_discord_id(discord_id=kwargs.get('discord_id'))
        elif kwargs.get('steam_id'):
            return self.__get_steam_summary_steam_id(steam_id=kwargs.get('steam_id'))
        raise TypeError("missing required positional argument: 'discord_id' or 'steam_id'")
