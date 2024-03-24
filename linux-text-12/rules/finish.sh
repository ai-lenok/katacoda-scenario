#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_reading_file", "file.txt")
        kwargs.setdefault("reference_command", f'wc -l {kwargs["reference_reading_file"]}')
        kwargs.setdefault("reference_command_wrong", f'wc {kwargs["reference_reading_file"]}')
        kwargs.setdefault("preparatory_command", f'ls -l /dev > {kwargs["reference_reading_file"]}')
        kwargs.setdefault("is_message_success_from_stdout", True)
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.preparatory_command)
                .do(self.run)
                .do(self.stop_words)
                .do(self.reading_file_exists)
                .do(self.not_empty)
                .do(self.reference_command_wrong)
                .do(self.reference_command)
                .do(self.compare_text)
                .finish())

    def preparatory_command(self):
        subprocess.run([self.params["preparatory_command"]],
                       shell=True, executable="/bin/bash")
        return self

    def reading_file_exists(self):
        if not Path(self.params["reference_reading_file"]).is_file():
            return self.fail(f'{self.params["reference_reading_file"]} не существует')
        return self

    def reference_command_wrong(self):
        process = subprocess.run([self.params["reference_command_wrong"]],
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 shell=True,
                                 executable="/bin/bash")

        reference_output_wrong_command = process.stdout.strip()

        if reference_output_wrong_command == self.stdout:
            return self.fail("Нужно вывести только количество строк")

        return self


if __name__ == '__main__':
    print(Checker().finish_json())
