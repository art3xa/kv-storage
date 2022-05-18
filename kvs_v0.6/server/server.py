import socket
import threading

conns = []


def main():
    host = socket.gethostname()
    port = 5000
    serv = socket.socket()
    serv.bind((host, port))
    serv.listen(100)
    global conns

    def sender():
        while True:
            global conns
            message = input(">>> ")
            if message:
                for i in range(len(conns)):
                    conns[i].send(message.encode())
            for i in range(len(conns)):
                try:
                    data = conns[i].recv(1024)
                    if data:
                        print(data.decode())
                except socket.error as e:
                    if e.errno == 10053:
                        conns.pop(i)
                        print("Подключено пользователй:", len(conns))
                    else:
                        raise

    def accepter():
        while True:
            global conns
            conn, address = serv.accept()
            conns.append(conn)
            print(f"Connection from: {address}")
            print("Подключено пользователй:", len(conns))

    t1 = threading.Thread(target=accepter)
    t1.start()

    storage_name = input("Please write source name: ")
    if storage_name:
        for i in range(len(conns)):
            conns[i].send(storage_name.encode())

    for i in range(len(conns)):
        try:
            data = conns[i].recv(1024)
            if data:
                print(data.decode())
        except socket.error as e:
            if e.errno == 10053:
                conns.pop(i)
                print("Подключено пользователй:", len(conns))
            else:
                raise

    t2 = threading.Thread(target=sender)
    t2.start()


if __name__ == '__main__':
    main()
