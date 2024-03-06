#!/usr/bin/env python3

import json
import pathlib
import subprocess
import os


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.path = f'/home/ubuntu/script.sh'

    def __run_script(self):
        subprocess.run(['chmod', '+x', self.path])
        process = subprocess.run([self.path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def debug(self):
        return f"FAIL: {os.getcwd()}"

    def check(self):
        if not pathlib.Path(self.path).is_file():
            return f'FAIL: {self.path} не существует'

        self.stdout, self.stderr = self.__run_script()

        return self.check_script_00_print_hello_world()

    def check_script_00_print_hello_world(self):
        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        if self.stdout == "Hello world":
            return "OK"
        else:
            return f"FAIL: Неправильный ответ: {self.stdout}"


if __name__ == '__main__':
    check_result = {"echo": Checker().debug()}
    json_object = json.dumps(check_result)
    print(json_object)
