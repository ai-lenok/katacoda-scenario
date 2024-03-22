#!/usr/bin/env python3
import sys

import requests

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.address = kwargs.get("address", 'http://localhost:8000')

    def check(self) -> str:
        return (self
                .do(self.request)
                .finish())

    def request(self):
        try:
            requests.get(self.address)
            return self.fail("Сервер работает")
        except requests.exceptions.ConnectionError:
            return self.ok("Сервер выключен")


if __name__ == '__main__':
    print(Checker().finish_json())
