import os
import os.path


class KVStorage:
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.isfile(file_name):
            f = open(self.file_name, 'w')
            f.close()
        self.file = open(self.file_name, 'r+')
