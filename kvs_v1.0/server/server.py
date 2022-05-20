import ast
import socket
import threading

conns = []
stop = False


def main():
    """Запуск сервера - центра клиентов"""
    host = socket.gethostname()
    port = 5000
    serv = socket.socket()
    serv.bind((host, port))
    serv.listen(100)
    global conns

    def sender():
        """Отправляет команды клиентам"""
        global stop
        while not stop:
            global conns
            message = input(">>> ")
            if message == 'exit':
                stop = True
                serv.close()
                break
            commands = message.split(maxsplit=2)
            if commands[0] == 'add':
                add(message)
            elif commands[0] == 'get' or commands[0] == 'del':
                get_and_delete(message)
            elif commands[0] == 'exists':
                exists(message)
            elif commands[0] == 'save' or commands[0] == 'change' \
                    or commands[0] == 'clone':
                save_change_clone(message)
            elif commands[0] == 'keys' or commands[0] == 'values':
                keys_values(message)
            elif commands[0] == 'all':
                get_all(message)
            elif commands[0] == 'size':
                size(message)
            else:
                for i in range(len(conns)):
                    conns[i].send(message.encode())
                for j in range(len(conns)):
                    try:
                        data = conns[j].recv(1024)
                        if data:
                            print(data.decode())
                    except socket.error as e:
                        if e.errno == 10053:
                            conns.pop(i)
                            print("Подключено пользователй:", len(conns))
                        else:
                            raise

    def acceptor():
        """Постоянно принимает новых клиентов"""
        global stop
        while not stop:
            global conns
            conn, address = serv.accept()
            conns.append(conn)
            print(f"Connection from: {address}")
            print("Подключено пользователй:", len(conns))

    t1 = threading.Thread(target=acceptor)
    t1.start()

    storage_name = input("Please write modules name: ")
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

    def add(message):
        global conns
        sizes = {}
        for i in range(len(conns)):
            conns[i].send('size'.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    sizes[conns[j]] = int(data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        to_client = max(sizes, key=sizes.get)
        to_client.send(message.encode())
        dat = to_client.recv(1024)
        print(dat.decode())

    def get_and_delete(message):
        global conns
        gets = []
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    gets.append(data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        if not [i for i in gets if i != gets[0]]:
            print(gets[0])
        else:
            for x in gets:
                if not x.startswith('There is no data with the key'):
                    print(x)

    def exists(message):
        global conns
        exists = []
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    exists.append(data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        if not [i for i in exists if i != exists[0]]:
            print(exists[0])
        else:
            for x in exists:
                if not x.startswith('There is no key'):
                    print(x)

    def save_change_clone(message):
        global conns
        gets = []
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    gets.append(data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        if not [i for i in gets if i != gets[0]]:
            print(gets[0])

    def keys_values(message):
        global conns
        keys = []
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    new_data = data.split()
                    keys = keys + new_data
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        print(keys)

    def get_all(message):
        global conns
        all = {}
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    new_data = ast.literal_eval(data)
                    all.update(new_data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        print(all)

    def size(message):
        global conns
        size = 0
        for i in range(len(conns)):
            conns[i].send(message.encode())
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    size = size + int(data)
            except socket.error as e:
                if e.errno == 10053:
                    conns.pop(j)
                    print("Подключено пользователй:", len(conns))
                else:
                    raise
        print(size)


if __name__ == '__main__':
    main()
