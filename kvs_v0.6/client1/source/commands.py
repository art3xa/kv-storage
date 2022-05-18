from source.storage import Storage


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
    storage_name = input("Write source name: ")
    storage = Storage(storage_name)
    while True:
        command = input("Write command: ")
        commands = Commands()
        result = commands.execute_command(storage, command)
        print(result)


if __name__ == '__main__':
    main()
