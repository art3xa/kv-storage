#!/usr/bin/env python3
"""Консольная версия 'ключ-значение' хранилища"""

import logging
import sys

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

if sys.platform.startswith('linux'):
    pass

try:
    from modules import commands, storagemain
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '1.0'
__author__ = "Artyom Romanov"
__email__ = 'artem.romanov.03@bk.ru'

LOGGER_NAME = 'KVS'
LOGGER = logging.getLogger(LOGGER_NAME)


def main():
    """Запуск локального 'ключ-значение' хранилища"""
    try:
        stream = open('kvs.log', 'a')
    except Exception:
        stream = sys.stderr
    with stream:
        log = logging.StreamHandler(stream)
        log.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))

        for module in (sys.modules[__name__], storagemain):
            logger = logging.getLogger(module.LOGGER_NAME)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(log)

        LOGGER.info('Application started')
        storage_name = input("Write modules name: ")
        stora = storagemain.Storage(storage_name)
        while True:
            command = input("Write command: ")
            comms = commands.Commands()
            result = comms.execute_command(stora, command)
            print(result)
            if command == "exit":
                break


if __name__ == '__main__':
    main()
