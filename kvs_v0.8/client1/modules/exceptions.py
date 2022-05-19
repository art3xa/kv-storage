"""Модуль содержит все возможные ошибки"""


class UsedKeyError(BaseException):
    def __init__(self, key):
        self.message = f'The key {key} is already used'

    def __str__(self):
        return self.message


class NoSuchKeyError(BaseException):
    def __init__(self, file, key):
        self.message = (f'There is no data with the '
                        f'key {key} in data file {file}')

    def __str__(self):
        return self.message


class LackOfMemoryError(BaseException):
    def __init__(self, file):
        self.message = (f'There is no memory for your data in '
                        f'data file {file} now.\n'
                        f'Delete something to add your data')

    def __str__(self):
        return self.message
