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
        self.reference_output = kwargs.get("reference_output", '1783')
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

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

        if self.check_stop_words([self.reference_output]):
            return f'FAIL: Пожалуйста, посчитайте ответ с помощью арифметических операций, а не сразу вводите его'

        self.stdout, self.stderr = self.__run_script()

        return self.check_script_output()

    def check_stop_words(self, words: list):
        """
        Проверяем, что не используем команду echo или printf
        :return: True - используется, False - не используется
        """
        with open(self.checking_script, mode='r') as fid:
            text_file = fid.read()
            for w in words:
                if w in text_file:
                    return True

        return False

    def check_script_output(self):
        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        if self.stdout == self.reference_output:
            return "OK"
        else:
            return f'FAIL: Неправильный ответ: "{self.stdout}"'


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
