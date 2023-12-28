class NotInsideMemcachedError(Exception):
    """
    Raised when the memcached server returns no value, so we assume it isn't stored
    """


class NoConfigGivenError(Exception):
    """
    Raised when the object detected no config on init
    """


class DiscordNotGodError(Exception):
    """
    Raised when the discord user ID that executed a command, doesn't match the `GOD ID` given on the configuration.
    Used to restrict access to users.
    """


class ShlinkError(Exception):
    """
    Failed connecting to the Shlink server or creating a short Url
    """


class ShlinkNotEnabledError(Exception):
    """
    Raised when the Shlink functionality is not enabled.
    """


class VanityUrlNotFoundError(Exception):
    """
    Raised when couldn't find the vanity url specified
    """


class SteamForbiddenError(Exception):
    """
    SteamForbidden, this could be due accessing a page without permission or the api key expired/is wrong.
    """


class SteamVisibilityNotPublic(Exception):
    """
    Raised when the Steam visibility is not set to Public.

    When the value from `communityvisibilitystate` is set to 3, means that the account is set to public visibility.
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

class DBSteamIDNotFoundError(Exception):
    """
    Raised if database returns no SteamID
    """