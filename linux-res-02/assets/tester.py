import enum
import json
import os
import re
import subprocess
from pathlib import Path


class TestStatus(enum.Enum):
    not_finish = 1
    ok = 2
    fail = 3


class Tester:
    def __init__(self, **kwargs):
        self.params = kwargs
        self.status = TestStatus.not_finish
        self.message = ""

        self.stdout = ''
        self.stderr = ''

        self.params.setdefault("is_message_success_from_stdout", False)
        self.params.setdefault("message_success", "")
        self.params.setdefault("check_name", "check")

        self.params.setdefault("reference_output", "")
        self.params.setdefault("reference_pattern", "")
        self.params.setdefault("reference_stop_words", ["echo", "printf"])
        kwargs.setdefault("reference_command", "")

        self.params.setdefault("checking_script", '/home/ubuntu/script.sh')

        self.params.setdefault("current_dir", '/home/ubuntu')
        os.chdir(self.params["current_dir"])

    def do(self, func):
        if self.status == TestStatus.not_finish:
            return func()
        else:
            return self

    def ok(self, message=""):
        self.status = TestStatus.ok
        if message:
            self.message = message
        elif self.params["is_message_success_from_stdout"]:
            self.message = self.stdout
        else:
            self.message = self.params["message_success"]
        return self

    def fail(self, message=""):
        self.status = TestStatus.fail
        self.message = message
        return self

    def finish_json(self) -> str:
        result = {self.params["check_name"]: self.check()}
        return json.dumps(result, ensure_ascii=False)

    def check(self):
        return self.finish()

    def finish(self) -> str:
        if self.status == TestStatus.ok:
            return "OK"
        elif self.status == TestStatus.fail:
            return "FAIL: " + self.message
        else:
            return "FAIL: Автотест не смог проверить результат"

    def run_script(self):
        subprocess.run(['chmod', '+x', self.params["checking_script"]])
        process = subprocess.run([self.params["checking_script"]],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        self.stdout = process.stdout.strip()
        self.stderr = process.stderr.strip()
        return self

    def run(self):
        if not Path(self.params["checking_script"]).is_file():
            return self.fail(f'{self.params["checking_script"]} не существует')

        return self.run_script()

    def not_empty(self):
        if not self.stdout:
            return self.fail(f'Скрипт ничего не вывел')
        return self

    def compare_text(self):
        if self.stdout == self.params["reference_output"]:
            return self.ok()
        else:
            return self.fail(f"Неправильный ответ:\n\n{self.stdout}")

    def compare_regex(self):
        if re.match(self.params["reference_pattern"], self.stdout):
            return self.ok()
        else:
            return self.fail(f"Неправильный ответ:\n```text\n{self.stdout}\n```")

    def stop_words(self):
        """Проверяем, что не используем команду echo или printf"""
        words = self.params.get("reference_stop_words", ["echo", "printf"])
        with open(self.params["checking_script"], mode='r') as fid:
            text_file = fid.read()
            for w in words:
                if w in text_file:
                    return self.fail(
                        "Пожалуйста, используйте утилиту, которая подставит нужный текст, а не вводите его сами")

        return self

    def reference_command(self):
        process = subprocess.run([self.params["reference_command"]],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 shell=True,
                                 executable="/bin/bash")

        self.params["reference_output"] = process.stdout.strip()
        return self
