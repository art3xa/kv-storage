import socket
import sys

from modules.Commands import Commands
from modules.Storage import Storage


def main():
    """Запуск клиента-хранилище"""
    host = socket.gethostname()
    port = 5000
    sock = socket.socket()
    sock.connect((host, port))
    print(f"Connected to server {host} {port}")
    storage_name = sock.recv(1024).decode()
    if storage_name:
        storage = Storage(storage_name)
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
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)
        sock.send(result.encode())
    sock.close()


if __name__ == '__main__':
    main()
