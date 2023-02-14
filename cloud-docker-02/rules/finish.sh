#!/usr/bin/env python3

import json
import subprocess
import re
import time

import requests


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
            return f"FAIL: Wrong count of compose containers: {count_containers_in_compose}. Two needed."

    def check_port(self):
        try:
            res = requests.get("http://localhost:8080/api/v1/addressbooks")
            if type(res.json()) != list:
                return f"FAIL: Application returned bad answer. {res.json()}"
            if res.status_code == 200:
                return "OK"
            else:
                return "FAIL: Port 8080 does not open"
        except:
            return "FAIL: Port 8080 does not open"

    def check_db(self):
        try:
            rows_start = self.__count_rows()
            need_rows_after_put = rows_start + 1

            self.__add_row()
            rows_added = self.__count_rows()

            if need_rows_after_put != rows_added:
                return f'FAIL: Before saving rows: {rows_start}, after: {rows_added}. ' \
                       f'{need_rows_after_put} needs after saving.'
        except requests.exceptions.RequestException:
            return "FAIL: Port 8080 does not open"
        except WrongTypeAnswerException as e:
            return f"FAIL: Application returned bad answer: {e}"

        return self.__check_after_restarting(rows_added)

    def __check_after_restarting(self, rows_expected):
        try:
            self.__restart_compose()
            time.sleep(5)

            rows_end = self.__count_rows()

            if rows_expected == rows_end:
                return "OK"
            else:
                return f'FAIL: Before restarting rows: {rows_expected}, after: {rows_end}. ' \
                       f'They must be equal to each other.'
        except requests.exceptions.RequestException:
            return "FAIL: Port 8080 does not open after restarting docker-compose"
        except WrongTypeAnswerException as e:
            return f"FAIL: Application returned bad answer: {e}"

    def __add_row(self):
        data = {"firstName": "Ivan", "lastName": "Ivanov", "phone": "+79999999999", "birthday": "2000-01-01"}
        requests.post("http://localhost:8080/api/v1/addressbook", json=data)

    def __count_rows(self):
        addressbooks = requests.get("http://localhost:8080/api/v1/addressbooks")
        if type(addressbooks.json()) != list:
            raise WrongTypeAnswerException(addressbooks.json())
        return len(addressbooks.json())

    def __restart_compose(self):
        self.__run_script(["docker-compose", "down"])
        self.__run_script(["docker-compose", "up", "-d"])


if __name__ == '__main__':
    checker = Checker()
    check_result = {}
    check_result["docker image"] = checker.check_image()
    check_result["docker-compose ps"] = checker.check_compose_ps()
    check_result["open port"] = checker.check_port()
    check_result["storage"] = checker.check_db()
    json_object = json.dumps(check_result, indent=4)
    print(json_object)
