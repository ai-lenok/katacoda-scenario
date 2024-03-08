#!/usr/bin/env python3

import json
import pathlib

class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.path = kwargs.get("check_path_exists", '/home/ubuntu/dir')

    def check(self):
        if not pathlib.Path(self.path).is_dir():
            return f'FAIL: Каталог "{self.path}" не существует'

        return "OK"


if __name__ == '__main__':
    check_result = {"create": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
