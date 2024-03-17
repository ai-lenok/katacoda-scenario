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
        self.file_names = set(kwargs.get("file_names", [".", "..", "file.txt", ".file.txt"]))
        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

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

        if self.check_stop_words(list(self.file_names)):
            return f'FAIL: Пожалуйста, используйте утилиту, которая подставит нужный текст, а не вводите его сами'

        self.stdout, self.stderr = self.__run_script()

        return self.check_script_output()

    def check_script_output(self):
        if not self.stdout:
            return f"FAIL: Скрипт ничего не вывел"

        real_files = set(self.stdout.split())

        if len(self.file_names) < len(real_files):
            return "FAIL: Нужно отобразить только имена файлов"

        if self.file_names == real_files:
            return "OK"

        diff_files = self.file_names - real_files

        if all([file_name[0] == "." for file_name in diff_files]):
            return "FAIL: Скрытые файлы не видны"

        return f'FAIL: Неправильный ответ: "{self.stdout}"'


if __name__ == '__main__':
    check_result = {"echo": Checker().check()}
    json_object = json.dumps(check_result)
    print(json_object)
