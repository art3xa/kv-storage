import socket

from KV_storage_coms import *


def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print(f"Connected to server {host} {port}")
    storage_name = client_socket.recv(1024).decode()
    storage = Storage(storage_name)
    res = "Storage name " + str(storage_name)
    print(res)
    client_socket.send(res.encode())
    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)
        client_socket.send(result.encode())
        if result == 'Goodbye. Thanks for using the KV-Storage':
            exit(0)
            break
    client_socket.close()


if __name__ == '__main__':
    client_program()
