#!/usr/bin/env python3

import json
import os
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.path_source = kwargs.get("path_source", '/home/ubuntu/file.txt')
        self.path_destination = kwargs.get("path_destination", '/home/ubuntu/link-file.txt')

    def check(self):
        if not Path(self.path_source).is_file():
            return f'FAIL: Файл "{self.path_source}" исчез'

        if not Path(self.path_destination).is_file():
            return f'FAIL: Файл "{self.path_destination}" не существует'

        if Path(self.path_destination).is_symlink():
            return f'FAIL: Файл "{self.path_destination}" является мягкой ссылкой'

        if os.stat(self.path_source).st_ino == os.stat(self.path_destination).st_ino:
            return "OK"
        else:
            return f'FAIL: Файл "{self.path_destination}" не является ссылкой'


if __name__ == '__main__':
    check_result = {"create": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
