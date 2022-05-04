import json
import os.path


class Storage:
    data = {}

    def __init__(self, name):
        self.name = name

    def add(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data[key]

    def erase(self, key):
        self.data.pop(key)

    def load(self):
        if not os.path.exists(f"{self.name}.json"):
            self.save()
        with open(f"{self.name}.json", "r+") as read_file:
            self.data = json.load(read_file)

    def save(self):
        with open(f"{self.name}.json", "w") as write_file:
            json.dump(self.data, write_file)

    def change_storage(self, name):
        new_storage = Storage(name)
        new_storage.load()
        self.name = name
        self.data = new_storage.data


class Commands:
    def __init__(self):
        self.commands = {
            'add': self.add,
            'del': self.delete,
            'get': self.get,
            'save': self.save,
            'change': self.change_storage,
            'all': self.get_all,
            'clone': self.clone_storage,
            'exit': self.close_app,
        }

    def handle_command(self, command, *args):
        return self.commands[command](*args)

    def execute_command(self, storage, input_data):
        command, arg1, arg2 = self.parse_args(input_data)
        try:
            return self.handle_command(command, storage, arg1, arg2)
        except KeyError:
            return 'Unknown command'

    @staticmethod
    def add(*args):
        storage = args[0]
        key = args[1]
        value = args[2]
        try:
            storage.add(key, value)
            storage.save()
            return f"Item {value} was successfully added to KV-Storage"
        except Exception as e:
            return e

    @staticmethod
    def delete(*args):
        storage = args[0]
        key = args[1]
        try:
            value = storage.data[key]
            storage.erase(key)
            storage.save()
            return f"Key {key} was successfully deleted from KV-Storage"
        except KeyError:
            return 'Key not found'

    @staticmethod
    def get(*args):
        storage = args[0]
        key = args[1]
        try:
            return storage.get(key)
        except KeyError:
            return 'Key not found'

    @staticmethod
    def close_app(*args):
        storage = args[0]
        storage.save()
        print('Goodbye. Thanks for using the KV-Storage')
        exit(0)

    @staticmethod
    def save(*args):
        storage = args[0]
        try:
            storage.save()
            return 'Your KV-Storage is saved'
        except Exception as e:
            return e

    @staticmethod
    def change_storage(*args):
        storage = args[0]
        name = args[1]
        try:
            storage.change_storage(name)
            return f'Changed to {name} KV-Storage'
        except Exception as e:
            return e

    @staticmethod
    def get_all(*args):
        storage = args[0]
        return f"All {storage.name} KV-Storage data: " + str(storage.data)

    @staticmethod
    def clone_storage(*args):
        storage = args[0]
        try:
            new_name = storage.name + 'Clone'
            new_storage = Storage(new_name)
            new_storage.data = storage.data
            new_storage.save()
            return f"Clone {new_name} KV-Storage was created"
        except Exception as e:
            return e

    @staticmethod
    def parse_args(args):
        args = args.split(maxsplit=2)
        command = args[0]
        arg1 = None
        arg2 = None
        if len(args) == 2:
            arg1 = args[1]
        if len(args) > 2:
            arg1 = args[1]
            arg2 = args[2]
        return command, arg1, arg2


def main():
    storage_name = input("Write storage name: ")
    storage = Storage(storage_name)
    storage.load()
    while True:
        command = input("Write command: ")
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)


if __name__ == '__main__':
    main()
