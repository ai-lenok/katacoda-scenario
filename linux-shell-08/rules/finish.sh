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
        self.reference_file_names = self.__generate_reference_set(self.count_files)
        os.chdir(self.current_dir)

    @staticmethod
    def __generate_reference_set(max_files: int) -> set:
        reference = set()
        for number in range(1, max_files + 1):
            file_name = '{:02d}.txt'.format(number)
            reference.add(file_name)
        return reference

    def check(self):
        files_in_dir = [f for f in Path().iterdir()]

        count_files = len(files_in_dir)

        if count_files == 0:
            return f'FAIL: Ни одного файла нет'

        real_file_names = set([f.name for f in files_in_dir if f.is_file()])
        count_real = len(real_file_names)
        count_reference = len(self.reference_file_names)
        if count_files != count_reference:
            return f'FAIL: Неправильный количество файлов\nДолжно быть: {count_reference}\nУ вас: {count_real}'

        diff_files = self.reference_file_names - real_file_names

        if len(diff_files) != 0:
            lost_files = sorted(diff_files)
            if 4 < len(lost_files):
                text_files = ", ".join(lost_files[:4]) + ", ..."
            else:
                text_files = ", ".join(lost_files)
            return f'FAIL: Следующие файлы не найдены: {text_files}'

        return "OK"


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
