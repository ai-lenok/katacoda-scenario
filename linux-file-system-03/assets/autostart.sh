#!/bin/bash -x

mkdir /home/ubuntu/dir
chown ubunt:ubuntu /home/ubuntu/dir

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE