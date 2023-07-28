#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.deployment_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'

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

            deployment = info["items"][0]
            deployment_name_actual = deployment['metadata']['name']
            if deployment_name_actual != self.deployment_name_expect:
                return f"FAIL: Не правильное имя Deployments'а: {deployment_name_actual}. Должно быть: '{self.deployment_name_expect}'."

            image_actual = deployment['spec']['containers'][0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Не правильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Deployments'ов в системе"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check deployment": checker.check_deployment()}
    json_object = json.dumps(check_result)
    print(json_object)
