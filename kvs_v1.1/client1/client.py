import logging
import socket
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

LOGGER_NAME = 'client'
LOGGER = logging.getLogger(LOGGER_NAME)


def main():
    """Запуск клиента-хранилище"""
    try:
        stream = open('client.log', 'a')
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

        host = socket.gethostname()
        port = 5000
        sock = socket.socket()
        sock.connect((host, port))
        print(f"Connected to server {host} {port}")
        storage_name = sock.recv(1024).decode()
        if storage_name:
            storage = storagemain.Storage(storage_name)
        res = "Storage name " + str(storage_name)
        print(res)
        sock.send(res.encode())
        while True:
            command = sock.recv(1024).decode()
            if not command:
                break
            if command == "exit":
                print('Goodbye. Thanks for using the KV-Storage')
                sock.close()
                sys.exit()
            commandss = commands.Commands()
            result = commandss.execute_command(storage, command)
            print(result)
            sock.send(result.encode())
        sock.close()

    def readexactly(bytes_count: int) -> bytes:
        """
        Функция приёма определённого количества байт
        """
        b = b''
        while len(b) < bytes_count:  # Пока не получили нужное количество байт
            part = sock.recv(bytes_count - len(b))  # Получаем оставшиеся байты
            if not part:  # Если из сокета ничего не пришло, значит его закрыли с другой стороны
                raise IOError("Соединение потеряно")
            b += part
        return b

    def reliable_receive() -> bytes:
        """
        Функция приёма данных
        возвращает тип bytes
        """
        b = b''
        while True:
            part_len = int.from_bytes(readexactly(2), "big")  # Определяем длину ожидаемого куска
            if part_len == 0:  # Если пришёл кусок нулевой длины, то приём окончен
                return b
            b += readexactly(part_len)  # Считываем сам кусок


if __name__ == '__main__':
    main()
