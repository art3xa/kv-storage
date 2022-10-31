"""Модуль реализует 'ключ-значение' хранилище"""

import json
import logging
import os.path

from . import exceptions

__all__ = ['Storage', 'LOGGER_NAME']
FILE_SIZE = 100
LOGGER_NAME = 'modules.storagemain'
LOGGER = logging.getLogger(LOGGER_NAME)


class PrefixTree:
    class TreeNode:
        def __init__(self, char: str = None):
            self.char = char
            self.children = {}
            self.is_word = False

    def __init__(self, words):
        self.root = PrefixTree.TreeNode()
        for word in words:
            self.add_word(word)

    def add_word(self, word: str) -> None:
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = PrefixTree.TreeNode(char)
            current = current.children[char]
        current.is_word = True

    def contains_full_word(self, word: str) -> bool:
        return self.get_node(word).is_word is True

    def starts_with(self, prefix: str) -> list:
        node = self.get_node(prefix)
        if node is None:
            return []
        return list(self.get_words(prefix[:-1], node))

    def get_words(self, prefix: str, node) -> list:
        prefix += str(node.char)
        if node.is_word:
            yield prefix
        if node.children is None:
            return
        for child_node in node.children.values():
            for word in self.get_words(prefix, child_node):
                yield word
        prefix = prefix[:-1]

    def get_node(self, prefix: str) -> TreeNode:
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current


class Storage:
    """'Ключ-значение' хранилище"""
    data = {}
    tree_keys = PrefixTree(list(data.keys()))
    tree_values = PrefixTree(list(data.values()))

    def __init__(self, name):
        """Инициализация 'ключ-значение' хранилища"""
        LOGGER.info('Initializing kv-storage file "%s"', name)
        self.name = name
        self.empty_space = FILE_SIZE
        self.load()

    def __iter__(self):
        with open(f"{self.name}.json", "r") as file:
            data = json.load(file)
            self.tree_keys = PrefixTree(list(data.keys()))
            self.tree_values = PrefixTree(list(data.values()))
            for key in data:
                yield key

    def add(self, key: str, value: str):
        """Добавить ключ-значение"""
        if key in self:
            LOGGER.warning(f'The key {key} is already used. Skip')
            return str(exceptions.UsedKeyError(key))
        count = len(value) + len(key) + 8
        if self.empty_space < count:
            LOGGER.warning(f'There is no memory for your data in '
                           f'data file "{self.name}" now. Skip')
            return str(exceptions.LackOfMemoryError(self.name))
        self.empty_space -= count
        self.data[key] = value
        self.tree_keys.add_word(key)
        self.tree_values.add_word(value)
        self.save()
        LOGGER.info(f"Item {value} was successfully added to KV-Storage")
        return f"Item {value} was successfully added to KV-Storage"

    def get(self, key: str):
        """Получить значение по ключу"""
        words = self.tree_keys.starts_with(key)
        if not words:
            LOGGER.warning(f'There is no data with the '
                           f'key "{key}" in data file "{self.name}". Skip')
            return str(exceptions.NoSuchKeyError(self.name, key))
        values = []
        for word in words:
            values.append(self.data[word])
            LOGGER.info(f'Get value {self.data[word]} from the key {word}')
        key_values = dict(zip(words, values))
        return str(key_values)

    def search(self, value: str):
        """Поиск по значению"""
        words = self.tree_values.starts_with(value)
        if not words:
            LOGGER.warning(f'There is no data with the '
                           f'value "{value}" in data file "{self.name}". Skip')
            return str(exceptions.NoSuchValueError(self.name, value))
        # values = []
        # for word in words:
        #     values.append(self.data[word])
        # key_values = dict(zip(words, values))
        return str(words)

    def delete(self, key: str):
        """Удалить ключ-значение по ключу"""
        if key not in self:
            return str(exceptions.NoSuchKeyError(self.name, key))
        count = len(key) + len(self.data[key]) + 8
        self.empty_space += count
        self.data.pop(key)
        self.save()
        self.load()
        return f'Key "{key}" was successfully deleted from KV-Storage'

    def exists(self, key: str):
        """Проверить наличие ключа"""
        if key in self:
            return f'The key "{key}" in data file "{self.name}"'
        return f'There is no key "{key}" in data file "{self.name}"'

    def keys(self):
        """Получить все ключи"""
        if not self.data.keys():
            return "[]"
        return " ".join(map(str, list(self.data.keys())))

    def values(self):
        """Получить все значения"""
        if not self.data.values():
            return "[]"
        return " ".join(map(str, list(self.data.values())))

    def all_items(self):
        return str(self.data)

    def get_file_size(self):
        """Получить количество свободного места"""
        return self.empty_space

    def load(self):
        """Загрузить 'ключ-значение' хранилище"""
        if not os.path.exists(f"{self.name}.json"):
            self.save()
        with open(f"{self.name}.json", "r+") as read_file:
            self.data = json.load(read_file)
            self.tree_keys = PrefixTree(list(self.data.keys()))
            self.tree_values = PrefixTree(list(self.data.values()))

    def save(self):
        """Сохранить 'ключ-значение' хранилище"""
        with open(f"{self.name}.json", "w") as write_file:
            json.dump(self.data, write_file)

    def change_storage(self, name):
        """Сменить 'ключ-значение' хранилище на другое по названию"""
        self.exit()
        new_storage = Storage(name)
        new_storage.load()
        self.name = name

    def exit(self):
        """Выход из 'ключ-значение' хранилища и удаление его"""
        self.data = {}
        self.tree_keys = PrefixTree(self.data.keys())
        self.tree_values = PrefixTree(self.data.values())
        os.remove(f"{self.name}.json")
        self.name = None
        self.empty_space = FILE_SIZE
