import socket

from commands import Commands
from storagemain import Storage


class Client:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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
            if not part:  # Если из сокета ничего не пришло, значит его закрыли с другой стороны
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
            if part_len == 0:  # Если пришёл кусок нулевой длины, то приём окончен
                return b
            b += self.readexactly(part_len)  # Считываем сам кусок

    def run(self):
        print("Connected to server")
        storage_name = self.reliable_receive().decode()
        storage = Storage(storage_name)
        storage.load()
        print("Storage name " + str(storage_name))
        while True:
            command = self.reliable_receive().decode()
            if not command:
                break
            commands = Commands()
            result = commands.execute_command(storage, command)
            print(result)
            self.reliable_send(result.encode())


if __name__ == '__main__':
    my_client = Client(socket.gethostname(), 5000)
    my_client.run()
