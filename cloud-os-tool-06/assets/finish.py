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
            configs = self.check_tags(data, self.config_map_data_expect)
            result_check_configs = self.tags_checking_to_text(configs, "FAIL: Неправильные data:")

            if result_check_configs:
                return result_check_configs

            return "OK"
        except:
            return f'FAIL: Не смог найти ConfigMap "{self.config_map_expect}"'

    def check_tags(self, tags_actual, tags_expect):
        dict_checking = {}
        for key, value in tags_expect.items():
            if key in tags_actual:
                if tags_actual[key] == value:
                    dict_checking[key] = {"status": "OK"}
                else:
                    dict_checking[key] = {"status": "incorrect", "value": tags_actual[key]}
            else:
                dict_checking[key] = {"status": "missing"}
        return dict_checking

    def tags_checking_to_text(self, tags_checking, fail_message_in):
        is_ok = True
        fail_msg = fail_message_in
        for key, value in tags_checking.items():
            if value["status"] != "OK":
                is_ok = False
                if value["status"] == "incorrect":
                    fail_msg += f' "{key}": "{value["value"]}".'
                if value["status"] == "missing":
                    fail_msg += f' Отсутствует "{key}".'
        if is_ok:
            return ""
        else:
            return fail_msg


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check config map": checker.check_config_map(), }

    json_object = json.dumps(check_result)
    print(json_object)
