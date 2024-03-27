#!/usr/bin/env bash

cat >script.sh <<EOL
#!/usr/bin/env python3
from pathlib import Path

if __name__ == '__main__':
    if Path("file.txt").exists():
        exit(0)
    else:
        exit(1)

EOL

chmod +x script.sh