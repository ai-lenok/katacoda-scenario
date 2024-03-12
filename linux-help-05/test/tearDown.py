#!/usr/bin/env python3

from pathlib import Path

file = Path("script.sh")
if file.exists():
    file.unlink()