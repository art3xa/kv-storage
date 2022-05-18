from source.commands import Commands
from source.storage import Storage


def main():
    storage_name = input("Write source name: ")
    storage = Storage(storage_name)
    while True:
        command = input("Write command: ")
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)


if __name__ == '__main__':
    main()
