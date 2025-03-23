class ZettelError(Exception):
    pass
class ZettelNotFound(ZettelError):
    pass
class InvalidZettelFormat(ZettelError):
    pass
class ZettelAlreadyExists(ZettelError):
    pass
