#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_command", f'curl localhost:8000')
        self.params.setdefault("reference_stop_words", ["echo", "printf", "cat"])
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.reliable_reference_command)
                .do(self.compare_text)
                .finish())

    def reliable_reference_command(self):
        try:
            process = subprocess.run([self.params["reference_command"]],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True,
                                     shell=True,
                                     executable="/bin/bash")

            self.params["reference_output"] = process.stdout.strip()
            return self
        except:
            return self.fail("Сервер не работает")


if __name__ == '__main__':
    print(Checker().finish_json())
