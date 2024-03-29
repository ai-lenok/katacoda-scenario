#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.pod_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.port_expect = 8080
        self.count_containers = 1

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

            containers = pod['spec']['containers']
            if len(containers) != self.count_containers:
                return f"FAIL: Неправильное количество контейнеров в Pod'е: {len(containers)}. Должно быть: {self.count_containers}."

            image_actual = containers[0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            if 'ports' not in containers[0]:
                return "FAIL: Не обнаружил открытых портов"
            ports = containers[0]['ports']
            if 1 < len(ports):
                return f"FAIL: Слишком много открытых портов: {ports}. Должен быть один."
            port_actual = ports[0]["containerPort"]
            if port_actual != self.port_expect:
                return f"FAIL: Открыт неправильный порт: {port_actual}. Должно быть: '{self.port_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Pod'ов в системе"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Check pod": checker.check_pod(), }

    json_object = json.dumps(check_result)
    print(json_object)
