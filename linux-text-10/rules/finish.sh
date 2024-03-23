#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_pattern",
                          r'lrwxrwxrwx\s+\d+\s+\w+\s+\w+\s+\d+\s+\w+\s+\d+\s+[\d:]+\s+\w+\s+->\s+[\w/-]+')
        kwargs.setdefault("reference_reading_file", "file.txt")
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.write_analyzed_file)
                .do(self.run)
                .do(self.stop_words)
                .do(self.reading_file_exists)
                .do(self.not_empty)
                .do(self.compare_regex)
                .finish())

    def write_analyzed_file(self):
        subprocess.run([f'ls -l /dev > {self.params["reference_reading_file"]}'],
                       shell=True, executable="/bin/bash")
        return self

    def reading_file_exists(self):
        if not Path(self.params["reference_reading_file"]).is_file():
            return self.fail(f'{self.params["reference_reading_file"]} не существует')
        return self


if __name__ == '__main__':
    print(Checker().finish_json())
