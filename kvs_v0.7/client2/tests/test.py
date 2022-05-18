import unittest

from modules.Storage import Storage


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


if __name__ == '__main__':
    unittest.main()
