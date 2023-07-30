#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.deployment_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.replicas_expect = 2
        self.count_containers = 1
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
        command = ["oc", "get", "deployments", "-ojson"]
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
                return f"Неправильное количество контейнеров в Pod'е: {len(containers)}. Должно быть: {self.count_containers}."

            image_actual = containers[0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Deployments'ов в системе"

    def check_selector(self):
        if not 'app' in self.deployment['spec']['selector']['matchLabels']:
            return 'FAIL: Отсутствуют selector "app"'
        selector = self.deployment['spec']['selector']['matchLabels']
        selector_actual = selector['app']
        if selector_actual != "addressbook":
            return f'FAIL: Неправильное значение у selector "app": "{selector_actual}"'

        return "OK"

    def check_count_replicas(self):
        replicas_actual = self.deployment['spec']['replicas']
        if replicas_actual != self.replicas_expect:
            return f'FAIL: Неправильное количество Pod: {replicas_actual}. Должно быть: {self.replicas_expect}.'
        return "OK"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check deployment": checker.check_deployment()}
    if check_result["Check deployment"] == "OK":
        check_result["Check selector"] = checker.check_selector()
        check_result["Check count replicas"] = checker.check_count_replicas()
    json_object = json.dumps(check_result)
    print(json_object)
