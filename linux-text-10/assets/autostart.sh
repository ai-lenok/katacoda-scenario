#!/bin/bash -x

ls -l /dev > /home/ubuntu/file.txt

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE