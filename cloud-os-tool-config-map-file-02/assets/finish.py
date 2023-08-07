#!/usr/bin/env python3

import json
import subprocess


class Checker:
    def __init__(self):
        self.stdout = ''
        self.stderr = ''
        self.deployment_name_expect = "addressbook"
        self.image_expect = 'nexus.local:5000/java-school/cloud/addressbook:1'
        self.count_containers = 1
        self.count_volumes = 1
        self.count_mount_config_map = 1
        self.volume_name_expect = 'deployment-volume'
        self.config_map_with_file_expect = 'application-file-config'
        self.config_mount_path_expect = '/app/config/'
        self.deployment = {}

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
        command = ["oc", "get", "deployments", "--output", "json"]
        self.stdout, _ = self.run(command)

        try:
            info = json.loads(self.stdout)
            count_deployments = len(info["items"])
            if count_deployments == 0:
                return "FAIL: Не обнаружено Deployments'ов в системе"
            if 1 < count_deployments:
                return f"FAIL: Слишком много Deployments'ов: {count_deployments}. Должен быть один."

            self.deployment = info["items"][0]
            deployment_name_actual = self.deployment['metadata']['name']
            if deployment_name_actual != self.deployment_name_expect:
                return f"FAIL: Неправильное имя Deployments'а: {deployment_name_actual}. Должно быть: '{self.deployment_name_expect}'."

            containers = self.deployment['spec']['template']['spec']['containers']
            if len(containers) != self.count_containers:
                return f"FAIL: Неправильное количество контейнеров в Pod'е: {len(containers)}. Должно быть: {self.count_containers}."

            image_actual = containers[0]['image']
            if image_actual != self.image_expect:
                return f"FAIL: Неправильный Docker-образ: {image_actual}. " \
                       f"Должен быть: '{self.image_expect}'."

            return "OK"
        except:
            return "FAIL: Не обнаружено Deployments'ов в системе"

    def check_create_volumes(self):
        if "volumes" not in self.deployment['spec']['template']['spec']:
            return 'FAIL: В конфигурации deployment.spec.template.spec отсутствует "volumes".'
        volumes = self.deployment['spec']['template']['spec']['volumes']
        if len(volumes) != self.count_volumes:
            return f'FAIL: В секции deployment.spec.template.spec.volumes неправильное количество настроек: {len(volumes)}. ' \
                   f'Должно быть: {self.count_volumes}.'
        volume = volumes[0]
        if volume['name'] != self.volume_name_expect:
            return f'FAIL: Неправильное имя в секции deployment.spec.template.spec.volumes:\n' \
                   f'  "{volume["name"]}".\n' \
                   f'Должно быть: "{self.volume_name_expect}".'
        if 'configMap' not in volume:
            return 'FAIL: В конфигурации deployment.spec.template.spec.volumes отсутствует "configMap".'
        config_map = volume['configMap']
        if config_map['name'] != self.config_map_with_file_expect:
            return f'FAIL: В секции deployment.spec.template.spec.volumes.configMap ' \
                   f'объявлен неправильный ConfigMap:\n' \
                   f'  "{config_map["name"]}".\n' \
                   f'Должен быть: "{self.config_map_with_file_expect}".'
        return "OK"

    def check_mount_config_map(self):
        container = self.deployment['spec']['template']['spec']['containers'][0]
        if 'volumeMounts' not in container:
            return 'FAIL: В конфигурации deployment.spec.template.spec.containers отсутствует "volumeMounts".'
        volume_mounts = container['volumeMounts']
        if len(volume_mounts) != self.count_mount_config_map:
            return f'FAIL: В секции deployment.spec.template.spec.containers.volumeMounts ' \
                   f'неправильное количество настроек: {len(volume_mounts)}. ' \
                   f'Должно быть: {self.count_mount_config_map}.'
        config_map = volume_mounts[0]
        if config_map['name'] != self.volume_name_expect:
            return f'FAIL: Неправильное имя в секции deployment.spec.template.spec.containers.volumeMounts: "{config_map["name"]}".' \
                   f'Должно быть: "{self.volume_name_expect}".'
        if 'mountPath' not in config_map:
            return 'FAIL: В конфигурации deployment.spec.template.spec.containers.volumeMounts отсутствует "mountPath".'
        if config_map['mountPath'] != self.config_mount_path_expect:
            return f'FAIL: Неправильная точка монтирования в секции\n' \
                   f'deployment.spec.template.spec.containers.volumeMounts:\n' \
                   f'  "{config_map["mountPath"]}".\n' \
                   f'Должна быть: "{self.config_mount_path_expect}".'
        return "OK"


if __name__ == '__main__':
    checker = Checker()
    check_result = {"Deployment": checker.check_deployment()}
    if check_result["Deployment"] == "OK":
        check_result["Volumes"] = checker.check_create_volumes()
        if check_result["Volumes"] == "OK":
            check_result["Mount"] = checker.check_mount_config_map()
    json_object = json.dumps(check_result)
    print(json_object)
