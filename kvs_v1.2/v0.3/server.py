import socket


class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(('', port))  # IP
        self.listener.listen(0)
        listenerr = self.listener
        print('[+] Waiting for incoming connection...')
        self.connection, address = self.listener.accept()
        print('[+] Got a connection from ' + str(address))

    def reliable_send(self, data: bytes) -> None:
        """
        Функция отправки данных в сокет
        данные ожидаются сразу типа bytes
        """
        # Разбиваем передаваемые данные на куски максимальной длины 0xffff
        # (65535)
        for chunk in (data[_:_ + 0xffff] for _ in range(0, len(data), 0xffff)):
            # Отправляем длину куска (2 байта)
            self.connection.send(len(chunk).to_bytes(2, "big"))
            self.connection.send(chunk)  # Отправляем сам кусок
            # Обозначаем конец передачи куском нулевой длины
            self.connection.send(b"\x00\x00")

    def readexactly(self, bytes_count: int) -> bytes:
        """
        Функция приёма определённого количества байт
        """
        b = b''
        while len(b) < bytes_count:  # Пока не получили нужное количество байт
            part = self.connection.recv(
                bytes_count - len(b))  # Получаем оставшиеся байты
            if not part:  # Если из сокета ничего не пришло, значит
                # его закрыли с другой стороны
                raise IOError("Соединение потеряно")
            b += part
        return b

    def reliable_receive(self) -> bytes:
        """
        Функция приёма данных
        возвращает тип bytes
        """
        b = b''
        while True:
            # Определяем длину ожидаемого куска
            part_len = int.from_bytes(self.readexactly(2), "big")
            if part_len == 0:  # Если пришёл кусок нулевой
                # длины, то приём окончен
                return b
            b += self.readexactly(part_len)  # Считываем сам кусок

    def run(self):
        storage_name = input("Write storage name: ")
        self.reliable_send(storage_name.encode())
        command = input("Write command: ")
        while command.lower().strip() != 'exit':
            self.reliable_send(command.encode())
            result = self.reliable_receive().decode()
            if not result:
                break
            print('Received from client: ' + result)
            command = input("Write command: ")


my_listener = Listener(socket.gethostname(), 5000)
my_listener.run()
