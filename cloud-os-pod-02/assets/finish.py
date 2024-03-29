#!/usr/bin/env python3

import json
import pathlib
import re
import subprocess


class Checker:
    def __init__(self, script_name):
        self.stdout = ''
        self.stderr = ''
        self.script_name = script_name
        self.path = f'/root/{script_name}'

        method_name = 'check_script_' + script_name[:-3].replace('-', '_')
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

    def check_script_00_print_hello_world(self):
        if self.stdout == "Hello world":
            return "OK"
        else:
            return f"FAIL: Wrong answer: {self.stdout}"

    def check_script_01_show_list_of_pods(self):
        addressbook = re.compile(r'^\s*addressbook\s+1/1')
        for line in self.stdout.split("\n"):
            if re.match(addressbook, line):
                return "OK"

        return "FAIL: Don't have addressbook Pod."

    #:: Spring Boot ::                (v3.0.1)
    def check_script_02_print_logs(self):
        spring_boot = re.compile(r'\s*::\s+Spring Boot\s+::\s+\(v\d.\d.\d\)')
        for line in self.stdout.split("\n"):
            if re.match(spring_boot, line):
                return "OK"

        return "FAIL: Do not find correct logs"

    def check_script_03_delete(self):
        if re.match(r'pod "addressbook" deleted', self.stdout):
            return "OK"
        else:
            return "FAIL"


if __name__ == '__main__':
    check_result = {}
    for file_name in ["00-print-hello-world.sh", "01-show-list-of-pods.sh", "02-print-logs.sh", "03-delete.sh", ]:
        check_result[file_name] = Checker(file_name).check()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
