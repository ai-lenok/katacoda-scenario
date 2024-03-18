#!/usr/bin/env python3

import json
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

        if not Path(self.path_destination).is_symlink():
            return f'FAIL: Файл "{self.path_destination}" не является ссылкой'

        return "OK"


if __name__ == '__main__':
    check_result = {"create": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
