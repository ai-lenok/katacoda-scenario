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
        self.status = TestStatus.not_finish
        self.message = ""

        self.stdout = ''
        self.stderr = ''

        self.is_message_success_from_stdout = kwargs.get("is_message_success_from_stdout", False)
        self.message_success = kwargs.get("message_success", "")
        self.check_name = kwargs.get("check_name", "check")

        self.reference_output = kwargs.get("reference_output", "")
        self.reference_pattern = kwargs.get("reference_pattern", "")

        self.checking_script = kwargs.get("checking_script", '/home/ubuntu/script.sh')

        self.current_dir = kwargs.get("current_dir", '/home/ubuntu')
        os.chdir(self.current_dir)

    def do(self, func):
        if self.status == TestStatus.not_finish:
            return func()
        else:
            return self

    def ok(self, message=""):
        self.status = TestStatus.ok
        if message:
            self.message = message
        elif self.is_message_success_from_stdout:
            self.message = self.stdout
        else:
            self.message = self.message_success
        return self

    def fail(self, message=""):
        self.status = TestStatus.fail
        self.message = message
        return self

    def finish_json(self) -> str:
        result = {self.check_name: self.finish()}
        return json.dumps(result, ensure_ascii=False)

    def finish(self) -> str:
        if self.status == TestStatus.ok:
            return "OK"
        elif self.status == TestStatus.fail:
            return "FAIL: " + self.message
        else:
            return "FAIL: Автотест не смог проверить результат"

    def run_script(self):
        subprocess.run(['chmod', '+x', self.checking_script])
        process = subprocess.run([self.checking_script],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        self.stdout = process.stdout.strip()
        self.stderr = process.stderr.strip()
        return self

    def check_and_run(self):
        if not Path(self.checking_script).is_file():
            return self.fail(f'{self.checking_script} не существует')

        return self.run_script()

    def check_not_empty(self):
        if not self.stdout:
            return self.fail(f'Скрипт ничего не вывел')
        return self

    def compare_text(self):
        if self.stdout == self.reference_output:
            return self.ok()
        else:
            return self.fail(f'Неправильный ответ:\n\n{self.stdout}')

    def compare_regex(self):
        if re.match(self.reference_pattern, self.stdout):
            return self.ok()
        else:
            return self.fail(f'Неправильный ответ:\n\n{self.stdout}')
