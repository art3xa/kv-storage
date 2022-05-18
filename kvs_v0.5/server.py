import socket


def server_program():
    host = socket.gethostname()
    port = 5000
    serv = socket.socket()
    serv.bind((host, port))
    serv.listen(100)
    conn, address = serv.accept()
    print(f"Connection from: {address}")
    storage_name = input("Please write storage name: ")
    conn.send(storage_name.encode())
    res = conn.recv(1024).decode()
    # print('Received from client: ' + res)
    print(res)
    command = input(">>> ")
    # while command.lower().strip() != 'exit':
    while True:
        conn.send(command.encode())
        result = conn.recv(1024).decode()
        if not result:
            break
        # print('Received from client: ' + result)
        print(result)
        command = input(">>> ")
    conn.close()


if __name__ == '__main__':
    server_program()
