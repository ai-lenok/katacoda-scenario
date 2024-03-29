#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_reading_file", "file.txt")
        kwargs.setdefault("reference_command", f'head  -n 15 {kwargs["reference_reading_file"]} | tail')
        kwargs.setdefault("is_message_success_from_stdout", True)
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.reading_file_exists)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.reference_command)
                .do(self.compare_text)
                .finish())

    def reading_file_exists(self):
        if not Path(self.params["reference_reading_file"]).is_file():
            return self.fail(f'{self.params["reference_reading_file"]} не существует')
        return self


if __name__ == '__main__':
    print(Checker().finish_json())
