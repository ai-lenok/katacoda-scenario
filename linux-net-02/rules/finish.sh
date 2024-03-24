#!/usr/bin/env python3
import sys

sys.path.insert(1, '/usr/local/lib/')

from ExerciseTester.tester import Tester


class Checker(Tester):
    def __init__(self, **kwargs):
        kwargs.setdefault("reference_pattern",
                          r'^PING\s+localhost\(localhost\s+\(::\d+\)\)\s+\d+\s+data\s+bytes\s+'
                          r'(\d+\s+bytes\s+from\s+localhost\s+\(::\d+\):\s+icmp_seq=\d+\s+ttl=\d+\s+time=[\d.]+\s+ms\s+)+\s+'
                          r'---\s+localhost\s+ping\s+statistics\s+---\s+'
                          r'\d+\s+packets\s+transmitted,\s+\d+\s+received,\s+0%\s+packet\s+loss,\s+time\s+\d+ms\s+'
                          r'rtt\s+min/avg/max/mdev\s+=\s+[\d./]+\s+ms$')
        super().__init__(**kwargs)

    def check(self):
        return (self
                .do(self.run)
                .do(self.stop_words)
                .do(self.not_empty)
                .do(self.compare_regex)
                .finish())


if __name__ == '__main__':
    print(Checker().finish_json())
