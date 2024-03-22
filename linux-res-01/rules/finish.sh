#!/usr/bin/env python3
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester

import re


class Checker(Tester):
    def __init__(self, **kwargs):
        self.pattern_memory_bytes = self.__generate_pattern('[\d\.]+')
        if "reference_pattern" not in kwargs:
            kwargs["reference_pattern"] = self.__generate_pattern('[\d\.]+[GMKBi]+')
        super().__init__(**kwargs)

    def __generate_pattern(self, number_pattern: str):
        space = '\s+'
        size = f'{number_pattern}{space}'
        return re.compile(f'\s*total\s+used\s+free\s+shared\s+buff\/cache\s+available\s+'
                          f'Mem:\s+{size}{size}{size}{size}{size}{size}'
                          f'Swap:\s+{size}{size}{number_pattern}')

    def check(self):
        return (self
                .do(self.run)
                .do(self.not_empty)
                .do(self.wrong_format)
                .do(self.compare_regex)
                .finish())

    def wrong_format(self):
        if re.match(self.pattern_memory_bytes, self.stdout):
            return self.fail(f'Нужно вывести ответ в удобном для человека виде')
        return self


if __name__ == '__main__':
    print(Checker().finish_json())
