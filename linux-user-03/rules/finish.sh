#!/usr/bin/env python3
import re
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        # docker:x:130:anton,user
        kwargs.setdefault("adding_user", 'user')
        kwargs.setdefault("adding_group", 'docker')
        kwargs.setdefault("reference_command", 'cat /etc/group')
        kwargs.setdefault("reference_pattern",
                          f'{kwargs["adding_group"]}:x:\d+:[\w,]*{kwargs["adding_user"]}[\w,]*')
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.reference_command)
                .do(self.compare_regex)
                .finish())

    def compare_regex(self):
        if re.search(self.params["reference_pattern"], self.params["reference_output"]):
            return self.ok()
        else:
            return self.fail(f'Пользователя {self.params["adding_user"]} нет в группе {self.params["adding_user"]}')


if __name__ == '__main__':
    print(Checker().finish_json())
