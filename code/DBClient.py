from functools import wraps

from Classes import DatabaseConf as _DatabaseConf
import psycopg2
import Errors


class DBClient:
    __config: _DatabaseConf
    __client: psycopg2.connect

    def __init__(self, **kwargs):
        configuration = kwargs.get("configuration")
        if configuration:
            self.__config = configuration
        else:
            raise Errors.NoConfigGivenError

    @property
    def _connection(self):
        try:
            return psycopg2.connect(
                user=self.__config.username,
                password=self.__config.password,
                host=self.__config.host,
                port=self.__config.port,
                database=self.__config.database,
            )
        except psycopg2.Error as e:
            print(f"Error connecting to the DB: {e}")
            raise e

    def _dbquery(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except psycopg2.Error as e:
                raise e

        return wrapper

    @_dbquery
    def __set_steam_id(self, *args, **kwargs):
        with self._connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "call proc_set_relationship (%s, %s)",
                    (str(kwargs.get('discord_id')), str(kwargs.get('steam_id'))))
                cursor.close()
                connection.commit()

    def set_steam_id(self, discord_id, steam_id):
        self.__set_steam_id(discord_id=discord_id, steam_id=steam_id)

    @_dbquery
    def __unset_steam_id(self, *args, **kwargs):
        with self._connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "call proc_unset_relationship (%s)",
                    (str(kwargs.get('discord_id')),))
                cursor.close()
                connection.commit()

    def unset_steam_id(self, discord_id):
        self.__unset_steam_id(discord_id=discord_id)

    @_dbquery
    def __get_steam_id(self, discord_id):
        try:

            with self._connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select func_return_steam_id_form_discord_id(%s)",
                        (str(discord_id),))
                    row = cursor.fetchone()
                    steam_id = row[0]
            return steam_id
        except psycopg2.errors.NoDataFound:
            raise Errors.DBSteamIDNotFoundError

    def get_steam_id(self, discord_id) -> str:
        steam_id = self.__get_steam_id(discord_id=discord_id)
        return steam_id

# class doomyDBClient:
#   """
#   For testing purpouses
#   """
#     __config: _DatabaseConf
#     __client: psycopg2.connect
#
#     def __init__(self, **kwargs):
#         configuration = kwargs.get("configuration")
#         if configuration:
#             self.__config = configuration
#         else:
#             raise Errors.NoConfigGivenError
#
#     @property
#     def _connection(self):
#         return True
#
#     def _dbquery(method):
#         @wraps(method)
#         def wrapper(self, *args, **kwargs):
#             try:
#                 return method(self, *args, **kwargs)
#             except psycopg2.Error as e:
#                 raise e
#
#         return wrapper
#
#     @_dbquery
#     def __set_steam_id(self, *args, **kwargs):
#         return True
#
#     def set_steam_id(self, discord_id, steam_id):
#         self.__set_steam_id(discord_id=discord_id, steam_id=steam_id)
#
#     @_dbquery
#     def __unset_steam_id(self, *args, **kwargs):
#         return True
#
#     def unset_steam_id(self, discord_id):
#         self.__unset_steam_id(discord_id=discord_id)
#
#     @_dbquery
#     def __get_steam_id(self, discord_id):
#         steam_id=
#         return steam_id
#
#     def get_steam_id(self, discord_id) -> str:
#         steam_id = self.__get_steam_id(discord_id=discord_id)
#         return steam_id
