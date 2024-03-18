#!/usr/bin/env python3

import json
import os
import re
import subprocess
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')
        self.reference_output = kwargs.get("reference_output",
                                           r"\s*PID\s+TTY\s+TIME\s+CMD\s+(\s+\d+\s+[\w?\/]+\s+[\d:]+\s+[\w\-\/:\(\)]+)+")
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

    def __generate_pattern(self, number_pattern: str):
        space = '\s+'
        size = f'{number_pattern}{space}'
        return re.compile(f'\s*total\s+used\s+free\s+shared\s+buff\/cache\s+available\s+'
                          f'Mem:\s+{size}{size}{size}{size}{size}{size}'
                          f'Swap:\s+{size}{size}{number_pattern}')

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

        if re.match(self.reference_output, self.stdout):
            return "OK"
        else:
            return f'FAIL: Неправильный ответ: "{self.stdout}"'


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
