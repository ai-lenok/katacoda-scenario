#!/usr/bin/env python3

import json
import pathlib
import subprocess


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')

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
        if not pathlib.Path(self.checking_script).is_file():
            return f'FAIL: {self.checking_script} не существует'

        self.stdout, self.stderr = self.__run_script()

        return self.check_script_00_print_hello_world()

    def check_script_00_print_hello_world(self):
        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        if self.stdout == "Hello world":
            return "OK"
        else:
            return f'FAIL: Неправильный ответ: "{self.stdout}"'


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
