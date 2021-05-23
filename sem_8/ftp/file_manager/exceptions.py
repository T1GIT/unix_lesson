class FileManagerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PassThrowRootException(FileManagerException):
    def __init__(self):
        super().__init__()


class FileNotExistsException(FileManagerException):
    def __init__(self, file):
        super().__init__(file)


class DirNotExistsException(FileManagerException):
    def __init__(self, file):
        super().__init__(file)


class NotFileException(FileManagerException):
    def __init__(self, file):
        super().__init__(file)


class NotDirException(FileManagerException):
    def __init__(self, file):
        super().__init__(file)


class IncorrectInputException(FileManagerException):
    def __init__(self, file):
        super().__init__(file)

