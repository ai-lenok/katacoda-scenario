#!/usr/bin/env python3

import json

# Data to be written
check_result ={
  "script01": "OK",
  "script02": "FAIL: File or directory does not exist: _file_name_",
  "script03": "FAIL: I found the wrong text: _word_",
  "script04": "FAIL: The filename is incorrect: _file_name_",
}

json_object = json.dumps(check_result, indent = 4)
print(json_object)

# class Checker:
#     def __init__(self, script_name):
#         self.stdout = ''
#         self.stderr = ''
#         self.script_name = script_name
#         self.path = f'script/{script_name}'
#
#         method_name = 'check_script_' + script_name[:2]
#         self.check_method = getattr(self, method_name, self.__default_method)
#
#     def __default_method(self):
#         print(f'Unknown script {self.script_name}')
#
#     def __run_script(self):
#         subprocess.run(['chmod', '+x', self.path])
#         process = subprocess.run([self.path],
#                                  stdout=subprocess.PIPE,
#                                  stderr=subprocess.PIPE,
#                                  universal_newlines=True)
#
#         stdout = process.stdout.strip()
#         stderr = process.stderr.strip()
#         print(stdout)
#         print(stderr)
#         return stdout, stderr
#
#     def __check_stop_words(self, words):
#         """
#         Проверяем, что не используем команду echo или printf
#         :param path: Путь к проверяемому файлу
#         :return: True - используется, False - не используется
#         """
#         with open(self.path, mode='r') as fid:
#             text_file = fid.read()
#             for w in words:
#                 if w in text_file:
#                     return True
#
#         return False
#
#     def check(self):
#         print(f"Check script: {self.script_name}")
#
#         if not pathlib.Path(self.path).is_file():
#             print(f'{self.path} does not exist')
#             return False
#
#         self.stdout, self.stderr = self.__run_script()
#
#         return self.check_method()