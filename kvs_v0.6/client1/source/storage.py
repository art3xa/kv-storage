import json
import os.path

from source.exceptions import NoSuchKeyError, UsedKeyError, LackOfMemoryError

FILE_SIZE = 100


class Storage:
    data = {}

    def __init__(self, name):
        self.name = name
        self.empty_space = FILE_SIZE
        self.load()

    def __iter__(self):
        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
            for key in data:
                yield key

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

    def keys(self):
        return str(self.data.keys())

    def values(self):
        return str(self.data.values())

    def get_file_size(self):
        # size = os.path.getsize(f"{self.name}.json")
        return f"Size of {self.name} KV-Storage is " \
               f"{self.empty_space}/{FILE_SIZE}"

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
