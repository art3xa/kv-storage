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

    def error_handling(e, index):
        if e.errno == 10053:
            conns.pop(index)
            print("Подключено пользователй:", len(conns))
        else:
            raise

    def send_messages(message):
        for conn in conns:
            conn.send(message.encode())

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
                send_messages(message)
                for j in range(len(conns)):
                    try:
                        data = conns[j].recv(1024)
                        if data:
                            print(data.decode())
                    except socket.error as e:
                        error_handling(e, j)

    def reliable_send(mess: bytes) -> None:
        """
        Функция отправки данных в сокет
        данные ожидаются сразу типа bytes
        """
        # Разбиваем передаваемые данные на куски максимальной длины 0xffff
        # (65535)
        global conns
        for chunk in (mess[_:_ + 0xffff] for _ in range(0, len(mess), 0xffff)):
            for conn in conns:
                # Отправляем длину куска (2 байта)
                conn.send(len(chunk).to_bytes(2, "big"))
                conn.send(chunk)  # Отправляем сам кусок
                # Обозначаем конец передачи куском нулевой длины
                conn.send(b"\x00\x00")

    def readexactly(bytes_count: int) -> bytes:
        """
        Функция приёма определённого количества байт
        """
        b = b''
        while len(b) < bytes_count:  # Пока не получили нужное количество байт
            part = sock.recv(bytes_count - len(b))  # Получаем оставшиеся байты
            if not part:  # Если из сокета ничего не пришло, значит
                # его закрыли с другой стороны
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
            # Определяем длину ожидаемого куска
            part_len = int.from_bytes(readexactly(2), "big")
            if part_len == 0:  # Если пришёл кусок
                # нулевой длины, то приём окончен
                return b
            b += readexactly(part_len)  # Считываем сам кусок

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
        send_messages(storage_name)

    for i in range(len(conns)):
        try:
            data = conns[i].recv(1024)
            if data:
                print(data.decode())
        except socket.error as e:
            error_handling(e, i)

    t2 = threading.Thread(target=sender)
    t2.start()

    def add(message):
        sizes = {}
        send_messages('size')
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    sizes[conns[j]] = int(data)
            except socket.error as e:
                error_handling(e, j)
        to_client = max(sizes, key=sizes.get)
        to_client.send(message.encode())
        dat = to_client.recv(1024)
        print(dat.decode())

    def get_and_delete(message):
        gets = []
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    gets.append(data)
            except socket.error as e:
                error_handling(e, j)
        if not [i for i in gets if i != gets[0]]:
            print(gets[0])
        else:
            for x in gets:
                if not x.startswith('There is no data with the key'):
                    print(x)

    def exists(message):
        exists = []
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    exists.append(data)
            except socket.error as e:
                error_handling(e, j)
        if not [i for i in exists if i != exists[0]]:
            print(exists[0])
        else:
            for x in exists:
                if not x.startswith('There is no key'):
                    print(x)

    def save_change_clone(message):
        gets = []
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    gets.append(data)
            except socket.error as e:
                error_handling(e, j)
        if not [i for i in gets if i != gets[0]]:
            print(gets[0])

    def keys_values(message):
        keys = []
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    new_data = data.split()
                    keys = keys + new_data
            except socket.error as e:
                error_handling(e, j)
        print(keys)

    def get_all(message):
        all = {}
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    new_data = ast.literal_eval(data)
                    all.update(new_data)
            except socket.error as e:
                error_handling(e, j)
        print(all)

    def size(message):
        size = 0
        send_messages(message)
        for j in range(len(conns)):
            try:
                data = conns[j].recv(1024).decode()
                if data:
                    size = size + int(data)
            except socket.error as e:
                error_handling(e, j)
        print(size)


if __name__ == '__main__':
    main()
