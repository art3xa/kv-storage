import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from modules.storagemain import Storage


class TestStorage(unittest.TestCase):

    def test_init(self):
        storage = Storage('test')
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_save(self):
        storage = Storage('test')
        storage.save()
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_add(self):
        storage = Storage('test')
        storage.add('1', '2')
        storage.save()
        self.assertEqual(storage.data, {"1": "2"})
        storage.exit()

    def test_get(self):
        storage = Storage('test')
        storage.add('2', '3')
        self.assertEqual(storage.get('2'), '3')
        storage.exit()

    def test_delete(self):
        storage = Storage('test')
        storage.add('0', '1')
        storage.delete('0')
        self.assertEqual(storage.data, {})
        storage.exit()

    def test_keys(self):
        storage = Storage('test')
        storage.add('1', '2')
        storage.add('hi', 'world')
        self.assertEqual(storage.keys(), "dict_keys(['1', 'hi'])")
        storage.exit()

    def test_values(self):
        storage = Storage('test')
        storage.add('a', 'b')
        storage.add('1', '3')
        self.assertEqual(storage.values(), "dict_values(['b', '3'])")
        storage.exit()

    def test_get_file_size(self):
        storage = Storage('test')
        storage.add('1', '23')
        self.assertEqual(
            storage.get_file_size(),
            "Size of test KV-Storage is 89/100")
        storage.exit()

    def test_change_storage(self):
        storage = Storage('test')
        storage.add('a', 'b')
        storage.change_storage('data')
        self.assertEqual(storage.data, {})
        storage.exit()


class TestFails(unittest.TestCase):

    def test_delete_exception(self):
        storage = Storage('test')
        storage.add('2', '1')
        with self.assertRaises(BaseException):
            storage.delete('1')
        storage.exit()


if __name__ == '__main__':
    unittest.main()
