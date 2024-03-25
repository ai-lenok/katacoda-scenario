#!/usr/bin/env python3
import re
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_command", "crontab -u ubuntu -l")
        kwargs.setdefault("reference_pattern", r'^(\*\s+){5}')
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.reference_command)
                .do(self.cron_condition_analysis)
                .finish())

    def cron_condition_analysis(self):
        lines = self.params["reference_output"].split('\n')

        for line in lines:
            if re.match(self.params["reference_pattern"], line):
                return self.ok()
        return self.fail("Не смог найти задачу, которая выполняется каждую минуту")


if __name__ == '__main__':
    print(Checker().finish_json())
