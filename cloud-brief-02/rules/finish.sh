#!/usr/bin/env python3

import json
import pathlib
import subprocess

import requests


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.path_to_jar_file = 'target/demo-1.jar'
        self.url_test = "http://localhost:8080/api/v1/test"

    def __run_script(self, command):
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check_file_exists(self):
        if pathlib.Path(self.path_to_jar_file).exists():
            return "OK"
        else:
            return f'FAIL: Файл не существует: "{self.path_to_jar_file}"'

    def check_port(self):
        try:
            res = requests.get(self.url_test)
            if res.status_code == 200:
                return "OK"
            else:
                return "FAIL: Порт 8080 закрыт"
        except:
            return "FAIL: Порт 8080 закрыт"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"File exists": checker.check_file_exists(),
                    "Check port": checker.check_port()}
    json_object = json.dumps(check_result)
    print(json_object)
