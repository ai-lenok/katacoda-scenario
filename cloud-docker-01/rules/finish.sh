#!/usr/bin/env python3

import json
import sys
import subprocess
import pathlib
import re
import requests


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

    def check_image(self):
        command = ["docker", "image", "ls"]
        self.stdout, self.stderr = self.__run_script(command)

        inet = re.compile(r'^\s*localhost/addressbook\s+1')
        for line in self.stdout.split("\n"):
            match = re.match(inet, line)
            if match:
                return "OK"
        return f"FAIL: Does not have correct docker image"

    def check_container(self):
        command = ["docker", "container", "ls"]
        self.stdout, self.stderr = self.__run_script(command)

        inet = re.compile(r'^\s*\w*\s*localhost/addressbook:1')
        for line in self.stdout.split("\n"):
            match = re.match(inet, line)
            if match:
                return "OK"
        return f"FAIL: Does not have correct docker container"

    def check_port(self):
      res = requests.get("http://localhost:8080/api/v1/addressbooks")
      if res.status_code == 200:
        return "OK"
      else:
        return "FAIL: Port does not open"

if __name__ == '__main__':
    checker = Checker()
    check_result = {}
    check_result["docker image"] = checker.check_image()
    check_result["docker container"] = checker.check_container()
    check_result["open port"] = checker.check_port()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)