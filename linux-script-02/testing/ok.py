#!/usr/bin/env python3
import re
from pathlib import Path


def user_exists(user_name: str):
    users_text = Path("/etc/passwd").read_text()
    print(users_text)
    return re.match(r'user:x:\d+:\d+:[\w\s]*:/home/user:/bin/sh', users_text)


if __name__ == '__main__':
    if user_exists("user"):
        exit(0)
    else:
        exit(1)
