#!/usr/bin/env python3

import json
import re
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''

    @staticmethod
    def __run_script(command):
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check_deployment(self):
        command = ["oc", "get", "deployment", "-ojson"]
        self.stdout, self.stderr = self.__run_script(command)

        try:
            info = json.loads(self.stdout)
            count_deployments = len(info["items"])
            if count_deployments == 0:
                return "FAIL: Couldn't find Deployment at all"
            if 1 < count_deployments:
                return f"FAIL: Too many Deployments: {count_deployments}. One needs."

            deployment = info["items"][0]
            if deployment['metadata']['name'] != "addressbook":
                return f"FAIL: Wrong Deployment name: {deployment['metadata']['name']}. Must be: 'addressbook'."

            image = deployment['spec']['template']['spec']['containers'][0]['image']
            if image != 'nexus.local:5000/java-school/cloud/addressbook:1':
                return f"FAIL: Wrong Deployment image: {image}. " \
                       f"Must be: 'nexus.local:5000/java-school/cloud/addressbook:1'."

            return "OK"
        except:
            return "FAIL: Couldn't find Deployment at all."

    def check_stateful_set(self):
        command = ["oc", "get", "statefulset", "-ojson"]
        self.stdout, self.stderr = self.__run_script(command)

        try:
            info = json.loads(self.stdout)
            count_stateful_set = len(info["items"])
            if count_stateful_set == 0:
                return "FAIL: Couldn't find StatefulSet at all"
            if 1 < count_stateful_set:
                return f"FAIL: Too many StatefulSet: {count_stateful_set}. One needs."

            stateful_set = info["items"][0]
            if stateful_set['metadata']['name'] != "db":
                return f"FAIL: Wrong StatefulSet name: {stateful_set['name']}. Must be: 'addressbook'."

            image = stateful_set['spec']['template']['spec']['containers'][0]['image']
            if image != 'bitnami/postgresql:15':
                return f"FAIL: Wrong StatefulSet image: {image}. " \
                       f"Must be: 'bitnami/postgresql:15'."

            return "OK"
        except:
            return "FAIL: Couldn't find StatefulSet at all."

    def has_label(self):
        command = ["oc", "get", "pods", "--selector", "app=addressbook"]
        self.stdout, self.stderr = self.__run_script(command)

        addressbook = re.compile(r'^\s*addressbook\s+1/1')
        for line in self.stdout.split("\n"):
            if re.match(addressbook, line):
                return "OK"

        return "FAIL: Don't have label Pod."

    def check_image(self):
        command = ["oc", "get", "pods", "addressbook", "-ojson"]
        self.stdout, self.stderr = self.__run_script(command)

        try:
            info = json.loads(self.stdout)

            image_name = info["spec"]["containers"][0]["image"]

            if image_name == "nexus.local:5000/java-school/cloud/addressbook:1":
                return "OK"
            else:
                return f"FAIL: Wrong image: {image_name}"
        except:
            return "FAIL: Do not find Pod addressbook."


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Deployment": checker.check_deployment(),
                    "StatefulSet": checker.check_stateful_set()}
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
