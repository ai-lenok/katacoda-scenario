#!/usr/bin/env python3
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
                .do(self.not_empty)
                .do(self.reference_command)
                .do(self.compare_text)
                .finish())


if __name__ == '__main__':
    print(Checker().finish_json())
