#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.pod_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.count_containers = 1
        self.labels_expect = {"app": "addressbook", "environment": "dev", "release": "stable", }
        self.annotations_expect = {"documentation": "https://example.com/docs", "dependency": "postgres",
                                   "author": "user", "email": "user@mail.com", }
        self.pod = {}

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

            self.pod = info["items"][0]
            pod_name_actual = self.pod['metadata']['name']
            if pod_name_actual != self.pod_name_expect:
                return f"FAIL: Неправильное имя Pod'а: {pod_name_actual}. Должно быть: '{self.pod_name_expect}'."

            containers = self.pod['spec']['containers']
            if len(containers) != self.count_containers:
                return f"FAIL: Неправильное количество контейнеров в Pod'е: {len(containers)}. Должно быть: {self.count_containers}."

            image_actual = self.pod['spec']['containers'][0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Pod'ов в системе"

    def check_labels(self):
        if 'labels' not in self.pod['metadata']:
            return "FAIL: Отсутствуют labels"

        check_labels = self.compare_dict(self.pod['metadata']['labels'], self.labels_expect, "Неправильные labels:\n")

        if check_labels:
            return f"FAIL: {check_labels}"

        return "OK"

    def check_annotations(self):
        if 'annotations' not in self.pod['metadata']:
            return "FAIL: Отсутствуют annotations"

        check_annotations = self.compare_dict(self.pod['metadata']['annotations'], self.annotations_expect,
                                              "Неправильные annotations:\n")

        if check_annotations:
            return f"FAIL: {check_annotations}"
        return "OK"

    def compare_dict(self, actual: dict, expect: dict, prefix_msg: str) -> str:
        diff = set(expect.items()) - set(actual.items())
        if not diff:
            return ""

        fail_msg = prefix_msg
        for key in dict(diff):
            if key in actual:
                fail_msg += f'- Неправильное значение\n    ' \
                            f'"{key}": "{actual[key]}",\n    ' \
                            f'должен быть\n    ' \
                            f'"{key}": "{expect[key]}". \n'
            else:
                fail_msg += f'- Отсутствует "{key}". \n'
        return fail_msg


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check pod": checker.check_pod()}
    if check_result["Check pod"] == "OK":
        check_result["labels"] = checker.check_labels()
        check_result["annotations"] = checker.check_annotations()

    json_object = json.dumps(check_result)
    print(json_object)
