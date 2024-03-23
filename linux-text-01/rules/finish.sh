#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_reading_file", "file.txt")
        kwargs.setdefault("count_file_lines", 4)
        kwargs.setdefault("is_message_success_from_stdout", True)
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.reading_file_exists)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.compare_wrong_part_file)
                .do(self.compare_part_file)
                .finish())

    def reading_file_exists(self):
        if not Path(self.params["reference_reading_file"]).is_file():
            return self.fail(f'{self.params["reference_reading_file"]} не существует')
        return self

    def compare_wrong_part_file(self):
        with open(self.params["reference_reading_file"], "r") as file:
            text = file.read().split("\n")
            output_lines = self.stdout.split("\n")
            count_file_lines = self.params["count_file_lines"]
            if text[:10] == output_lines:
                return self.fail(f"Нужно вывести {count_file_lines} строк(и)")

        return self

    def compare_part_file(self):
        with open(self.params["reference_reading_file"], "r") as file:
            text = file.read().split("\n")
            output_lines = self.stdout.split("\n")
            count_file_lines = self.params["count_file_lines"]
            if text[:count_file_lines] == output_lines:
                return self.ok()

        return self.fail(f"Неправильный ответ:\n\n{self.stdout}")


if __name__ == '__main__':
    print(Checker().finish_json())
