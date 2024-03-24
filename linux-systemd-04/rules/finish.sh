#!/usr/bin/env python3
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_command", f'sudo journalctl')
        kwargs.setdefault("is_message_success_from_stdout", True)
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.reference_command)
                .do(self.compare_text)
                .finish())


if __name__ == '__main__':
    print(Checker().finish_json())
