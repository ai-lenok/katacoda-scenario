#!/bin/bash -x

chmod 444 /home/ubuntu/file.txt
chown root /home/ubuntu/file.txt

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE