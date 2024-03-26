#!/usr/bin/env python3
import re
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("creating_user", 'user')
        kwargs.setdefault("reference_command", 'cat /etc/passwd')
        kwargs.setdefault("reference_pattern",
                          f'{kwargs["creating_user"]}:x:\d+:\d+:[\w\s]*:/home/user:/bin/sh')
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.reference_command)
                .do(self.compare_regex)
                .finish())

    def compare_regex(self):
        if not re.match(self.params["reference_pattern"], self.params["reference_output"]):
            return self.ok()
        else:
            return self.fail(f'Пользователь {self.params["creating_user"]} не найден')


if __name__ == '__main__':
    print(Checker().finish_json())
