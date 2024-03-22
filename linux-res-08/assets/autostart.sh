#!/bin/bash -x

runuser -u ubuntu -- python3 -m http.server -d /home/ubuntu/web

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE