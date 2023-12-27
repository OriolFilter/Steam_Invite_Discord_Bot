# import discord_rpc
import json

import requests
from requests import Response
from dataclasses import dataclass, asdict
from typing import Optional
from functools import wraps
from Classes import SteamConf
import Errors


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
        if self.gameid:
            return True
        return False

    @property
    def has_public_visibility(self) -> bool:
        if self.communityvisibilitystate == 3:
            return True
        return False

    @property
    def has_lobby(self) -> bool:
        return True if self.lobbysteamid else False

    @property
    def lobby_url(self):
        return f"steam://joinlobby/{self.gameid}/{self.lobbysteamid}/{self.steamid}"


def steam_api_call(method) -> dict:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> dict:
        response: requests.request = method(self, *args, **kwargs)
        if response.status_code == 200:
            return response.json()["response"]
        elif response.status_code == 403:
            raise Errors.SteamForbiddenError
        else:
            raise Errors.UnexpectedError

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
        payload = {
            "key": self.__api_key,
            "vanityurl": vanity_url,
        }
        return requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/", params=payload)

    def get_id_from_vanity_url(self, vanity_url) -> int:
        jresponse = self.__get_id_from_vanity_url(vanity_url)
        if jresponse["success"] == 1:
            return jresponse["steamid"]
        elif jresponse["success"] == 42:
            raise Errors.VanityUrlNotFoundError
        else:
            raise Errors.UnexpectedError

    @steam_api_call
    def __player_summary(self, steamid: str) -> requests or dict:
        payload = {
            "key": self.__api_key,
            "steamids": int(steamid),
        }
        response: Response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params=payload)
        return response

    def player_summary(self, steamid: str) -> PlayerSummary:
        result = self.__player_summary(steamid)['players']
        if len(result) == 0:
            raise Errors.SteamIdUserNotFoundError
        summary = result[0]
        return PlayerSummary(**dict(summary))

    def is_user_playing(self, steamid) -> bool:
        return self.player_summary(steamid=steamid).is_playing
