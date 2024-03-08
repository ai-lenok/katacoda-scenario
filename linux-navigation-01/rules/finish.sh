#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path


class Checker:
    def __init__(self, **kwargs):
        self.stdout = ''
        self.stderr = ''
        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')
        self.reference_dir = kwargs.get("reference_dir", '/home/ubuntu/dir')

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

        return self.check_script()

    def check_script(self):
        cwd = Path.cwd()
        if cwd == self.reference_dir:
            return "OK"
        else:
            return f'FAIL: Неправильная текущая директория\nДолжна быть: {self.reference_dir}\nУ вас: {cwd}'


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
