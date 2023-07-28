#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.pod_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.labels_expect = {"app": "addressbook", "environment": "dev", "release": "stable", }
        self.annotations_expect = {"documentation": "https://example.com/docs", "dependency": "postgres",
                                   "author": "user", "email": "user@example.com", }
        self.pod_data = {}

    @staticmethod
    def run(command):
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        return stdout, stderr

    def check_pod(self):
        command = ["oc", "get", "pods", "-ojson"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            count_pods = len(info["items"])
            if count_pods == 0:
                return "FAIL: Не обнаружено Pod'ов в системе"
            if 1 < count_pods:
                return f"FAIL: Слишком много Pod'ов: {count_pods}. Должен быть один."

            self.pod_data = info["items"][0]
            pod_name_actual = self.pod_data['metadata']['name']
            if pod_name_actual != self.pod_name_expect:
                return f"FAIL: Не правильное имя Pod'а: {pod_name_actual}. Должно быть: '{self.pod_name_expect}'."

            image_actual = self.pod_data['spec']['containers'][0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Не правильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Pod'ов в системе"

    def check_labels(self):
        if not 'labels' in self.pod_data['metadata']:
            return "FAIL: Отсутствуют labels"

        labels = self.check_tags(self.pod_data['metadata']['labels'], self.labels_expect)
        check_labels = self.tags_checking_to_text(labels, "Не правильные labels:")

        if check_labels:
            return f"FAIL: {check_labels}"

        return "OK"

    def check_annotations(self):
        if not 'annotations' in self.pod_data['metadata']:
            return "FAIL: Отсутствуют annotations"

        annotations = self.check_tags(self.pod_data['metadata']['annotations'], self.annotations_expect)
        check_annotations = self.tags_checking_to_text(annotations, "Не правильные annotations:")

        if check_annotations:
            return f"FAIL: {check_annotations}"
        return "OK"

    def check_tags(self, tags_actual, tags_expect):
        dict_checking = {}
        for key, value in tags_expect.items():
            if key in tags_actual:
                if tags_actual[key] == value:
                    dict_checking[key] = {"status": "OK"}
                else:
                    dict_checking[key] = {"status": "incorrect", "value": tags_actual[key]}
            else:
                dict_checking[key] = {"status": "missing"}
        return dict_checking

    def tags_checking_to_text(self, tags_checking, fail_message_in):
        is_ok = True
        fail_msg = fail_message_in
        for key, value in tags_checking.items():
            if value["status"] != "OK":
                is_ok = False
                if value["status"] == "incorrect":
                    fail_msg += f' "{key}": "{value["value"]}".'
                if value["status"] == "missing":
                    fail_msg += f' Отсутствует "{key}".'
        if is_ok:
            return ""
        else:
            return fail_msg


if __name__ == '__main__':
    checker = Checker()
    check_result = {}
    check_result["Check pod"] = checker.check_pod()
    if check_result["Check pod"] == "OK":
        check_result["labels"] = checker.check_labels()
        check_result["annotations"] = checker.check_annotations()

    json_object = json.dumps(check_result)
    print(json_object)
