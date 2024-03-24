#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_command", f'nc -zv localhost 8000')
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.not_empty_stderr)
                .do(self.reference_command_stderr)
                .do(self.compare_text_stderr)
                .finish())

    def not_empty_stderr(self):
        if not self.stderr:
            return self.fail(f'Скрипт ничего не вывел')
        return self

    def reference_command_stderr(self):
        process = subprocess.run([self.params["reference_command"]],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 shell=True,
                                 executable="/bin/bash")

        self.params["reference_output"] = process.stderr.strip()
        return self

    def compare_text_stderr(self):
        if self.stderr == self.params["reference_output"]:
            return self.ok()
        else:
            return self.fail(f"Неправильный ответ:\n\n{self.stderr}")


if __name__ == '__main__':
    print(Checker().finish_json())
