#!/bin/bash -x

runuser -u ubuntu -c python3 -m http.server &

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE