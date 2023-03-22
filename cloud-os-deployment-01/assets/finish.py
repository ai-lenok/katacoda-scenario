#!/usr/bin/env python3

import json
import subprocess
import time

import requests


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.correct_images = ["dzx912/switch:blue", "dzx912/switch:green"]
        self.switch_to_blue = ["sh", "/root/deploy-blue.sh"]
        self.switch_to_green = ["sh", "/root/deploy-green.sh"]
        self.namespace = self.get_namespace()
        self.url_version = f"http://{self.namespace}.apps.sbc-okd.pcbltools.ru/api/v1/version"

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


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Deployment": checker.check_deployment(),
                    "Request to blue first": checker.check_switch_to_blue(),
                    "Request to green first": checker.check_switch_to_green(),
                    "Request to blue second": checker.check_switch_to_blue(),
                    "Request to green second": checker.check_switch_to_green(),
                    }
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
