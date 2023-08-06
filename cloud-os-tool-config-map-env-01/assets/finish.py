#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.deployment_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.count_containers = 1
        self.count_env = 2
        self.config_map_data_expect = {"APP_USER_ID": "123", "APP_HOST": "https://example.com", }
        self.deployment = {}

    @staticmethod
    def run(command):
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check_deployment(self):
        command = ["oc", "get", "deployments", "--output", "json"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            count_deployments = len(info["items"])
            if count_deployments == 0:
                return "FAIL: Не обнаружено Deployments'ов в системе"
            if 1 < count_deployments:
                return f"FAIL: Слишком много Deployments'ов: {count_deployments}. Должен быть один."

            self.deployment = info["items"][0]
            deployment_name_actual = self.deployment['metadata']['name']
            if deployment_name_actual != self.deployment_name_expect:
                return f"FAIL: Неправильное имя Deployments'а: {deployment_name_actual}. Должно быть: '{self.deployment_name_expect}'."

            containers = self.deployment['spec']['template']['spec']['containers']
            if len(containers) != self.count_containers:
                return f"FAIL: Неправильное количество контейнеров в Pod'е: {len(containers)}. Должно быть: {self.count_containers}."

            image_actual = containers[0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Deployments'ов в системе"

    def check_env(self):
        container = self.deployment['spec']['template']['spec']['containers'][0]
        if 'env' not in container:
            return f'FAIL: В конфигурации deployment.spec.template.spec.containers отсутствует "env".'
        env_conf = container['env']
        if len(env_conf) != self.count_env:
            return f'FAIL: В секции "env" неправильное количество настроек: {len(env_conf)}. ' \
                   f'Должно быть: {self.count_env}.'
        result_check_envs = self.compare_dict(self.list_to_map(env_conf),
                                              self.config_map_data_expect,
                                              "FAIL: Неправильные переменные окружения:\n")

        if result_check_envs:
            return result_check_envs

        return "OK"

    def compare_dict(self, actual: dict, expect: dict, prefix_msg: str) -> str:
        diff = set(expect.items()) - set(actual.items())
        if not diff:
            return ""

        fail_msg = prefix_msg
        for key in dict(diff):
            print(key)
            if key in actual:
                fail_msg += f'- Неправильное значение\n    ' \
                            f'"{key}": "{actual[key]}",\n    ' \
                            f'должен быть\n    ' \
                            f'"{key}": "{expect[key]}". \n'
            else:
                fail_msg += f'- Отсутствует {key}. \n'
        return fail_msg

    def list_to_map(self, data: list) -> dict:
        result = {}
        for d in data:
            name, value = "", ""
            if 'name' in d:
                name = d['name']
            if 'value' in d:
                value = d['value']
            if name and value:
                result[name] = value

        return result


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check deployment": checker.check_deployment()}
    if check_result["Check deployment"] == "OK":
        check_result["Check env"] = checker.check_env()
    json_object = json.dumps(check_result)
    print(json_object)
