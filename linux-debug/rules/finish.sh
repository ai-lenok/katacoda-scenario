#!/usr/bin/env python3
import sys

sys.path.insert(0, '/usr/local/')

from lib.tester_lib import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reference_pattern = r"\s*PID\s+TTY\s+TIME\s+CMD\s+(\s+\d+\s+[\w?\/]+\s+[\d:]+\s+[\w\-\/:\(\)]+)+"

    def check(self) -> str:
        return (self
                .do(self.check_and_run)
                .do(self.check_not_empty)
                .do(self.compare_regex)
                .finish())


if __name__ == '__main__':
    print(Checker().finish_json())
