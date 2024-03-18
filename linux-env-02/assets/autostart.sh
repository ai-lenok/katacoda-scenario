#!/bin/bash -x

mkdir -p /home/ubuntu/dir/

chown ubuntu:ubuntu /home/ubuntu/dir/

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE