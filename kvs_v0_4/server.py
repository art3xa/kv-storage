import socket
# from KV_storage_coms import *


def server_program():
    host = socket.gethostname()
    port = 5000
    serv = socket.socket()
    serv.bind((host, port))
    serv.listen(100)
    conn, address = serv.accept()
    print("Connection from: " + str(address))
    storage_name = input("Write storage name: ")
    conn.send(storage_name.encode())
    command = input("Write command: ")
    while command.lower().strip() != 'exit':
        conn.send(command.encode())
        result = conn.recv(1024).decode()
        if not result:
            break
        print('Received from client: ' + result)
        command = input("Write command: ")
    conn.close()


if __name__ == '__main__':
    server_program()
