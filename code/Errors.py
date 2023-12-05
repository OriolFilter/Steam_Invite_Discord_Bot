class NotInsideMemcachedError(Exception):
    """
    Raised when the memcached server returns no value, so we assume it isn't stored
    """


class NoConfigGivenError(Exception):
    """
    Raised when the object detected no config on init
    """


class ShlinkError(Exception):
    """
    Failed connecting to the Shlink server or creating a short Url
    """


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

