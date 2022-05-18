import json
import os.path

FILE_SIZE = 100


class UsedKeyError(Exception):
    def __init__(self, key):
        self.message = f'The key {key} is already used'

    def __str__(self):
        return self.message


class BigDataError(Exception):
    def __init__(self):
        self.message = 'The data is too big to store even in empty data file'

    def __str__(self):
        return self.message


class NoSuchKeyError(Exception):
    def __init__(self, file, key):
        self.message = (f'There is no data with the '
                        f'key {key} in data file {file}')

    def __str__(self):
        return self.message


class LackOfMemoryError(Exception):
    def __init__(self, file):
        self.message = (f'There is no memory for your data in '
                        f'data file {file} now.\n'
                        f'Delete something to add your data')

    def __str__(self):
        return self.message


class Storage:
    data = {}

    def __init__(self, name):
        self.name = name
        self.empty_space = FILE_SIZE
        # if os.path.isdir(name):
        #     shutil.rmtree(name)
        self.load()

    def __iter__(self):
        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
            for key in data:
                yield key

    # @staticmethod
    # def create_storage(directory):
    #     if os.path.isdir(directory):
    #         shutil.rmtree(directory)
    #     os.mkdir(directory)
    #     with open(f"{directory}.json", "r+") as file:
    #         file.truncate(FILE_SIZE)
    #     return Storage(directory)

    def get(self, key: str):
        if key not in self:
            return str(NoSuchKeyError(self.name, key))
        return self.data[key]

    def add(self, key: str, value: str):
        if key in self:
            return str(UsedKeyError(key))
        count = len(value) + len(key) + 8
        if self.empty_space < count:
            return str(LackOfMemoryError(self.name))
        self.empty_space -= count
        self.data[key] = value
        self.save()
        return f"Item {value} was successfully added to KV-Storage"

    def delete(self, key: str):
        if key not in self:
            raise NoSuchKeyError(self.name, key)
        count = len(key) + len(self.data[key]) + 8
        self.empty_space += count
        self.data.pop(key)
        self.save()
        return f"Key {key} was successfully deleted from KV-Storage"

    # def add(self, key, value):
    #     self.data[key] = value
    #
    # def get(self, key):
    #     return self.data[key]

    def keys(self):
        return str(self.data.keys())

    def values(self):
        return str(self.data.values())

    # def erase(self, key):
    #     self.data.pop(key)

    def get_file_size(self):
        # size = os.path.getsize(f"{self.name}.json")
        return f"Size of {self.name} KV-Storage is {self.empty_space}/{FILE_SIZE}"

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
            # 'create': self.create_storage,
            'add': self.add,
            'del': self.delete,
            'get': self.get,
            'save': self.save,
            'change': self.change_storage,
            'all': self.get_all,
            'clone': self.clone_storage,
            'exit': self.close_app,
            'size': self.get_size,
            'keys': self.keys,
            'values': self.values,
        }

    def handle_command(self, command, *args):
        return self.commands[command](*args)

    def execute_command(self, storage, input_data):
        command, arg1, arg2 = self.parse_args(input_data)
        try:
            return self.handle_command(command, storage, arg1, arg2)
        except KeyError:
            return 'Unknown command'

    # @staticmethod
    # def create_storage(*args):
    #     storage =

    @staticmethod
    def add(*args):
        storage = args[0]
        key = args[1]
        value = args[2]
        try:
            return storage.add(key, value)
        except Exception as e:
            return e

    @staticmethod
    def delete(*args):
        storage = args[0]
        key = args[1]
        try:
            return storage.delete(key)
        except KeyError:
            return 'Key not found'

    @staticmethod
    def get(*args):
        storage = args[0]
        key = args[1]
        try:
            return storage.get(key)
        except KeyError:
            return (f'There is no data with the '
                    f'key {key} in data file {storage.name}')

    @staticmethod
    def keys(*args):
        storage = args[0]
        try:
            return str(storage.keys())
        except Exception as e:
            return e

    @staticmethod
    def values(*args):
        storage = args[0]
        try:
            return storage.values()
        except Exception as e:
            return e

    @staticmethod
    def close_app(*args):
        storage = args[0]
        storage.save()
        return 'Goodbye. Thanks for using the KV-Storage'

    @staticmethod
    def save(*args):
        storage = args[0]
        try:
            storage.save()
            return f'Your {storage.name} KV-Storage was successfully saved'
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
            new_name = storage.name + '-Clone'
            new_storage = Storage(new_name)
            new_storage.data = storage.data
            new_storage.save()
            return f"Clone {new_name} KV-Storage was created"
        except Exception as e:
            return e

    @staticmethod
    def get_size(*args):
        storage = args[0]
        return str(storage.get_file_size())

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
    while True:
        command = input("Write command: ")
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)


if __name__ == '__main__':
    main()
