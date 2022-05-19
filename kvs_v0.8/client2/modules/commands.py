"""Модуль содержит все возможные команды"""

from . import storagemain


class Commands(object):
    """Консольные команды"""

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
        """Добавить 'ключ-значение'"""
        storage = args[0]
        key = args[1]
        value = args[2]
        try:
            return storage.add(key, value)
        except Exception as e:
            return e

    @staticmethod
    def get(*args):
        """Получить значение по ключу"""
        storage = args[0]
        key = args[1]
        try:
            return storage.get(key)
        except KeyError:
            return (f'There is no data with the '
                    f'key {key} in data file {storage.name}')

    @staticmethod
    def delete(*args):
        """Удалить ключ-значение по ключу"""
        storage = args[0]
        key = args[1]
        try:
            return storage.delete(key)
        except KeyError:
            return 'Key not found'

    @staticmethod
    def keys(*args):
        """Получить все ключи"""
        storage = args[0]
        try:
            return str(storage.keys())
        except Exception as e:
            return e

    @staticmethod
    def values(*args):
        """Получить все значения"""
        storage = args[0]
        try:
            return storage.values()
        except Exception as e:
            return e

    @staticmethod
    def get_size(*args):
        """Получить количество свободного места"""
        storage = args[0]
        return str(storage.get_file_size())

    @staticmethod
    def close_app(*args):
        """Выйти из 'ключ-значение' хранилища"""
        storage = args[0]
        storage.save()
        return 'Goodbye. Thanks for using the KV-Storage'

    @staticmethod
    def save(*args):
        """Сохранить 'ключ-значение' хранилище"""
        storage = args[0]
        try:
            storage.save()
            return f'Your {storage.name} KV-Storage was successfully saved'
        except Exception as e:
            return e

    @staticmethod
    def change_storage(*args):
        """Сменить 'ключ-значение' хранилище на другое по названию"""
        storage = args[0]
        name = args[1]
        try:
            storage.change_storage(name)
            return f'Changed to {name} KV-Storage'
        except Exception as e:
            return e

    @staticmethod
    def get_all(*args):
        """Получить все 'ключ-значения' из хранилища"""
        storage = args[0]
        return f"All {storage.name} KV-Storage data: " + str(storage.data)

    @staticmethod
    def clone_storage(*args):
        """Клонировать выбранное 'ключ-значение' хранилище"""
        storage = args[0]
        try:
            new_name = storage.name + '-Clone'
            new_storage = storagemain.Storage(new_name)
            new_storage.data = storage.data
            new_storage.save()
            return f"Clone {new_name} KV-Storage was created"
        except Exception as e:
            return e

    @staticmethod
    def parse_args(args):
        """Распарсить команду"""
        args = args.split(maxsplit=2)
        if len(args) == 0:
            command = None
        else:
            command = args[0]
        arg1 = None
        arg2 = None
        if len(args) == 2:
            arg1 = args[1]
        if len(args) > 2:
            arg1 = args[1]
            arg2 = args[2]
        return command, arg1, arg2
