from devvio_util.exceptions import DevvError


class DBError(DevvError):
    def __init__(self, message="Database exception"):
        super().__init__(message)
