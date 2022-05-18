import json
import os.path

from modules.exceptions import UsedKeyError, NoSuchKeyError, LackOfMemoryError

FILE_SIZE = 100


class Storage:
    """'Ключ-значение' хранилище"""
    data = {}

    def __init__(self, name):
        """Иницализация 'ключ-значение' хранилища"""
        self.name = name
        self.empty_space = FILE_SIZE
        self.load()

    def __iter__(self):
        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
            for key in data:
                yield key

    def add(self, key: str, value: str):
        """Добавить ключ-значение"""
        if key in self:
            return str(UsedKeyError(key))
        count = len(value) + len(key) + 8
        if self.empty_space < count:
            return str(LackOfMemoryError(self.name))
        self.empty_space -= count
        self.data[key] = value
        self.save()
        return f"Item {value} was successfully added to KV-Storage"

    def get(self, key: str):
        """Получить значение по ключу"""
        if key not in self:
            return str(NoSuchKeyError(self.name, key))
        return self.data[key]

    def delete(self, key: str):
        """Удалить ключ-значение по ключу"""
        if key not in self:
            raise NoSuchKeyError(self.name, key)
        count = len(key) + len(self.data[key]) + 8
        self.empty_space += count
        self.data.pop(key)
        self.save()
        return f"Key {key} was successfully deleted from KV-Storage"

    def keys(self):
        """Получить все ключи"""
        return str(self.data.keys())

    def values(self):
        """Получить все значения"""
        return str(self.data.values())

    def get_file_size(self):
        """Получить количество свободного места"""
        # size = os.path.getsize(f"{self.name}.json")
        return f"Size of {self.name} KV-Storage is " \
               f"{self.empty_space}/{FILE_SIZE}"

    def load(self):
        """Загрузить 'ключ-значение' хранилище"""
        if not os.path.exists(f"{self.name}.json"):
            self.save()
        with open(f"{self.name}.json", "r+") as read_file:
            self.data = json.load(read_file)

    def save(self):
        """Сохранить 'ключ-значение' хранилище"""
        with open(f"{self.name}.json", "w") as write_file:
            json.dump(self.data, write_file)

    def change_storage(self, name):
        """Сменить 'ключ-значение' хранилище на другое по названию"""
        new_storage = Storage(name)
        new_storage.load()
        self.name = name
        self.data = new_storage.data

    def exit(self):
        self.data = {}
        os.remove(f"{self.name}.json")
        self.name = None
        self.empty_space = FILE_SIZE
