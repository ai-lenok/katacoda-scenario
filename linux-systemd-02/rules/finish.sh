#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_command", 'systemctl list-units --type=service')
        kwargs.setdefault("reference_command_wrong", 'systemctl list-units')
        kwargs.setdefault("is_message_success_from_stdout", True)
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.reference_command_wrong)
                .do(self.reference_command)
                .do(self.compare_text)
                .finish())

    def reference_command_wrong(self):
        process = subprocess.run([self.params["reference_command_wrong"]],
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 shell=True,
                                 executable="/bin/bash")

        reference_output_wrong_command = process.stdout.strip()

        if reference_output_wrong_command == self.stdout:
            return self.fail("Нужно вывести только сервисы, а не все службы")

        return self


if __name__ == '__main__':
    print(Checker().finish_json())
