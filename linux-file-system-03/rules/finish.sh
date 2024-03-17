#!/usr/bin/env python3

import json
import os
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)
        self.check_dir_path = kwargs.get("check_dir", f'{self.current_dir}/dir')
        self.check_dir = Path(self.check_dir_path)

    def check(self):
        if not self.check_dir.is_dir():
            return f'FAIL: Директория "{self.check_dir}" исчезла'

        files = [f for f in self.check_dir.iterdir() if f.is_file()]
        count_files = len(files)

        if count_files == 0:
            return f'FAIL: В директории "{self.check_dir}" нет файлов'
        if 1 < count_files:
            return f'FAIL: В директории "{self.check_dir}" больше одного файла'

        if files[0].name[0] == ".":
            return "OK"
        else:
            return f'FAIL: Файл {files[0]} не скрыт'


if __name__ == '__main__':
    check_result = {"create": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
