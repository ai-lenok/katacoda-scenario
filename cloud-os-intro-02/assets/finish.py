#!/usr/bin/env python3

import re
import subprocess

import json


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

    def has_pod(self):
        command = ["oc", "get", "pods"]
        self.stdout, self.stderr = self.__run_script(command)

        addressbook = re.compile(r'^\s*addressbook\s+1/1')
        for line in self.stdout.split("\n"):
            if re.match(addressbook, line):
                return "OK"

        return "FAIL: Не нашел Pod с именем addressbook."

    def has_label(self):
        command = ["oc", "get", "pods", "--selector", "app=addressbook"]
        self.stdout, self.stderr = self.__run_script(command)

        addressbook = re.compile(r'^\s*addressbook\s+1/1')
        for line in self.stdout.split("\n"):
            if re.match(addressbook, line):
                return "OK"

        return 'FAIL: Не нашел label "app=addressbook" у Pod.'

    def check_image(self):
        command = ["oc", "get", "pods", "addressbook", "-ojson"]
        self.stdout, self.stderr = self.__run_script(command)

        try:
            info = json.loads(self.stdout)

            image_name = info["spec"]["containers"][0]["image"]

            correct_image = "nexus.local:5000/java-school/cloud/addressbook:1"

            if image_name == correct_image:
                return "OK"
            else:
                return f'FAIL: Неправильный Docker-образ: "{image_name}". Должен быть: "{correct_image}"'
        except:
            return "FAIL: Не нашел Pod с именем addressbook."


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Pod": checker.has_pod(),
                    "Label": checker.has_label(),
                    "Image": checker.check_image()}
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
