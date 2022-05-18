from modules.Commands import Commands
from modules.Storage import Storage


def main():
    """Запуск локального 'ключ-значение' хранилища"""
    storage_name = input("Write modules name: ")
    storage = Storage(storage_name)
    while True:
        command = input("Write command: ")
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)


if __name__ == '__main__':
    main()
