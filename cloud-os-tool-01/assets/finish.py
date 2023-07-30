#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.pod_name_expect = "my-application"
        self.image_expect = 'busybox'

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

            pod = info["items"][0]
            pod_name_actual = pod['metadata']['name']
            if pod_name_actual != self.pod_name_expect:
                return f"FAIL: Неправильное имя Pod'а: {pod_name_actual}. Должно быть: '{self.pod_name_expect}'."

            image_actual = pod['spec']['containers'][0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Pod'ов в системе"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check pod": checker.check_pod(), }

    json_object = json.dumps(check_result)
    print(json_object)
