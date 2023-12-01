# import discord_rpc
import requests
from requests import Response
from dataclasses import dataclass, asdict
from typing import Optional
from functools import wraps
from Classes import SteamConf


# steam error codes https://partner.steamgames.com/doc/webapi_overview/responses

@dataclass
class PlayerSummary:
    steamid: int = None
    avatar: Optional[str] = None
    avatarmedium: Optional[str] = None
    avatarfull: Optional[str] = None
    avatarhash: Optional[str] = None
    commentpermission: Optional[str] = None
    communityvisibilitystate: Optional[str] = None
    gameextrainfo: Optional[str] = None
    lobbysteamid: Optional[str] = None
    gameid: Optional[int] = None
    lastlogoff: Optional[int] = None
    loccityid: Optional[int] = None
    loccountrycode: Optional[str] = None
    locstatecode: Optional[int] = None
    personaname: Optional[str] = None
    personastate: Optional[str] = None
    personastateflags: Optional[str] = None
    primaryclanid: Optional[int] = None
    profilestate: Optional[str] = None
    profileurl: Optional[str] = None
    realname: Optional[str] = None
    timecreated: Optional[int] = None

    def __dict__(self):
        return asdict(self)

    @property
    def is_playing(self) -> bool:
        return True if self.gameextrainfo else False

    @property
    def has_lobby(self) -> bool:
        return True if self.lobbysteamid else False

    @property
    def lobby_url(self):
        return f"steam://joinlobby/{self.gameid}/{self.lobbysteamid}/{self.steamid}"


class VanityUrlNotFound(Exception):
    """
    Raised when couldn't find the vanity url specified
    """


class Forbidden(Exception):
    """
    Forbidden, this could be due accessing a page without permission or the api key expired/is wrong.
    """


class UnexpectedError(Exception):
    """
    Raised when the error wasn't planned
    """


class SteamIdUserNotFoundError(Exception):
    """
    Raised when couldn't find a user by the given SteamId
    """


class PlayerNotPlayingError(Exception):
    """
    Raised when the player is not playing and wanted to obtain the invite link
    """


def steam_api_call(method) -> dict:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> dict:
        response: requests.request = method(self, *args, **kwargs)
        if response.status_code == 200:
            return response.json()["response"]
        elif response.status_code == 403:
            raise Forbidden
        else:
            raise UnexpectedError

    return wrapper


class SteamApi:
    __configuration: SteamConf

    def __init__(self, configuration: SteamConf, *args, **kwargs):
        self.__configuration = configuration

    @property
    def __api_key(self) -> str:
        return self.__configuration.token

    @steam_api_call
    def __get_id_from_vanity_url(self, vanity_url) -> requests.request:
        requests.get(
            f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.__api_key}&vanityurl={vanity_url}")

    def get_id_from_vanity_url(self, vanity_url) -> int:
        jresponse = self.__get_id_from_vanity_url(vanity_url)
        # print(jresponse)
        if jresponse["success"] == 1:
            return jresponse["steamid"]
        elif jresponse["success"] == 42:
            raise VanityUrlNotFound
        else:
            raise UnexpectedError

    @steam_api_call
    def __player_summary(self, id) -> requests or dict:
        response: Response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.__api_key}&steamids={int(id)}")
        return response

    def player_summary(self, id) -> PlayerSummary:
        result = self.__player_summary(id)['players']
        if len(result) == 0:
            raise SteamIdUserNotFoundError
        summary = result[0]
        return PlayerSummary(**dict(summary))

    def is_user_playing(self, id) -> bool:
        return self.player_summary(id=id).is_playing
