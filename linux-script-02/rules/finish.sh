#!/usr/bin/env python3
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        self.return_code = 0
        super().__init__(**kwargs)

    def check(self) -> str:
        return (self
                .do(self.script_exists)
                .do(self.is_execution)
                .do(self.run_script)
                .do(self.check_status)
                .finish())

    def script_exists(self):
        if not Path(self.params["checking_script"]).is_file():
            return self.fail(f'{self.params["checking_script"]} не существует')
        return self

    def is_execution(self):
        file_mode = Path(self.params["checking_script"]).stat().st_mode
        if not stat.S_IXUSR & file_mode:
            return self.fail(f'У файла {self.params["checking_script"]} нет права выполнения')
        return self

    def run_script(self):
        try:
            process = subprocess.run([self.params["checking_script"]],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True,
                                     executable="/bin/bash")

            self.stdout = process.stdout.strip()
            self.stderr = process.stderr.strip()
            self.return_code = process.returncode
        except:
            self.fail(f'Во время выполнения скрипта возникла ошибка')
        return self

    def check_status(self):
        if self.return_code != 0:
            return self.ok()
        else:
            return self.fail(
                f'Скрипт вернул успешный статус')


if __name__ == '__main__':
    print(Checker().finish_json())
