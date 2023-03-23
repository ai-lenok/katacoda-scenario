#!/usr/bin/env python3

import subprocess
import time

import requests

import json


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.correct_images = ["dzx912/switch:blue", "dzx912/switch:green"]
        self.switch_to_blue = ["/root/deploy-blue.sh"]
        self.switch_to_green = ["/root/deploy-green.sh"]
        self.namespace = self.get_namespace()
        self.host = f"{self.namespace}.apps.sbc-okd.pcbltools.ru"
        self.url_version = f"http://{self.host}/api/v1/version"

    def get_namespace(self):
        self.stdout, _ = self.run(["oc", "config", "view", "-ojson"])
        try:
            info = json.loads(self.stdout)
            return info["contexts"][0]["context"]["namespace"]
        except:
            return ""

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
        command = ["oc", "get", "deployment", "-ojson"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            count_deployments = len(info["items"])
            if count_deployments == 0:
                return "FAIL: Couldn't find Deployment at all"
            if count_deployments != 2:
                return f"FAIL: Wrong number of Deployments: {count_deployments}. Two needs."

            real_images = []
            for deployment in info["items"]:
                image = deployment['spec']['template']['spec']['containers'][0]['image']
                real_images.append(image)

            for image in real_images:
                if image not in self.correct_images:
                    return f"FAIL: Image must be one of {self.correct_images}. Your images: {real_images}"

            return "OK"
        except:
            return "FAIL: Couldn't find Deployment at all."

    def check_ingress(self):
        command = ["oc", "get", "ingress", "-ojson"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            count_ingress = len(info["items"])
            if count_ingress == 0:
                return "FAIL: Couldn't find Ingress at all"
            if 1 < count_ingress:
                return f"FAIL: Too many Ingress: {count_ingress}. One needs."

            host = info["items"][0]["spec"]["rules"][0]["host"]
            if self.host == host:
                return "OK"
            else:
                return f"FAIL: Wrong ingress host. Must be: '{self.host}'. Actual: '{host}'"
        except:
            return "FAIL: Couldn't find Ingress at all."

    def check_switch_to_blue(self):
        self.run(self.switch_to_blue)
        time.sleep(10)
        res = requests.get(self.url_version)
        if res.text == "blue":
            return "OK"
        else:
            return f"FAIL: Must be 'blue'. Wrong answer from server: {res.text}"

    def check_switch_to_green(self):
        self.run(self.switch_to_green)
        time.sleep(10)
        res = requests.get(self.url_version)
        if res.text == "green":
            return "OK"
        else:
            return f"FAIL: Must be 'green'. Wrong answer from server: {res.text}"


def print_result(dict_result):
    json_object = json.dumps(dict_result, indent=4)
    print(json_object)


if __name__ == '__main__':
    checker = Checker()
    checker_list = [{"key": "Deployment", "func": checker.check_deployment},
                    {"key": "Ingress", "func": checker.check_ingress},
                    {"key": "Request to blue first", "func": checker.check_switch_to_blue},
                    {"key": "Request to green first", "func": checker.check_switch_to_green},
                    {"key": "Request to blue second", "func": checker.check_switch_to_blue},
                    {"key": "Request to green second", "func": checker.check_switch_to_green}]

    check_result = {}
    for check in checker_list:
        result = check["func"]()
        check_result[check["key"]] = result
        if result != "OK":
            break

    print_result(check_result)
