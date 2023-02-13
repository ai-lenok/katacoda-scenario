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

        addressbook = re.compile(r'^\s*docker.io/dzx912/addressbook\s+1')
        postgres = re.compile(r'^\s*docker.io/library/postgres')
        find_addressbook = False
        find_postgres = False
        for line in self.stdout.split("\n"):
            match_ab = re.match(addressbook, line)
            match_postgres = re.match(postgres, line)
            if match_ab:
                find_addressbook = True
            if match_postgres:
                find_postgres = True

        if find_addressbook and find_postgres:
            return "OK"
        else:
            message = "FAIL: "
            if not find_addressbook:
                message += "Don't have addressbook image. "
            if not find_postgres:
                message += "Don't have postgres image. "
            return message

    def check_compose_ps(self):
        command = ["docker-compose", "ps"]
        self.stdout, self.stderr = self.__run_script(command)

        count_containers_in_compose = len(self.stdout.split("\n")) - 1
        if count_containers_in_compose == 2:
            return "OK"
        else:
            return f"FAIL: Wrong count of compose containers: {count_containers_in_compose}. Need two."

    def check_port(self):
        try:
            res = requests.get("http://localhost:8080/api/v1/addressbooks")
            if res.status_code == 200:
                return "OK"
            else:
                return "FAIL: Port does not open"
        except:
            return "FAIL: Port does not open"

    def check_db(self):
        try:
            res = requests.get("http://localhost:8080/api/v1/addressbooks")
            if res.status_code == 200:
                return "OK"
            else:
                return "FAIL: Port does not open"
        except:
            return "FAIL: Port does not open"


if __name__ == '__main__':
    checker = Checker()
    check_result = {}
    check_result["docker image"] = checker.check_image()
    check_result["docker-compose ps"] = checker.check_compose_ps()
    check_result["open port"] = checker.check_port()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
