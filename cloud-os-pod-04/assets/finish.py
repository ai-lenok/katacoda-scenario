#!/usr/bin/env python3

import re
import subprocess

import json


class WrongTypeAnswerException(Exception):
    pass


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''

    def __run_script(self, command):
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

        return "FAIL: Don't have addressbook Pod."

    def has_label(self):
        command = ["oc", "get", "pods", "--selector", "app=addressbook"]
        self.stdout, self.stderr = self.__run_script(command)

        addressbook = re.compile(r'^\s*addressbook\s+1/1')
        for line in self.stdout.split("\n"):
            if re.match(addressbook, line):
                return "OK"

        return "FAIL: Don't have label Pod."

    # oc get pods addressbook -ojson | jq '.spec.containers[].image'
    def check_image(self):
        command = ["oc", "get", "pods", "addressbook", "-ojson", "|", "jq", "'.spec.containers[].image'"]
        self.stdout, self.stderr = self.__run_script(command)

        if self.stdout == "nexus.local:5000/java-school/cloud/addressbook:1":
            return "OK"
        else:
            return f"FAIL: Wrong answer: {self.stdout}"


if __name__ == '__main__':
    checker = Checker()
    check_result = {}
    check_result["Pod"] = checker.has_pod()
    check_result["Label"] = checker.has_label()
    check_result["Image"] = checker.check_image()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
