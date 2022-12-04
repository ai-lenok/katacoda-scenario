#!/usr/bin/env python3

import json
import sys
import subprocess
import pathlib
import re


class Checker:
    def __init__(self, script_name):
        self.stdout = ''
        self.stderr = ''
        self.script_name = script_name
        self.path = f'/root/{script_name}'

        method_name = 'check_script_' + script_name[:2]
        self.check_method = getattr(self, method_name, self.__default_method)

    def __default_method(self):
        return f'FAIL: Unknown script {self.script_name}'

    def __run_script(self):
        subprocess.run(['chmod', '+x', self.path])
        process = subprocess.run([self.path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def __check_stop_words(self, words):
        """
        Проверяем, что не используем команду echo или printf
        :param path: Путь к проверяемому файлу
        :return: True - используется, False - не используется
        """
        with open(self.path, mode='r') as fid:
            text_file = fid.read()
            for w in words:
                if w in text_file:
                    return True

        return False

    def check(self):
        if not pathlib.Path(self.path).is_file():
            return f'FAIL: {self.path} does not exist'

        self.stdout, self.stderr = self.__run_script()

        return self.check_method()

    def check_script_00(self):
        if self.stdout == "Hello world":
            return "OK"
        else:
            return "FAIL"

    def check_script_01(self):
        if self.stdout == "/usr/bin/python3":
            return "OK"
        else:
            return "FAIL"

    def check_script_02(self):
        if self.stdout.startswith('ls is'):
            return "OK"
        else:
            return "FAIL"

    def check_script_03(self):
        if re.match(r'.*[\d\.\-]*-generic.*', self.stdout):
            return "OK"
        else:
            return "FAIL"

    def check_script_04(self):
        if not self.stdout:
            return f'FAIL: You should list files'

        for word in self.stdout.split():
            if word.startswith("/usr/bin/s") and word.endswith("d"):
                pass
            else:
                return f"FAIL: The filename is incorrect: {word}"
        return "OK"


if __name__ == '__main__':
    check_result = {}
    for file_name in ["00.sh", "01.sh", "02.sh", "03.sh", "04.sh", ]:
        check_result[file_name] = Checker(file_name).check()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
