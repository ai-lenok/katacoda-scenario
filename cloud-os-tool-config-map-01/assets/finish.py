#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.config_map_expect = "open-config"
        self.config_map_data_expect = {"APP_USER_ID": "123", "APP_HOST": "https://example.com", }

    @staticmethod
    def run(command):
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check_config_map(self):
        command = ["oc", "get", f"configmaps/{self.config_map_expect}", "-ojson"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            data = info["data"]
            result_check_configs = self.compare_dict(data, self.config_map_data_expect, "FAIL: Неправильные data:\n")

            if result_check_configs:
                return result_check_configs

            return "OK"
        except:
            return f'FAIL: Не смог найти ConfigMap "{self.config_map_expect}"'

    def compare_dict(self, actual: dict, expect: dict, prefix_msg: str) -> str:
        diff = set(expect.items()) - set(actual.items())
        if not diff:
            return ""

        fail_msg = prefix_msg
        for key in dict(diff):
            if key in actual:
                fail_msg += f'- Неправильное значение\n    ' \
                            f'"{key}": "{actual[key]}",\n    ' \
                            f'должен быть\n    ' \
                            f'"{key}": "{expect[key]}". \n'
            else:
                fail_msg += f'- Отсутствует "{key}". \n'
        return fail_msg


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check config map": checker.check_config_map(), }

    json_object = json.dumps(check_result)
    print(json_object)
