#!/usr/bin/env python3

import json
import os
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        self.count_files = kwargs.get("count_files", 99)
        os.chdir(self.current_dir)

    def check(self):
        files = [f for f in Path().iterdir()]

        count = len(files)

        if count == 0:
            return f'FAIL: Ни одного файла нет'

        if count < self.count_files:
            return f'FAIL: Файлов слишком мало: {count}'

        if self.count_files < count:
            return f'FAIL: Файлов слишком много: {count}'

        lost_files = []
        for number in range(1, self.count_files + 1):
            file_name = '{:02d}.txt'.format(number)
            if not Path(file_name).is_file():
                lost_files.append(file_name)

        if len(lost_files) != 0:
            return f'FAIL: Следующие файлы не найдены: {lost_files}'

        return "OK"


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
