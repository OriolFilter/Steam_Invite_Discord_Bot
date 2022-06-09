class NotInsideMemcachedError(Exception):
    """
    Raised when the memcached server returns no value, so we assume it isn't stored
    """


class NoConfigGivenError(Exception):
    """
    Raised when the object detected no config on init
    """
