"""Модуль настроек игры"""
import configparser
import logging

__all__ = ['Settings', 'SettingsError',
           'LOGGER_NAME']

LOGGER_NAME = 'modules.settings'
LOGGER = logging.getLogger(LOGGER_NAME)


class SettingsError(Exception):
    """Ошибка в настройках"""
    pass


def _parse_int_list(name, value, items):
    result = value.split(',')
    if len(result) != items:
        LOGGER.warning('Invalid %s: "%s". Skip', name, value)
        return None
    return tuple(result)


class Settings:
    """Класс реализует доступ к настройкам"""
    _SECTIONS = ('GLOBAL',)
    _GLOBAL_KEYS = ('file_size',)
    _STR_PREFIX = 'STRINGS'

    def __init__(self, filename='settings.ini'):
        """Чтение настроек"""
        self._config = configparser.ConfigParser(default_section='')
        self._config.optionxform = str
        LOGGER.info('Reading config from "%s"', filename)
        self._config.read(filename, encoding='utf8')
        self._prepare()

    def _prepare(self):

        for section in Settings._SECTIONS:
            if section not in self._config:
                LOGGER.error('Error: section "%s" not found', section)
                raise SettingsError

        for key in self._global():
            if key not in Settings._GLOBAL_KEYS:
                LOGGER.warning('Unknown key "%s" in `GLOBAL`. Skip', key)

        for key in Settings._GLOBAL_KEYS:
            if key not in self._global():
                LOGGER.error('Error: key "%s" not found in `GLOBAL`', key)
                raise SettingsError

        self._file_size = _parse_int_list(
            'file_size', self._global()['file_size'], 1)

    def _strings(self):
        try:
            return self._config['.'.join((Settings._STR_PREFIX,))]
        except KeyError:
            return None

    def _global(self):
        return self._config['GLOBAL']

    @property
    def file_size(self):
        """Размер файлов"""
        return self._file_size

    def string(self, name):
        """Строка с названием `name`"""
        return self._strings().get(name, None)
