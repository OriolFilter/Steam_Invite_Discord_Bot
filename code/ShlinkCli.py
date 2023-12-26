import requests
import json

from Classes import ShlinkConf as _ShlinkConf
import Errors


# https://api-spec.shlink.io/

class ShlinkClient:
    __config: _ShlinkConf

    def __init__(self, **kwargs):
        configuration: _ShlinkConf = kwargs.get("configuration")
        if configuration:
            self.__config = configuration
        else:
            raise Errors.NoConfigGivenError

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def _enabled(self) -> bool:
        if any(self.__config.url) and any(self.__config.token):
            return True

    def _shorten(self, longurl) -> str:
        headers = {
            "X-Api-Key": self.__config.token,
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        payload = {
            "longUrl": longurl,
            "crawlable": False,
            "forwardQuery": False,
            "findIfExists": True,
            "tags": [
                "steam-lobby"
            ],
        }

        api_response = requests.post(f'{self.__config.url}/rest/v3/short-urls', headers=headers,
                                     data=json.dumps(payload))

        if api_response.status_code != 200:
            print(f'Response code: {api_response.status_code}')
            print(f"Failed to get a URL shortener for the URL: `{longurl}`")
            print(f'Shlink server: `{self.__config.url}`')
            raise Errors.ShlinkError

        shortUrl: str = api_response.json()['shortUrl']
        return shortUrl

    def shorten(self, longurl) -> str:
        return self._shorten(longurl=longurl)
