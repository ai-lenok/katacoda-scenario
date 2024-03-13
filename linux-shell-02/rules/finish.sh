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
        self.reference_success = kwargs.get("reference_success", '0')
        self.reference_fail = kwargs.get("reference_fail", '1')

        self.command_success = kwargs.get("command_success", 'bash -c "exit 0"; \n')
        self.command_fail = kwargs.get("command_fail", 'bash -c "exit 1"; \n')

        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

    def __run_command(self, command: str):
        new_command = command
        with open(self.checking_script) as file:
            new_command += file.read()
        process = subprocess.run([new_command],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 shell=True,
                                 executable="/bin/bash")

        self.stdout = process.stdout.strip()
        self.stderr = process.stderr.strip()

    def check(self):
        if not Path(self.checking_script).is_file():
            return f'FAIL: {self.checking_script} не существует'

        self.__run_command(self.command_success)

        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        if self.reference_success != self.stdout and self.reference_fail != self.stdout:
            return f'FAIL: Неправильный ответ: "{self.stdout}"'

        if self.reference_success != self.stdout:
            return 'FAIL: Скрипт вернул ошибку, хотя был успех'

        self.__run_command(self.command_fail)

        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        if self.reference_success != self.stdout and self.reference_fail != self.stdout:
            return f'FAIL: Неправильный ответ: "{self.stdout}"'

        if self.reference_fail != self.stdout:
            return 'FAIL: Скрипт вернул успех, хотя была ошибка'

        return "OK"


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
