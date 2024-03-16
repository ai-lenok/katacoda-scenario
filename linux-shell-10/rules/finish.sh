#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')
        self.reference_output = kwargs.get("reference_output", 'Hello world')
        self.count_files = kwargs.get("count_files", 100)
        self.reference_file_names = self.__generate_reference_set(self.count_files)
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

    @staticmethod
    def __generate_reference_set(max_files: int) -> set:
        reference = set()
        decimal_index = 0
        while decimal_index < max_files:
            file_name_2 = '{:03d}'.format(decimal_index + 2)
            file_name_5 = '{:03d}'.format(decimal_index + 5)
            reference.add(file_name_2)
            reference.add(file_name_5)
            decimal_index += 10
        return reference

    def __run_script(self):
        subprocess.run(['chmod', '+x', self.checking_script])
        process = subprocess.run([self.checking_script],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check(self):
        if not Path(self.checking_script).is_file():
            return f'FAIL: {self.checking_script} не существует'

        self.stdout, self.stderr = self.__run_script()

        return self.check_script_output()

    def check_script_output(self):
        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        real_file_names = set(self.stdout.split())

        count_real = len(real_file_names)
        count_reference = len(self.reference_file_names)
        if count_real != count_reference:
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
