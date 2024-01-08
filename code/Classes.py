from dataclasses import dataclass, asdict
from os import getenv


# import mariadb
# from Steam import Steam


@dataclass
class _CONFIG:
    """
    Skell for other Services Configurations
    """

    def __hash__(self) -> dict:
        return asdict(self)

    def load_envs(self) -> object:
        """
        Loads variables from environment.
        :return:
        """
        raise NotImplementedError

    def __post_init__(self):
        self = self.load_envs()


# @dataclass
# class MemcachedConf(_CONFIG):
#     """
#     Stores the configuration required for the service Memcached
#
#     hostname: str = "127.0.0.1"
#     port: int = 11211
#     username: str
#     password: str
#     """
#     hostname: str = "127.0.0.1"
#     port: int = 11211
#     username: str = None
#     password: str = None
#
#     def load_envs(self):
#         self.hostname = getenv("MEMCACHED_HOSTNAME") or self.hostname
#         self.port = getenv("MEMCACHED_PORT") or self.port
#         self.username = getenv("MEMCACHED_USERNAME") or self.username
#         self.password = getenv("MEMCACHED_PASSWORD") or self.password
#         return self


@dataclass
class DiscordConf(_CONFIG):
    """
    Stores the configuration for the Discord Bot

    token: str
    mc_url: str : Url to post on the discord embeds / messages
    prefix: str : Prefix for the commands
    description: str : Bot description to have
    """
    token: str = None
    prefix: str = "s."
    # description: str = ""
    activity: str = ""
    god_id: int = None

    def load_envs(self):
        self.token = getenv("DISCORD_TOKEN", self.token)
        self.prefix = getenv("DISCORD_PREFIX", self.prefix)
        # self.description = getenv("DISCORD_DESCRIPTION", self.description)
        self.activity = getenv("DISCORD_ACTIVITY", self.activity)
        self.activity = getenv("DISCORD_ACTIVITY", self.activity)
        self.god_id = getenv("GOD_DISCORD_ID", self.god_id)
        return self


@dataclass
class DatabaseConf(_CONFIG):
    """
    Stores the configuration required for the DatabaseServer

    host: str = "127.0.0.1"
    port: int = 5432
    username: str
    password: str
    database: str
    """
    host: str = "127.0.0.1"
    port: int = 5432
    username: str = None
    password: str = None
    database: str = None

    def load_envs(self):
        self.host = getenv("DB_HOST") or self.host
        self.port = getenv("DB_PORT") or self.port
        self.username = getenv("DB_USERNAME") or self.username
        self.password = getenv("DB_PASSWORD") or self.password
        self.database = getenv("DB_DATABASE") or self.password
        return self


@dataclass
class SteamConf(_CONFIG):
    """
    Stores the api token for Steam
    """
    token: str = None

    def load_envs(self):
        self.token = getenv("STEAM_TOKEN") or self.token
        return self


@dataclass
class ShlinkConf(_CONFIG):
    """
    Stores the API token and server URL for the Shlink service
    """
    token: str = None  # Api key
    url: str = None  # Server URL

    def load_envs(self):
        self.url = getenv("SHLINK_SERVER_URL") or self.url
        self.token = getenv("SHLINK_TOKEN") or self.token
        return self


@dataclass
class HealthCheckConf(_CONFIG):
    """
    Stores the port to host the webserver/healtcheck (8080 by default)
    """
    port: int = 8080

    def load_envs(self):
        if getenv("HEALTHCHECK_PORT"):
            self.port = int(getenv("HEALTHCHECK_PORT"))
        return self


@dataclass
class ProjectConf(_CONFIG):
    """
    Git Repo related configs.

    _repo: URL to repository page
    _wiki: URL to wiki page
    _issues: URL to issues page
    _version: Version of the bot running.
    """
    _repository: str = None
    _wiki: str = None
    _issues: str = None
    _version: str = None

    def load_envs(self):
        self._repository = getenv("REPOSITORY", self._repository)
        self._wiki = getenv("WIKI", self._wiki)
        self._issues = getenv("ISSUES", self._wiki)
        self._version = getenv("VERSION", self._version)
        return self

    @property
    def repository(self) -> str | None:
        return self._repository

    @property
    def version(self) -> str:
        return self._version or "???"

    @property
    def issues(self) -> str | None:
        if self.repository and not self._issues:
            return f'{self.repository}/issues'
        else:
            return self._issues

    @property
    def wiki(self) -> str | None:
        if self.repository and not self._wiki:
            return f'{self.repository}/wiki'
        else:
            return self._issues


# class MemcachedCli(_DBSkel):
#     __config: MemcachedConf
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#
#     def on_set(method):
#         """
#         Decorator
#         :return:
#         """
#
#         @wraps(method)
#         def wrapper(self, *args, **kwargs):
#             try:
#                 method()
#             except ConnectionError:
#                 print("Connection with memcached error!!")
#                 raise ConnectionError
#
#         return wrapper
#
#     def __set_(self, data: dict, *args, **kwargs):
#         """
#         Expected dictionary skel
#
#         {
#             DISCORD_ID: STEAM_ID,
#             DISCORD_ID2: STEAM_ID2,
#             ...
#         }
#
#         :return: result
#         """
#         print(f'[MEMCACHED] >> Inserting data')
#         # noinspection PyTypeChecker
#         bmemcache_cli = bmemcached.Client(
#             [f'{self.__config.hostname}:{self.__config.port}'],
#             username=self.__config.username,
#             password=self.__config.password)
#
#         for key, value in data.items():
#             print(f"[MEMCACHED] >>> Inserting {key}({value})")
#             bmemcache_cli.set(key, value)
#
#     def set_steam_id(self, data: dict, *args, **kwargs) -> None:
#         self.__set(data, args, kwargs)
#
#     def __get(self, key: str, *args, **kwargs) -> dict | str | int:
#
#         bmemcache_cli = bmemcached.Client(
#             [f'{self.__config.hostname}:{self.__config.port}'],
#             username=self.__config.username,
#             password=self.__config.password)
#
#         result = bmemcache_cli.get(key)
#         if not result: raise Errors.NoInsideMemcachedError
#
#         return
#
#     def get(self, key: str, *args, **kwargs) -> int | str | dict:
#         return self.__get(key, args, kwargs)


# class DBMiddleman:
#     MemcachedCli: MemcachedCli
#     DBCli: DBCli
#
#     def __init__(self, config: MemcachedConf):
#         self.MemcachedCli = MemcachedCli(config=config)
#
#     def get_memcached_query(method):
#         @wraps(method)
#         def wrapper(self, *args, **kwargs):
#             result = method(self, *args, **kwargs)
#             if not result:
#                 raise
#                 # try:
#             # except Errors.NoInsideMemcachedError as e:
#             #     cli: DBCli = self.DBCli
#             #     cli
#             # get from database and insert to memcache


class Configuration:
    """
    Object used to store/load configurations
    """
    # memcached: MemcachedConf
    steam: SteamConf
    discord: DiscordConf
    database: DatabaseConf
    shlink: ShlinkConf
    project: ProjectConf

    def __init__(self):
        # self.memcached = MemcachedConf()
        self.healtcheck = HealthCheckConf()
        self.steam = SteamConf()
        self.discord = DiscordConf()
        self.database = DatabaseConf()
        self.shlink = ShlinkConf()
        self.project = ProjectConf()
