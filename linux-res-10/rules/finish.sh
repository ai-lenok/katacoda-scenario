#!/usr/bin/env python3
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_pattern", r".*[\d\.\-]*-generic.*")
        super().__init__(**kwargs)
        self.reference_short_format = kwargs.get("reference_short_format", "Linux")

    def check(self) -> str:
        return (self
                .do(self.run)
                .do(self.not_empty)
                .do(self.short_format)
                .do(self.compare_regex)
                .finish())

    def short_format(self):
        if self.stdout == self.reference_short_format:
            return self.fail(f'Нужно вывести подробную информацию')
        return self


if __name__ == '__main__':
    print(Checker().finish_json())
