#!/usr/bin/env python3

import filecmp
import json
import os
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')
        self.path_source = kwargs.get("check_path_source", '/home/ubuntu/file.txt')
        self.path_dest = kwargs.get("check_path_dest", '/home/ubuntu/new_file.txt')
        self.reference_file = kwargs.get("reference_file", '/root/text/poem.txt')
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

    def check(self):
        if not Path(self.path_source).exists():
            return f'FAIL: Файл "{self.path_source}" перестал существовать'
        if not Path(self.path_source).is_file():
            return f'FAIL: Файл "{self.path_source}" существует, но у него неправильный тип'

        if not Path(self.path_dest).exists():
            return f'FAIL: Файл "{self.path_dest}" не существует'
        if not Path(self.path_dest).is_file():
            return f'FAIL: Файл "{self.path_dest}" существует, но у него неправильный тип'

        if not filecmp.cmp(self.path_source, self.reference_file):
            return f'FAIL: У файла "{self.path_source}" поменялось исходное состояние'

        if not filecmp.cmp(self.path_source, self.path_dest):
            return f'FAIL: У файлов разное содержание'
        return "OK"


if __name__ == '__main__':
    check_result = {"create": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
