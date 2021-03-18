class BaseMathException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            super().__init__()
        else:
            super().__init__(msg)


class InvalidSizeException(BaseMathException):
    def __init__(self, msg=None):
        super().__init__(msg)
