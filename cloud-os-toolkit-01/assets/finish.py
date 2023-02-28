#!/usr/bin/env python3

import json
import re
import subprocess
import time


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.command_run_rows_checker = ["oc", "apply", "--filename", "/usr/lib/checker/python-checker.yaml"]
        self.command_clean_rows_checker = ["oc", "delete", "--filename", "/usr/lib/checker/python-checker.yaml"]
        self.rows_before_restart = -1

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
        self.stdout, _ = self.run(command)

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

    def check_rows(self):
        self.clear_pod_check_rows()
        self.wait_addressbook_available()
        self.run(self.command_run_rows_checker)
        try:
            for i in range(60):
                time.sleep(1)

                self.stdout, _ = self.run(["oc", "logs", "check-rows"])
                if self.stdout:
                    info = json.loads(self.stdout)
                    return self.check_result_after_adding_row(info)
        except:
            return "FAIL: Couldn't get answer from addressbook"
        return "FAIL: Couldn't get answer from addressbook"

    def check_result_after_adding_row(self, info):
        self.run(self.command_clean_rows_checker)

        if not info['before']['status']:
            return "FAIL: Couldn't get answer from addressbook"

        self.rows_before_restart = info['after']['size']

        if self.rows_before_restart != info['after']['size']:
            return f"FAIL: Before add rows: {info['before']['size']}, after: {info['after']['size']}. " \
                   f"It must be: {info['before']['size']} and {info['before']['size'] + 1}"

        return "OK"

    def clear_pod_check_rows(self):
        if self.has_pod_check_rows():
            self.run(self.command_clean_rows_checker)
            for i in range(10):
                if self.has_pod_check_rows():
                    time.sleep(1)
                else:
                    return

    def has_pod_check_rows(self):
        self.stdout, _ = self.run(["oc", "get", "pods", "check-rows"])
        return not self.stdout.startswith('Error from server (NotFound)')

    def wait_addressbook_available(self):
        for i in range(60):
            if not self.addressbook_is_available():
                time.sleep(1)
            else:
                return

    def addressbook_is_available(self):
        names, status = self.get_pods_name()
        if not status:
            return False

        for name in names:
            self.stdout, _ = self.run(["oc", "logs", name])
            is_started = re.findall(r"Started AddressbookApplication in", self.stdout)
            if not is_started:
                return False
        return True

    def check_pods_by_selector(self):
        names, status = self.get_pods_name()
        if not status:
            return "FAIL: Couldn't find Pods by selector 'app=addressbook'"
        if len(names) != 2:
            return f"FAIL: Wrong number of Pods by selector 'app=addressbook': {len(names)}. Two needs."
        return "OK"

    def check_pod_drops(self):
        self.run(["oc", "delete", "pods", "--selector", "app=addressbook"])
        self.wait_addressbook_available()
        self.clear_pod_check_rows()

        self.run(self.command_run_rows_checker)
        try:
            for i in range(60):
                time.sleep(1)

                self.stdout, _ = self.run(["oc", "logs", "check-rows"])
                if self.stdout:
                    info = json.loads(self.stdout)
                    return self.check_result_after_restart_pods(info)
        except:
            return "FAIL: Couldn't get answer from addressbook"
        return "FAIL: Couldn't get answer from addressbook"

    def check_result_after_restart_pods(self, info):
        self.run(self.command_clean_rows_checker)
        if not info['before']['status']:
            return "FAIL: Couldn't get answer from addressbook after Pods drops"

        if self.rows_before_restart != info['before']['size']:
            return f"FAIL: There was {self.rows_before_restart} rows before the Pod drops. " \
                   f"Now there are: {info['before']['size']}. It must be equals."

        if info['before']['size'] + 1 != info['after']['size']:
            return f"FAIL: Before add rows: {info['before']['size']}, after: {info['after']['size']}. " \
                   f"It must be: {info['before']['size']} and {info['before']['size'] + 1}"

        return "OK"

    def get_pods_name(self):
        names = []
        self.stdout, _ = self.run(["oc", "get", "pods", "--selector", "app=addressbook", "-ojson"])
        try:
            info = json.loads(self.stdout)
            for pod in info['items']:
                names.append(pod['metadata']['name'])
            return names, True
        except:
            return names, False


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Deployment": checker.check_deployment(),
                    "StatefulSet": checker.check_stateful_set(),
                    "Selector": checker.check_pods_by_selector(), }

    if check_result["Deployment"] == "OK" \
            and check_result["StatefulSet"] == "OK" \
            and check_result["Selector"] == "OK":
        check_result['Application available'] = checker.check_rows()
        if check_result['Application available'] == "OK":
            check_result['Available after drops'] = checker.check_pod_drops()
        else:
            check_result['Available after drops'] = "FAIL: Didn't run checker"
    else:
        check_result['Application available'] = "FAIL: Didn't run checker"
        check_result['Available after drops'] = "FAIL: Didn't run checker"

    json_object = json.dumps(check_result, indent=4)
    print(json_object)
